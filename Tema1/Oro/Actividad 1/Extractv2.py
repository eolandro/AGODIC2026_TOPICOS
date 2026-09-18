CabeceraPrimaria = (b'\xEB\x58\x90\x6D\x6B\x66\x73\x2E\x66\x61\x74') # mkfs.fat

Cabeceras = {
    (b'\xFF\xD8\xFF', "jpg"),
    (b'\x89\x50\x4E\x47', "png"),
    (b'\x47\x49\x46\x38', "gif"),
    (b'\x00\x00\x00\x18', "mp4")
}

Finales = {
    "jpg": (b'\xFF\xD9'),
    "mp4": (b'\xD4\x17\x20\xE0'),
    "png": (b'\x49\x45\x4E\x44\xAE\x42\x60\x82'),
    "zip": (b'\x50\x4B\x05\x06')
}

Cache = []
Resultados = []

with open("disk.img", "rb") as entrada:
    archivo = entrada.read()
    if not archivo:
        print("Error: No se pudo leer el archivo disk.img")
        exit(1)

Apartirde = archivo.find(CabeceraPrimaria)
if Apartirde == -1:
    Apartirde = 0

Region = archivo[Apartirde:]


for cabecera, tipo in Cabeceras:
    i = 0
    while True:
        pos = Region.find(cabecera, i)
        if pos == -1:
            break
        Desplazamiento = pos + Apartirde
        print(f"\nEncontrado: {tipo} en desplazamiento (0x{Desplazamiento:08X})")
        Cache.append((tipo,cabecera,Desplazamiento))
        # print(Cache)
        i = pos + len(cabecera)
Cache.sort()


for data in Cache:
    tipo = data[0]
    cabecera = data[1]
    Inicio = data[2]
    # BytesFinales = Finales.get(tipo)
    try:
        BytesFinales = Finales[tipo]
    except KeyError:
        BytesFinales = None
    if BytesFinales:
        j = archivo.find(BytesFinales, Inicio + len(cabecera))
        if j != -1:
            Fin = j + len(BytesFinales)
            tamanno = Fin - Inicio
            # print(f" Final: {Fin}")
            Resultados.append((tipo, Inicio, Fin, tamanno))


for cont, data in enumerate(Resultados, 1):
    tipo, Inicio, Fin, tamanno = data
    NombreArchivo = f"archivo_{cont}.{tipo}"
    Contenido = archivo[Inicio:Fin]
    with open(NombreArchivo, "wb") as salida:
        salida.write(Contenido)
    print(f"\nGenerado: {NombreArchivo} ({tamanno} bytes)")