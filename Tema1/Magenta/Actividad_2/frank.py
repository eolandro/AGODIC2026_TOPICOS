from pathlib import Path
import difflib

RutaOriginal = Path('.')/'T.exe'
RutaParche = Path('.')/'T_parche.exe'


if RutaOriginal.exists():
    with RutaOriginal.open('rb') as original:
        BuffeR0 = original.read(0x249)
        BuffeR0 = BuffeR0 + b'\x84'
        # leer el byte a remplazar
        original.read(1)
        BuffeR1 = original.read()
        with RutaParche.open("wb") as parche:
            parche.write(BuffeR0)
            parche.write(BuffeR1)

else:
    print('No se encontro', RutaOriginal.resolve())


def hex_diff(original, parche):

    with open(original, 'rb') as f1, open(parche, 'rb') as f2:
        # Lee el contenido y conviértelo a texto hexadecimal
        hex1 = f1.read().hex()
        hex2 = f2.read().hex()

        ancho = 4
        lineas1 = [hex1[i:i+ancho] for i in range(0, len(hex1), ancho)]
        lineas2 = [hex2[i:i+ancho] for i in range(0, len(hex2), ancho)]

        diferencia = difflib.ndiff(lineas1, lineas2)

        # Filtramos para quedarnos solo con lo que empieza con '-' o '+'
        solo_cambios = [linea for linea in diferencia if linea.startswith(('-', '+'))]

        print("\n".join(solo_cambios))


hex_diff(RutaOriginal, RutaParche)


