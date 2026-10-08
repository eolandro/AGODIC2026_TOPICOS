import sys
from pathlib import Path

ARCHIVO_ENTRADA = Path("phackeame.exe")
ARCHIVO_SALIDA = Path("R5phackeame_gris.exe")

OFFSET = 0x29666
ESPERADO = bytes([0x75, 0x1C])   # salto condicional original
NUEVO = bytes([0x90, 0x90])      # dos NOP


def formato_hex(datos: bytes) -> str:
    return " ".join(f"{b:02x}" for b in datos)


def aplicar_parche(datos: bytearray, offset: int, esperado: bytes, nuevo: bytes) -> None:
    fin = offset + len(esperado)

    if fin > len(datos):
        raise ValueError("El offset queda fuera del tamaño del archivo.")

    actual = bytes(datos[offset:fin])
    if actual != esperado:
        raise ValueError(
            f"Bytes inesperados en 0x{offset:X}: encontré {formato_hex(actual)}, "
            f"esperaba {formato_hex(esperado)}."
        )

    datos[offset:fin] = nuevo


def main() -> int:
    if not ARCHIVO_ENTRADA.is_file():
        print(f"[!] No existe el archivo: {ARCHIVO_ENTRADA.resolve()}")
        return 1

    contenido = bytearray(ARCHIVO_ENTRADA.read_bytes())

    try:
        aplicar_parche(contenido, OFFSET, ESPERADO, NUEVO)
    except ValueError as error:
        print(f"[!] {error}")
        return 1

    ARCHIVO_SALIDA.write_bytes(contenido)

    print("[+] Parche aplicado con éxito")
    print(f"    Offset : 0x{OFFSET:X}")
    print(f"    Cambio : {formato_hex(ESPERADO)} -> {formato_hex(NUEVO)}")
    print(f"    Salida : {ARCHIVO_SALIDA.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
