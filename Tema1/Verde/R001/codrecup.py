import os
import sys

Imagen = sys.argv[1] if len(sys.argv) > 1 else 'disk.img'
TamañoSector = 512        

with open(Imagen, 'rb') as entrada:
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
        Inicio = Posición + 1
    return PosicionesEncontradas

def FinalJPEG(Inicio):
    Pos = Inicio + 2                                 
    while Pos + 4 <= TamañoImagen:
        if Datos[Pos] != 0xFF:
            return -1                                 
        Marcador = Datos[Pos + 1]
        if Marcador == 0xFF:                          
            Pos += 1
            continue
        if Marcador == 0xD9:                          
            return Pos + 2
        if Marcador == 0x01 or 0xD0 <= Marcador <= 0xD8:  
            Pos += 2
            continue
        Largo = int.from_bytes(Datos[Pos + 2:Pos + 4], 'big')
        Pos = Pos + 2 + Largo                         
        if Marcador == 0xDA:                         
            while True:                             
                Pos = Datos.find(b'\xFF', Pos)
                if Pos == -1 or Pos + 1 >= TamañoImagen:
                    return -1
                Siguiente = Datos[Pos + 1]
                if Siguiente == 0x00 or 0xD0 <= Siguiente <= 0xD7:
                    Pos += 2                        
                elif Siguiente == 0xFF:
                    Pos += 1
                else:
                    break
    return -1

TiposCaja = [b'ftyp', b'moov', b'mdat', b'free', b'skip', b'wide', b'moof', b'uuid', b'meta']


def FinalMP4(Inicio):
    Pos = Inicio
    while Pos + 8 <= TamañoImagen:
        Tamaño = int.from_bytes(Datos[Pos:Pos + 4], 'big')
        Tipo = Datos[Pos + 4:Pos + 8]
        if Tipo not in TiposCaja:
            break                                    
        if Tamaño == 1:
            Tamaño = int.from_bytes(Datos[Pos + 8:Pos + 16], 'big')
        if Tamaño < 8:
            break
        Pos = Pos + Tamaño
    if Pos > TamañoImagen or Pos == Inicio:
        return -1
    return Pos


def FinalPNG(Inicio):
    Pos = Datos.find(b'IEND\xAE\x42\x60\x82', Inicio)
    return -1 if Pos == -1 else Pos + 8

Candidatos = []
for Posición in TotalApariciones(bytes.fromhex("FFD8FF")):
    if Posición % TamañoSector == 0 and Datos[Posición + 3] in (0xE0, 0xE1):
        Candidatos.append((Posición, "jpg"))
for Posición in TotalApariciones(b'ftyp'):          
    if (Posición - 4) % TamañoSector == 0:
        Candidatos.append((Posición - 4, "mp4"))
for Posición in TotalApariciones(bytes.fromhex("89504E470D0A1A0A")):
    if Posición % TamañoSector == 0:
        Candidatos.append((Posición, "png"))
Candidatos.sort()

Contador = 0
FinAnterior = 0
for Inicio, Tipo in Candidatos:
    if Inicio < FinAnterior:
        continue                                     
    if Tipo == "jpg":
        Fin = FinalJPEG(Inicio)
    elif Tipo == "mp4":
        Fin = FinalMP4(Inicio)
    else:
        Fin = FinalPNG(Inicio)
    if Fin == -1:
        continue                                      

    Contador = Contador + 1
    NombreDeSalida = f"recuperados/Archivo_{Contador:03d}.{Tipo}"
    with open(NombreDeSalida, "wb") as salida:
        salida.write(Datos[Inicio:Fin])
    print(f"[+] {NombreDeSalida}  inicio=0x{Inicio:08X}  fin=0x{Fin:08X}  ({Fin - Inicio} bytes)")
    FinAnterior = Fin

print(f"\nTotal de archivos recuperados: {Contador}")
