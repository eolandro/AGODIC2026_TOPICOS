from pathlib import Path

RutaOriginal = Path(".") / "T.exe"
RutaParche = Path(".") / "T_parche.exe"
Desplazamiento = 0x245

if RutaOriginal.exists():
    with RutaOriginal.open("rb") as original:
        Buffer0 = original.read(Desplazamiento)
        Buffer0 = Buffer0 + b"\x39\xc0\x90"
        original.read(3)
        Buffer1 = original.read()
        with RutaParche.open("wb") as parche:
            parche.write(Buffer0)
            parche.write(Buffer1)
            print("You Cooked")
else:
    print("Archivon't: ", RutaOriginal.resolve())
