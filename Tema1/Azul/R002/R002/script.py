archivo = "T.exe"
parche = "prueba_parche.exe"

posicion = 0x248

with open(archivo, "rb") as archivo:
    datos = bytearray(archivo.read())

datos[posicion + 1] = 0x84

with open(parche, "wb") as archivo:
    archivo.write(datos)

print("\nParche aplicado correctamente")
print(f"\nArchivo creado:", {parche})



