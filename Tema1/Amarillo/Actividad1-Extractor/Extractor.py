import os

Cabeceras = {
    "FFD8FF": "jpg",
    "66747970": "mp4"
}

Final = {
    "FFD9": "jpg"
}

MínimoEntreFotos = 50000
with open('disk.img', 'rb') as entrada:
    Datos = entrada.read()
TamañoImagen = len(Datos)
os.makedirs('recuperados', exist_ok=True)

def TotalApariciones(FirmaBuscada):
    PosicionesEncontradas = []
    Inicio = 0
    while True:
        Posición = Datos.find(FirmaBuscada, Inicio)
        if Posición == -1:
            break
        PosicionesEncontradas.append(Posición)
        Inicio = Posición + 1   #Seguimos buscando después de la posición encontrada
    return PosicionesEncontradas

PosicionesJPEG = TotalApariciones(bytes.fromhex("FFD8FF"))
PosicionesValidas = []
for Posición in PosicionesJPEG:
    SigByte = Datos[Posición + 3]
    if SigByte == 0xE0 or SigByte == 0xE1:
        PosicionesValidas.append(Posición)
InicioFoto = []
for Posición in PosicionesValidas:
    Foto = (len(InicioFoto) == 0) or (Posición - InicioFoto[-1] > MínimoEntreFotos)
    if Foto:
        InicioFoto.append(Posición)

PosicionesMP4 = TotalApariciones(bytes.fromhex("66747970"))
InicioVideos = []
for Posición in PosicionesMP4:
    InicioVideos.append(Posición - 4)

Archivos = []
for Posición in InicioFoto:
    Archivos.append((Posición, "jpg"))
for Posición in InicioVideos:
    Archivos.append((Posición, "mp4"))
Archivos.sort()   # se ordena por posición (el primer valor del par)

Contador = 0
for Indice in range(len(Archivos)):
    Inicio, Tipo = Archivos[Indice]
    if Indice + 1 < len(Archivos):
        Límite, _ = Archivos[Indice + 1]
    else:
        Límite = TamañoImagen

    if Tipo == "jpg":
        Fin = Datos.rfind(bytes.fromhex("FFD9"), Inicio, Límite)
        if Fin == -1:
            continue   # no se encontró un final válido, se descarta
        Fin = Fin + 2  # se incluyen los 2 bytes de FF D9
    elif Tipo == "mp4":
        Fin = Límite    # Un MP4 no tiene una firma de "fin" como el JPEG, así que se usa el mismo límite que ya calculamos

    # ---------- Guardar cada archivo recuperado ----------
    Contador = Contador + 1
    NombreDeSalida = f"recuperados/Archivo_{Contador:03d}.{Tipo}"
    with open(NombreDeSalida, "wb") as salida:
        salida.write(Datos[Inicio:Fin])
    print(f"[+] {NombreDeSalida}  ({Fin - Inicio} bytes)")

print(f"\nTotal de archivos recuperados: {Contador}")