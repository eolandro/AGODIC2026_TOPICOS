from pathlib import Path

# Configuración adaptada a los archivos de tu carpeta
ORIGEN = Path("phackeame.exe")
DESTINO = Path("phackeame_python.exe")

OFFSET = 0x29666
BYTES_BUSCADOS = b"\x75\x1c"
BYTES_NUEVOS = b"\x90\x90"


def parchear_ejecutable():
    if not ORIGEN.exists():
        print(f"[-] Archivo no encontrado: {ORIGEN.name}")
        return

    # Leer todo el binario en memoria
    contenido = bytearray(ORIGEN.read_bytes())

    # Extraer los bytes en la posición objetivo
    bytes_actuales = contenido[OFFSET : OFFSET + len(BYTES_BUSCADOS)]
    print(f"[*] Bytes detectados en 0x{OFFSET:X}: {bytes_actuales.hex().upper()}")

    # Verificar coincidencia antes de modificar
    if bytes_actuales == BYTES_BUSCADOS:
        # Reemplazo directo en el buffer
        contenido[OFFSET : OFFSET + len(BYTES_BUSCADOS)] = BYTES_NUEVOS

        # Guardar en el nuevo archivo
        DESTINO.write_bytes(contenido)

        print("[+] Parche aplicado con éxito.")
        print(f"[+] Ejecutable generado: {DESTINO.name}")
    else:
        print("[-] Los bytes encontrados no coinciden con la firma esperada.")


if __name__ == "__main__":
    parchear_ejecutable()