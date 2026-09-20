from pathlib import Path

RutaOriginal = Path('.')/'T.exe'
RutaParche = Path('.')/'T_parche.exe'
Desplazamiento = 0x248
CantidadBytes = 6               # Cantidad de bytes a reemplazar (0F 85 13 00 00 00 -> 6 bytes)

if RutaOriginal.exists():
    with RutaOriginal.open("rb") as original:
        Buffer0 = original.read(Desplazamiento)
        Buffer0 += b'\x90' * CantidadBytes  #Los 6 bytes se reemplazan por NOP (0x90)
        original.read(CantidadBytes)    #Saltamos los bytes originales a reemplazar
        Buffer1 = original.read()   #Leer el resto del archivo
        with RutaParche.open("wb") as parche:
            parche.write(Buffer0)
            parche.write(Buffer1)
    print(f"Parche creado exitosamente: {RutaParche.resolve()}")
else:
    print("No se encontro: ", RutaOriginal.resolve())