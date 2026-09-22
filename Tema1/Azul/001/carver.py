from pathlib import Path
import struct
import sys


JPEG_HEADER = b"\xff\xd8\xff"
JPEG_FOOTER = b"\xff\xd9"
MP4_TYPE = b"ftyp"


def buscar_todas(datos, firma):
    posiciones = []
    inicio = 0

    while True:
        posicion = datos.find(firma, inicio)

        if posicion == -1:
            break

        posiciones.append(posicion)
        inicio = posicion + 1

    return posiciones


def nombre_sin_extension(ruta):
    return Path(ruta).stem


def extraer_jpegs(datos, carpeta_salida, base):
    resultados = []
    inicios = buscar_todas(datos, JPEG_HEADER)

    for numero, inicio in enumerate(inicios, start=1):
        final = datos.find(JPEG_FOOTER, inicio + len(JPEG_HEADER))

        if final == -1:
            print(f"[!] JPEG incompleto en offset {inicio:#x}")
            continue

        final += len(JPEG_FOOTER)
        contenido = datos[inicio:final]

        if len(contenido) < 100:
            print(f"[!] JPEG demasiado pequeño en offset {inicio:#x}")
            continue

        salida = carpeta_salida / f"{base}_foto_{numero:03d}.jpg"
        salida.write_bytes(contenido)

        resultados.append({
            "tipo": "JPEG",
            "inicio": inicio,
            "final": final - 1,
            "tamano": len(contenido),
            "archivo": salida.name
        })

        print(
            f"[+] JPEG recuperado: {salida.name} | "
            f"inicio={inicio:#x} | final={(final - 1):#x} | "
            f"tamano={len(contenido)} bytes"
        )

    return resultados


def leer_uint32_be(datos, posicion):
    if posicion + 4 > len(datos):
        return None

    return struct.unpack(">I", datos[posicion:posicion + 4])[0]


def extraer_cajas_mp4(datos, inicio):
    posicion = inicio
    cajas = []

    while posicion + 8 <= len(datos):
        tamano = leer_uint32_be(datos, posicion)
        tipo = datos[posicion + 4:posicion + 8]

        if tamano is None:
            return None

        encabezado = 8

        if tamano == 1:
            if posicion + 16 > len(datos):
                return None

            tamano = struct.unpack(
                ">Q",
                datos[posicion + 8:posicion + 16]
            )[0]

            encabezado = 16

        elif tamano == 0:
            tamano = len(datos) - posicion

        if tamano < encabezado:
            return None

        final_caja = posicion + tamano

        if final_caja > len(datos):
            return None

        cajas.append({
            "inicio": posicion,
            "final": final_caja,
            "tipo": tipo.decode("ascii", errors="replace"),
            "tamano": tamano
        })

        posicion = final_caja

        if len(cajas) > 10000:
            return None

        if tipo in (b"moov", b"mdat"):
            if tipo == b"moov":
                hay_moov = True
            else:
                hay_mdat = True

            if "hay_moov" in locals() and "hay_mdat" in locals():
                return cajas

    return None


def extraer_mp4s(datos, carpeta_salida, base):
    resultados = []
    encontrados = buscar_todas(datos, MP4_TYPE)

    numero = 1
    offsets_revisados = set()

    for posicion_ftyp in encontrados:
        inicio = posicion_ftyp - 4

        if inicio < 0 or inicio in offsets_revisados:
            continue

        offsets_revisados.add(inicio)

        tamano_ftyp = leer_uint32_be(datos, inicio)

        if tamano_ftyp is None or tamano_ftyp < 8:
            continue

        cajas = extraer_cajas_mp4(datos, inicio)

        if not cajas:
            print(f"[!] Posible MP4 inválido en offset {inicio:#x}")
            continue

        tipos = [caja["tipo"] for caja in cajas]

        if "ftyp" not in tipos:
            continue

        final = cajas[-1]["final"]
        contenido = datos[inicio:final]

        if len(contenido) < 100:
            continue

        salida = carpeta_salida / f"{base}_video_{numero:03d}.mp4"
        salida.write_bytes(contenido)

        resultados.append({
            "tipo": "MP4",
            "inicio": inicio,
            "final": final - 1,
            "tamano": len(contenido),
            "cajas": tipos,
            "archivo": salida.name
        })

        print(
            f"[+] MP4 recuperado: {salida.name} | "
            f"inicio={inicio:#x} | final={(final - 1):#x} | "
            f"tamano={len(contenido)} bytes | cajas={tipos}"
        )

        numero += 1

    return resultados


def guardar_reporte(carpeta_salida, resultados):
    reporte = carpeta_salida / "reporte_carving.txt"

    with reporte.open("w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE FILE CARVING\n")
        archivo.write("=" * 60 + "\n\n")

        for resultado in resultados:
            archivo.write(f"Tipo: {resultado['tipo']}\n")
            archivo.write(f"Archivo: {resultado['archivo']}\n")
            archivo.write(f"Inicio: {resultado['inicio']} ")
            archivo.write(f"({resultado['inicio']:#x})\n")
            archivo.write(f"Final: {resultado['final']} ")
            archivo.write(f"({resultado['final']:#x})\n")
            archivo.write(f"Tamaño: {resultado['tamano']} bytes\n")

            if "cajas" in resultado:
                archivo.write(
                    "Cajas MP4: " +
                    ", ".join(resultado["cajas"]) +
                    "\n"
                )

            archivo.write("\n")

    print(f"[+] Reporte guardado en: {reporte}")


def main():
    if len(sys.argv) != 2:
        print("Uso:")
        print("  python carver.py disk.img")
        sys.exit(1)

    ruta_imagen = Path(sys.argv[1])

    if not ruta_imagen.is_file():
        print(f"[!] No existe la imagen: {ruta_imagen}")
        sys.exit(1)

    carpeta_salida = Path("recuperados")
    carpeta_salida.mkdir(exist_ok=True)

    print(f"[*] Analizando: {ruta_imagen}")
    print(f"[*] Tamaño: {ruta_imagen.stat().st_size} bytes")

    datos = ruta_imagen.read_bytes()
    base = nombre_sin_extension(ruta_imagen)

    resultados = []

    resultados.extend(
        extraer_jpegs(datos, carpeta_salida, base)
    )

    resultados.extend(
        extraer_mp4s(datos, carpeta_salida, base)
    )

    guardar_reporte(carpeta_salida, resultados)

    print()
    print(f"[*] Archivos recuperados: {len(resultados)}")


if __name__ == "__main__":
    main()