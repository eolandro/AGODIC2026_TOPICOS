from collections import deque
import os

# =====================================================================
#  Extractor de archivos (file carving) desde una imagen de disco.
#
#  Mantiene la MISMA IDEA de tu codigo original:
#   - Se lee byte por byte
#   - Se usa una "cola" (Cache) para detectar cuando aparece una cabecera
#
#  LO QUE CAMBIA respecto a la version anterior:
#   - Antes, para videos/bmp, el programa "adivinaba" el final buscando
#     la siguiente cabecera conocida. Eso casi siempre corta el archivo
#     en un punto incorrecto -> por eso salian videos/bmp que no abrian.
#   - Ahora, para los formatos que GUARDAN su propio tamaño dentro del
#     header (RIFF/AVI/WAV, BMP, MP4/MOV), se lee ese tamaño real y se
#     copia exactamente esa cantidad de bytes. El archivo queda íntegro.
#   - Para JPG/PNG/GIF/PDF/ZIP se sigue usando el "pie" (footer), igual
#     que en tu idea original, porque para esos si funciona bien.
# =====================================================================

# ---------- Formatos con pie de archivo conocido (igual que antes) ----------
FOOTER_FORMATS = {
    "jpg":   (b'\xff\xd8\xff',          b'\xff\xd9',                       "imagenes"),
    "png":   (b'\x89PNG\r\n\x1a\n',     bytes.fromhex("49454E44AE426082"), "imagenes"),
    "gif89": (b'GIF89a',                b'\x00\x3b',                       "imagenes"),
    "gif87": (b'GIF87a',                b'\x00\x3b',                       "imagenes"),
    "pdf":   (b'%PDF-',                 b'%%EOF',                          "otros"),
    "zip":   (b'PK\x03\x04',            bytes.fromhex("504B0506"),         "otros"),
}

# ---------- Cabeceras "disparadoras" que se buscan en el escaneo ----------
# ("tipo_de_manejo", bytes_a_buscar)
DISPARADORES = [
    ("riff", b'RIFF'), ("mp4", b'ftyp'), ("bmp", b'BM'), ("mkv", b'\x1a\x45\xdf\xa3'),
    ("mp3_excluir", b'ID3'),          # mp3 con etiqueta ID3
    ("mp3_excluir", b'\xff\xfb'),     # mp3 sin etiqueta (frame sync MPEG)
]
for ext, (cab, pie, cat) in FOOTER_FORMATS.items():
    DISPARADORES.append(("footer:" + ext, cab))

MAXH = max(len(h) for _, h in DISPARADORES)


# ---------------------------------------------------------------------
#  Extractores especializados: reciben el archivo abierto y la posicion
#  donde inicia la cabecera, y devuelven (bytes_completos, extension, categoria)
# ---------------------------------------------------------------------

def extraer_riff(entrada, inicio):
    """AVI y WAV son formato RIFF: el propio header dice su tamaño total."""
    entrada.seek(inicio)
    cab = entrada.read(12)                      # 'RIFF' + tamaño(4) + tipo(4)
    if len(cab) < 12:
        return None
    tam_dato = int.from_bytes(cab[4:8], "little")
    tipo = cab[8:12]
    total = tam_dato + 8                         # 8 = 'RIFF' + campo de tamaño
    if tipo == b'AVI ':
        ext, cat = "avi", "videos"
    else:
        return None   # WAVE u otro tipo RIFF (audio) -> se ignora, no se extrae
    if total <= 12 or total > 700 * 1024 * 1024:  # validacion de sanidad
        return None
    entrada.seek(inicio)
    return entrada.read(total), ext, cat


def extraer_bmp(entrada, inicio):
    """El header de BMP guarda el tamaño total en los bytes 2-5."""
    entrada.seek(inicio)
    cab = entrada.read(6)
    if len(cab) < 6 or cab[:2] != b'BM':
        return None
    total = int.from_bytes(cab[2:6], "little")
    if total <= 54 or total > 100 * 1024 * 1024:
        return None
    entrada.seek(inicio)
    return entrada.read(total), "bmp", "imagenes"


def extraer_mp4(entrada, inicio_ftyp):
    """
    MP4/MOV estan hechos de 'boxes': [tamaño(4)][tipo(4)][datos...]
    Vamos sumando el tamaño de cada box hasta encontrar uno que ya no
    parezca valido (ahi termina el archivo real).
    """
    inicio = inicio_ftyp - 4          # el tamaño del primer box va 4 bytes ANTES de 'ftyp'
    if inicio < 0:
        return None
    entrada.seek(inicio)
    pos = inicio
    limite = 500 * 1024 * 1024
    while True:
        cab = entrada.read(8)
        if len(cab) < 8:
            break
        tam = int.from_bytes(cab[0:4], "big")
        tipo = cab[4:8]
        if not all(0x20 <= b <= 0x7E for b in tipo):   # ya no es texto -> no es un box valido
            break
        if tam == 1:                                    # tamaño de 64 bits
            tam64 = entrada.read(8)
            if len(tam64) < 8:
                break
            tam = int.from_bytes(tam64, "big")
        elif tam == 0:                                  # "hasta el final del archivo" (no sabemos donde)
            break
        if tam < 8:
            break
        pos_box_inicio = pos
        pos = pos_box_inicio + tam
        if pos - inicio > limite:
            break
        entrada.seek(pos)
    total = pos - inicio
    if total <= 8:
        return None
    entrada.seek(inicio)
    return entrada.read(total), "mp4", "videos"


