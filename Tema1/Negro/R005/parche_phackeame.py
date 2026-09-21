

from pathlib import Path
import shutil
import sys


ARCHIVO_ORIGINAL = Path("phackeame.exe")
ARCHIVO_PARCHADO = Path("phackeame_parche.exe")

OFFSET       = 0x29666
BYTES_ORIG   = b"\x75\x1c"
BYTES_PARCHE = b"\x90\x90"

def main() -> None:

    if not ARCHIVO_ORIGINAL.exists():
        sys.exit(f"[X] No se encontro el original: {ARCHIVO_ORIGINAL.resolve()}")

    datos = bytearray(ARCHIVO_ORIGINAL.read_bytes())


    if OFFSET + len(BYTES_ORIG) > len(datos):
        sys.exit(f"[X] El offset 0x{OFFSET:X} esta fuera del archivo.")

    actuales = bytes(datos[OFFSET:OFFSET + len(BYTES_ORIG)])


    if actuales == BYTES_PARCHE:
        sys.exit("[!] El binario ya parece estar parchado (90 90). No hay nada que hacer.")


    if actuales != BYTES_ORIG:
        sys.exit(
            "[X] Los bytes en el offset no coinciden con lo esperado.\n"
            f"    Esperado  : {BYTES_ORIG.hex(' ')}\n"
            f"    Encontrado: {actuales.hex(' ')}\n"
            "    Verifica que sea el binario correcto (mismo SHA256)."
        )


    respaldo = Path(str(ARCHIVO_ORIGINAL) + ".bak")
    if not respaldo.exists():
        shutil.copy2(ARCHIVO_ORIGINAL, respaldo)


    datos[OFFSET:OFFSET + len(BYTES_PARCHE)] = BYTES_PARCHE
    ARCHIVO_PARCHADO.write_bytes(datos)


    print("[OK] Parche aplicado correctamente.")
    print(f"     Offset        : 0x{OFFSET:X}")
    print(f"     Cambio        : {BYTES_ORIG.hex(' ')} (JNE)  ->  {BYTES_PARCHE.hex(' ')} (NOP NOP)")
    print(f"     Respaldo      : {respaldo.resolve()}")
    print(f"     Archivo nuevo : {ARCHIVO_PARCHADO.resolve()}")


if __name__ == "__main__":
    main()
