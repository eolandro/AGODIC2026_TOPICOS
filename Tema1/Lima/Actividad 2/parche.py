from pathlib import Path

DirectorioScript = Path(__file__).parent

RutaOriginal = DirectorioScript / 'T.exe'
RutaParche = DirectorioScript / 'T_parche.exe'
Desplazamiento = 0x248

if RutaOriginal.exists():
    with RutaOriginal.open("rb") as original:
        Buffer0 = original.read(Desplazamiento)
        Buffer0 = Buffer0 + b'\x0F\x84' 
        original.read(2) 
        Buffer1 = original.read()
        
        with RutaParche.open('wb') as parche:
            parche.write(Buffer0)
            parche.write(Buffer1)
        print("Parche generado: T_parche.exe en", DirectorioScript)
else:
    print('No se encontró: ', RutaOriginal.resolve())