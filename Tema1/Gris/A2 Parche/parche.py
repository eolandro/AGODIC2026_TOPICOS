"""
Parche automatico para el sistema Legacy
Practica: Debugger - R002

Este script lee el ejecutable original y le aplica el mismo cambio
que se hizo manualmente con el depurador: convierte la instruccion
JNE (que valida el Serial Key) en NOPs, para que el programa
siempre acepte cualquier clave.

NOTA IMPORTANTE: este script no genera el .exe para entregarlo,
es solo la prueba de que el proceso se puede automatizar.
NO se debe entregar ningun ejecutable, solo este codigo fuente.
"""

# ---------- CONFIGURACION ----------
ARCHIVO_ORIGINAL = "legacy.exe"
ARCHIVO_NUEVO = "legacy_parche_generado.exe"

OFFSET_DEL_SALTO = 0x253       # posicion en el ARCHIVO (no en memoria) donde empieza el JNE
CANTIDAD_DE_BYTES = 6          # el JNE ocupa 6 bytes: 0F 85 13 00 00 00

BYTES_ESPERADOS = bytes.fromhex("0F8513000000")  # lo que debe haber ANTES de parchar
BYTES_NUEVOS = b"\x90" * CANTIDAD_DE_BYTES        # NOP x 6


def main():
    print("----------- PARCHE LEGACY -----------")

    # 1. Leer el archivo original completo
    with open(ARCHIVO_ORIGINAL, "rb") as f:
        contenido_original = f.read()

    print(f"El archivo original '{ARCHIVO_ORIGINAL}' tiene {len(contenido_original)} bytes")

    # 2. Separar el archivo en 3 partes: antes, el salto, y despues
    parte_1 = contenido_original[:OFFSET_DEL_SALTO]
    parte_del_salto = contenido_original[OFFSET_DEL_SALTO: OFFSET_DEL_SALTO + CANTIDAD_DE_BYTES]
    parte_2 = contenido_original[OFFSET_DEL_SALTO + CANTIDAD_DE_BYTES:]

    print("Bytes originales encontrados en el offset:", parte_del_salto.hex())

    # 3. Verificacion de seguridad: confirmar que son los bytes que esperamos
    if parte_del_salto != BYTES_ESPERADOS:
        print("¡ADVERTENCIA! Los bytes no coinciden con los esperados.")
        print("Se esperaba:", BYTES_ESPERADOS.hex(), "pero se encontro:", parte_del_salto.hex())
        print("Revisa el offset, puede que el ejecutable sea distinto al analizado.")
        return

    print("Verificacion correcta: coincide con la instruccion JNE esperada.")

    # 4. Construir el nuevo contenido con los NOPs en vez del salto
    contenido_nuevo = parte_1 + BYTES_NUEVOS + parte_2

    # 5. Guardar el archivo parchado
    with open(ARCHIVO_NUEVO, "wb") as f:
        f.write(contenido_nuevo)

    print(f"\nEl parche se aplico correctamente.")
    print(f"Nuevo archivo generado: {ARCHIVO_NUEVO}")


if __name__ == "__main__":
    main()
