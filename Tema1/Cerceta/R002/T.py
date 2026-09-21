from pathlib import Path

RutaOriginal = Path('.') / 'T.exe'
RutaParche = Path('.') / 'parche_T3.exe'
Desplazamiento = 0x248
Bn = b'\x90\x90\x90\x90\x90\x90'

if RutaOriginal.exists():
    with RutaOriginal.open('rb') as original:
        Buffer0 = original.read(Desplazamiento)
        original.read(6)
        Buffer1 = original.read()
        with RutaParche.open('wb') as parche:
            parche.write(Buffer0)
            parche.write(Bn)
            parche.write(Buffer1)
else:
    print("No se encontro: ", RutaOriginal.resolve())
    
    
 