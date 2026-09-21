import os
import re
import struct
import sys

def recuperar_jpeg(datos, carpeta):
    print("\n[1] Buscando fotografías JPEG...")

    firmas = [b"\xFF\xD8\xFF\xE1", b"\xFF\xD8\xFF\xE0"]

    encontrados = []
    for firma in firmas:
        encontrados += [m.start() for m in re.finditer(re.escape(firma), datos)]
    encontrados = sorted(set(encontrados))
    numero = 0

    for inicio in encontrados:
        final = datos.find(b"\xFF\xD9", inicio + 4)

        if final == -1:
            print(f"  [?] JPEG en {inicio}: no se encontró FF D9")
            continue

        final += 2
        contenido = datos[inicio:final]

        if len(contenido) < 1000:
            continue

        numero += 1
        nombre = os.path.join(carpeta, f"foto_{numero:03}.jpg")

        with open(nombre, "wb") as salida:
            salida.write(contenido)

        print(
            f"  [+] Foto encontrada: {nombre} "
            f"(offset {inicio}, {len(contenido)} bytes)"
        )

    print(f"  Total de candidatos JPEG: {numero}")

def leer_box(datos, posicion):
    """Lee un box/atom MP4."""
    if posicion + 8 > len(datos):
        return None

    tam = struct.unpack(">I", datos[posicion:posicion+4])[0]
    tipo = datos[posicion+4:posicion+8]

    if tam == 1:
        if posicion + 16 > len(datos):
            return None
        tam = struct.unpack(">Q", datos[posicion+8:posicion+16])[0]

    elif tam == 0:
        tam = len(datos) - posicion

    if tam < 8:
        return None

    if posicion + tam > len(datos):
        return None

    return tam, tipo

def recuperar_mp4(datos, carpeta):
    print("\n[2] Buscando videos MP4...")

    posiciones = [m.start() for m in re.finditer(b"ftyp", datos)]
    numero = 0

    for ftyp in posiciones:
        inicio = ftyp - 4

        if inicio < 0:
            continue

        box = leer_box(datos, inicio)

        if box is None:
            continue

        tam, tipo = box

        if tipo != b"ftyp":
            continue

        posicion = inicio
        final = inicio

        while posicion < len(datos):
            box = leer_box(datos, posicion)

            if box is None:
                break

            tam, tipo = box

            tipos_validos = {
                b"ftyp", b"moov", b"mdat", b"free", b"skip",
                b"wide", b"uuid", b"pnot", b"udta", b"meta"
            }

            if tipo not in tipos_validos:
                break

            final = posicion + tam
            posicion = final

        if final - inicio < 10000:
            continue

        numero += 1
        nombre = os.path.join(carpeta, f"video_{numero:03}.mp4")

        with open(nombre, "wb") as salida:
            salida.write(datos[inicio:final])

        print(
            f"  [+] Video encontrado: {nombre} "
            f"(offset {inicio}, {final-inicio} bytes)"
        )

    print(f"  Total de candidatos MP4: {numero}")

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python recuperador_facil.py disk.img")
        return

    ruta = sys.argv[1]

    if not os.path.exists(ruta):
        print("ERROR: no existe la imagen:", ruta)
        return

    print("     RECUPERADOR FORENSE SIMPLE")
    print("Imagen:", ruta)

    print("\nLeyendo imagen...")
    with open(ruta, "rb") as archivo:
        datos = archivo.read()

    print("Tamaño:", len(datos), "bytes")

    carpeta = "recuperados"
    os.makedirs(carpeta, exist_ok=True)

    recuperar_jpeg(datos, carpeta)
    recuperar_mp4(datos, carpeta)

    print("\n")
    print("Proceso terminado.")
    print("Revisa la carpeta:", carpeta)

if __name__ == "__main__":
    main()
