import sys
import random

def main():
    if len(sys.argv) < 2:
        print("Uso: python desmain.py <archivo.txt>")
        return
    nombre_archivo = sys.argv[1]
    try:
        with open(nombre_archivo, "rb") as archivo:
            byte = archivo.read(1)
            
            while byte:
                ivar2 = byte[0]                 
                ivar3 = random.randint(0, 255)  

                if ivar2 < ivar3:
                    print(f"{ivar3}-{ivar3 - ivar2}")
                elif ivar3 < ivar2:
                    print(f"{ivar2 - ivar3}+{ivar3}")
                elif ivar3 == ivar2:
                    print(f"{ivar2 - 1}+1")
                elif ivar2 == 0:
                    pass  

                byte = archivo.read(1)

    except FileNotFoundError:
        print(f"Error: No se pudo abrir el archivo '{nombre_archivo}'")

if __name__ == "__main__":
    main()