archivo = "phackeame.exe"
salida = "phackeame_parche2.exe"
with open(archivo, "rb") as f:
    datos = bytearray(f.read())
if datos[0x29666:0x29668] == b"\x75\x1c":
    datos[0x29666:0x29668] = b"\x90\x90"
    with open(salida, "wb") as f:
        f.write(datos)
    print("Parche realizado")
else:
    print("No se encontraron los bytes")
