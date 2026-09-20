import sys
import random
import time


def main():
    if len(sys.argv) < 2:
        print("Usage:\nsumnotransfer archivont", end="")
        return 1

    random.seed(int(time.time()))

    try:
        archivo = open(sys.argv[1], "rb")  # "rb" confirmado en el binario
    except IOError:
        print("No se puede abrir el archivont")
        return 1

    with archivo:
        while True:
            byte = archivo.read(1)
            if byte == b"":  # EOF
                break

            caracter = byte[0]
            numero_aleatorio = random.randint(0, 255)  # rand() % 256

            if caracter < numero_aleatorio:
                print(f"{numero_aleatorio}-{numero_aleatorio - caracter}")

            if numero_aleatorio < caracter:
                print(f"{caracter - numero_aleatorio}+{numero_aleatorio}")

            if caracter == 0:
                print("1-1")  # <- DAT_00402050 confirmado, NO es "0"

            if numero_aleatorio == caracter:
                print(f"{caracter - 1}+1")

    return 0


main()