def extraer_mkv_heuristico(entrada, inicio, max_size=150 * 1024 * 1024):
    """
    MKV no guarda un tamaño simple de leer como los anteriores (usa un
    formato mas complejo, EBML). Aqui se deja el metodo "heuristico":
    cortar cuando aparece la siguiente cabecera conocida. Es menos
    confiable -> revisa estos en ImHex si no abren bien.
    """
    entrada.seek(inicio + 4)
    buf = b""
    chunk = entrada.read(65536)
    total_leido = 0
    while chunk:
        buf += chunk
        total_leido += len(chunk)
        for _, cab in DISPARADORES:
            idx = buf.find(cab, 4)   # buscar despues del propio inicio
            if idx != -1:
                entrada.seek(inicio)
                return entrada.read(idx + 4), "mkv", "videos"
        if total_leido > max_size:
            break
        chunk = entrada.read(65536)
    entrada.seek(inicio)
    return entrada.read(min(total_leido + 4, max_size)), "mkv", "videos"


def extraer_por_footer(entrada, inicio, pie, ext, cat, max_size=100 * 1024 * 1024):
    entrada.seek(inicio)
    buf = b""
    chunk = entrada.read(65536)
    total_leido = 0
    while chunk:
        buf += chunk
        total_leido += len(chunk)
        idx = buf.find(pie)
        if idx != -1:
            return buf[: idx + len(pie)], ext, cat
        if total_leido > max_size:
            return None
        chunk = entrada.read(65536)
    return None


# ---------------------------------------------------------------------
#  Escaneo principal: igual espiritu que tu codigo (byte a byte + cola)
# ---------------------------------------------------------------------

def escanear(ruta_disco, carpeta_salida=None):
    if carpeta_salida is None:
        # Carpeta 'salida' siempre junto al script (no importa desde
        # donde se ejecute el comando en la terminal).
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
        carpeta_salida = os.path.join(carpeta_base, "salida")

    print(f"[i] Los archivos se guardaran en: {carpeta_salida}")

    for cat in ("videos", "imagenes", "otros"):
        os.makedirs(os.path.join(carpeta_salida, cat), exist_ok=True)
    contador = {"videos": 0, "imagenes": 0, "otros": 0}
    contador_ext = {}     # cuenta por extension, ej. {"jpg": 5, "mp4": 2, ...}
    mp3_excluidos = 0

    with open(ruta_disco, "rb") as entrada:
        Cache = deque(maxlen=MAXH)          # <-- tu "cola" original
        offset = 0
        bt = entrada.read(1)

        while bt:
            Cache.append(bt)
            ventana = b"".join(Cache)

            for tipo, cab in DISPARADORES:
                if ventana.endswith(cab):
                    inicio = offset - len(cab) + 1
                    resultado = None

                    if tipo == "mp3_excluir":
                        mp3_excluidos += 1
                        entrada.seek(offset + 1)   # no se extrae, seguimos avanzando
                        break

                    if tipo == "riff":
                        resultado = extraer_riff(entrada, inicio)
                    elif tipo == "mp4":
                        resultado = extraer_mp4(entrada, inicio)
                    elif tipo == "bmp":
                        resultado = extraer_bmp(entrada, inicio)
                    elif tipo == "mkv":
                        resultado = extraer_mkv_heuristico(entrada, inicio)
                    elif tipo.startswith("footer:"):
                        ext = tipo.split(":", 1)[1]
                        _, pie, cat = FOOTER_FORMATS[ext]
                        resultado = extraer_por_footer(entrada, inicio, pie, ext, cat)

                    if resultado:
                        datos, ext, cat = resultado
                        contador[cat] += 1
                        contador_ext[ext] = contador_ext.get(ext, 0) + 1
                        nombre = f"{cat}_{contador[cat]:04d}.{ext}"
                        ruta = os.path.join(carpeta_salida, cat, nombre)
                        with open(ruta, "wb") as out:
                            out.write(datos)

                        fin = inicio + len(datos)
                        entrada.seek(fin)      # saltamos justo al final de lo extraido
                        offset = fin - 1
                        Cache.clear()
                    else:
                        entrada.seek(offset + 1)   # falso positivo, seguimos donde ibamos
                    break

            offset += 1
            bt = entrada.read(1)

    # -------- generar resumen.txt en vez de ir imprimiendo cada archivo --------
    total = sum(contador_ext.values())
    lineas = [f"Total de archivos extraidos: {total}", ""]
    for ext, n in sorted(contador_ext.items()):
        lineas.append(f"{ext.capitalize()}: {n}")
    lineas.append("")
    lineas.append(f"Mp3 excluidos (no se extraen): {mp3_excluidos}")

    ruta_resumen = os.path.join(carpeta_salida, "resumen.txt")
    with open(ruta_resumen, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"[i] Listo. Resumen guardado en: {ruta_resumen}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python Extractor_Alo.py disk.img")
        sys.exit(1)
    escanear(sys.argv[1])
