from pathlib import Path

RutaOriginal = Path('.') / 'T.exe'
RutaParche = Path('.') / 'T_parche.exe'
Desplazamiento = 0x24A  

if RutaOriginal.exists():
    with open(RutaOriginal, "rb") as original:
        Buffer0 = original.read(Desplazamiento)
        Buffer0 = Buffer0 + b'\x00'  
        original.read(1)              
        Buffer1 = original.read()
        with RutaParche.open("wb") as parche:
            parche.write(Buffer0)
            parche.write(Buffer1)
    print(f"Parche generado: {RutaParche.resolve()}")
else:
    print('No se encontro: ', RutaOriginal.resolve())
