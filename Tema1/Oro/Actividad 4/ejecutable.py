"""
import os
import random
import sys


def procesar_archivo(ruta_archivo: str) -> int:
    try:
        with open(ruta_archivo, "rb") as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break

                ivar2 = byte[0]
                ivar3 = random.randint(0, 255)

                if ivar2 < ivar3:
                    print(f"{ivar3}-{ivar3 - ivar2}")

                if ivar3 < ivar2:
                    print(f"{ivar2 - ivar3}+{ivar3}")

                if ivar2 == 0:
                    print("1-1")

                if ivar3 == ivar2:
                    print(f"{ivar2 - 1}+1")

        return 0

    except (FileNotFoundError, PermissionError):
        print(f"No se puede abrir el archivo: {ruta_archivo}\n", end="")
        return 1


def main():
    if len(sys.argv) >= 2:
        ruta = sys.argv[1]
    else:
        ruta = input("Ingresa el nombre o ruta del archivo .txt: ").strip().strip('"')

    # Si la ruta no es absoluta, la busca en la misma carpeta donde reside este script
    if not os.path.isabs(ruta):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_absoluta = os.path.join(base_dir, ruta)
        
        # Si existe junto al script, usa esa ruta; de lo contrario mantiene la original
        if os.path.exists(ruta_absoluta):
            ruta = ruta_absoluta

    codigo_salida = procesar_archivo(ruta)
    sys.exit(codigo_salida)


if __name__ == "__main__":
    main()
    
"""
import random
import sys
import time


def procesar_archivo(ruta_archivo: str) -> int:
    try:
        f = open(ruta_archivo, "rb")
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        # Equivalente a: printf(s_No_se_puede_abrir_el_archivo..., 0)
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
    # Equivalente a: if (param_1 < 2) -> imprime uso y sale con código 1
    if len(sys.argv) < 2:
        print("Usage: sumnotransfer archivo")
        sys.exit(1)

    # Equivalente a: srand((uint)time(NULL))
    random.seed(int(time.time()))

    ruta = sys.argv[1]

    codigo_salida = procesar_archivo(ruta)
    sys.exit(codigo_salida)


if __name__ == "__main__":
    main()