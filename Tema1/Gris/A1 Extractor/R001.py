import os


FIRMAS = {
    b"\xFF\xD8\xFF": "jpg",
    b"ftyp": "mp4"
}

FIN_JPEG = b"\xFF\xD9"


def buscar_firma(datos, firma):
    posiciones = []
    inicio = 0

    while True:
        posicion = datos.find(firma, inicio)

        if posicion == -1:
            break

        posiciones.append(posicion)
        inicio = posicion + 1

    return posiciones


def validar_jpeg(datos, posicion):
    if posicion + 4 > len(datos):
        return False

    marcador = datos[posicion + 3]

    return marcador in (0xE0, 0xE1, 0xE2, 0xDB)


def detectar_archivos(datos):
    encontrados = []

    for posicion in buscar_firma(datos, b"\xFF\xD8\xFF"):
        if validar_jpeg(datos, posicion):
            encontrados.append((posicion, "jpg"))

    for posicion in buscar_firma(datos, b"ftyp"):
        inicio = posicion - 4

        if inicio >= 0:
            encontrados.append((inicio, "mp4"))

    return sorted(set(encontrados), key=lambda x: x[0])


def box_valido(datos, posicion):
    if posicion + 8 > len(datos):
        return False

    tipo = datos[posicion + 4:posicion + 8]

    return all(32 <= byte <= 126 for byte in tipo)


def tamaño_mp4(datos, inicio):
    posicion = inicio

    while posicion + 8 <= len(datos):

        tamaño = int.from_bytes(
            datos[posicion:posicion + 4],
            "big"
        )

        if not box_valido(datos, posicion):
            break

        if tamaño == 0:
            return len(datos) - inicio

        if tamaño == 1:
            if posicion + 16 > len(datos):
                break

            tamaño = int.from_bytes(
                datos[posicion + 8:posicion + 16],
                "big"
            )

            encabezado = 16
        else:
            encabezado = 8

        if tamaño < encabezado:
            break

        siguiente = posicion + tamaño

        if siguiente > len(datos):
            break

        posicion = siguiente

    return posicion - inicio


def obtener_final(datos, archivos, indice):
    inicio, tipo = archivos[indice]

    if tipo == "jpg":
        if indice + 1 < len(archivos):
            limite = archivos[indice + 1][0]
        else:
            limite = len(datos)

        final = datos.find(FIN_JPEG, inicio, limite)

        if final == -1:
            return None

        return final + 2

    if tipo == "mp4":
        tamaño = tamaño_mp4(datos, inicio)

        if tamaño <= 0:
            return None

        return inicio + tamaño

    return None


def main():

    print("======================================")
    print("       RECUPERANDO ARCHIVOS")
    print("======================================")

    ruta = input("\nEscribe la ruta de la imagen de memoria: ").strip()

    ruta = ruta.strip('"')

    if not os.path.isfile(ruta):
        print("\n[ERROR] El archivo no existe.")
        return

    carpeta = input(
        "Escribe la carpeta donde guardar los recuperados "
        "(Enter para usar 'recuperados'): "
    ).strip()

    if not carpeta:
        carpeta = "recuperados"

    os.makedirs(carpeta, exist_ok=True)

    with open(ruta, "rb") as archivo:
        datos = archivo.read()

    print(f"\nImagen analizada: {ruta}")
    print(f"Tamaño: {len(datos):,} bytes")

    archivos = detectar_archivos(datos)

    print(f"\nArchivos encontrados: {len(archivos)}")

    recuperados = 0

    for indice, (inicio, tipo) in enumerate(archivos):

        final = obtener_final(datos, archivos, indice)

        if final is None or final <= inicio:
            print(
                f"[!] No fue posible recuperar el "
                f"{tipo.upper()} en 0x{inicio:08X}"
            )
            continue

        contenido = datos[inicio:final]

        recuperados += 1

        nombre = os.path.join(
            carpeta,
            f"archivo_{recuperados:03d}.{tipo}"
        )

        with open(nombre, "wb") as salida:
            salida.write(contenido)

        print(
            f"[OK] {nombre} "
            f"({len(contenido):,} bytes)"
        )

    print("\n======================================")
    print(f"Archivos recuperados: {recuperados}")
    print(f"Resultados guardados en: {carpeta}")
    print("======================================")


if __name__ == "__main__":
    main()