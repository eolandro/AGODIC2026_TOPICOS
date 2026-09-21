from pathlib import Path
import shutil
import sys

ARCHIVO_ORIGINAL = Path("T.exe")
ARCHIVO_PARCHADO = Path("T_parche.exe")

OFFSET       = 0x248
BYTES_ORIG   = bytes.fromhex("0F 85 13 00 00 00")
BYTES_PARCHE = b"\x90" * len(BYTES_ORIG)

def main() -> None:
    if not ARCHIVO_ORIGINAL.exists():
        sys.exit(f"[X] No se encontro el original: {ARCHIVO_ORIGINAL.resolve()}")

    datos = bytearray(ARCHIVO_ORIGINAL.read_bytes())

    if OFFSET + len(BYTES_ORIG) > len(datos):
        sys.exit(f"[X] El offset 0x{OFFSET:X} esta fuera del archivo.")

    actuales = bytes(datos[OFFSET:OFFSET + len(BYTES_ORIG)])

    if actuales == BYTES_PARCHE:
        sys.exit("[!] El binario ya parece estar parchado (NOP). No hay nada que hacer.")

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
    print(f"     Cambio        : {BYTES_ORIG.hex(' ')} (JNE)")
    print(f"                     -> {BYTES_PARCHE.hex(' ')} (NOP x{len(BYTES_PARCHE)})")
    print(f"     Respaldo      : {respaldo.resolve()}")
    print(f"     Archivo nuevo : {ARCHIVO_PARCHADO.resolve()}")


if __name__ == "__main__":
    main()
