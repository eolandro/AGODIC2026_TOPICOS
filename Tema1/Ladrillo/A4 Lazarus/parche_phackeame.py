from pathlib import Path

RutaOriginal = Path('.') / 'phackeame.exe'
RutaParche = Path('.') / 'phackeame_parche.exe'
Desplazamiento = 0x29666

if RutaOriginal.exists():
    with open(RutaOriginal, "rb") as original:
        Buffer0 = original.read(Desplazamiento)
        Buffer0 = Buffer0 + b'\x90\x90'
        original.read(2)         
        Buffer1 = original.read() 
        with RutaParche.open("wb") as parche:
            parche.write(Buffer0)
            parche.write(Buffer1)
    print(f"Parche generado: {RutaParche.resolve()}")
else:
    print('No se encontro: ', RutaOriginal.resolve())