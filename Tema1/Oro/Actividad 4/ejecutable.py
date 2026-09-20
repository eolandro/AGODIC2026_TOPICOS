import random
import sys
import time


def procesar_archivo(ruta_archivo: str) -> int:
    try:
        f = open(ruta_archivo, "rb")
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        print("No se puede abrir el archivo")
        return 1
    with f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            ivar2 = byte[0]
            ivar3 = random.randint(0, 255)  # equivalente a rand() % 0x100
            if ivar2 < ivar3:
                print(f"{ivar3}-{ivar3 - ivar2}")
            if ivar3 < ivar2:
                print(f"{ivar2 - ivar3}+{ivar3}")
            if ivar2 == 0:
                print("1-1")
            if ivar3 == ivar2:
                print(f"{ivar2 - 1}+1")
    return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: sumnotransfer archivo")
        sys.exit(1)

    random.seed(int(time.time()))
    ruta = sys.argv[1]
    codigo_salida = procesar_archivo(ruta)
    sys.exit(codigo_salida)
