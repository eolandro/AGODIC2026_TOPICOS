# EQUIPO VERDE 
nombre_archivo_original = "T.exe"
nombre_archivo_nuevo = "T_PVerde.exe"
posicion_del_salto = 0x248
cantidad_de_bytes = 6

archivo = open(nombre_archivo_original, "rb")
contenido_original = archivo.read()
archivo.close()
print("----------- E Q U I P O   V E R D E -----------")
print("\n El archivo original",nombre_archivo_original, "tiene", len(contenido_original), "bytes")

parte_1 = contenido_original[0:posicion_del_salto]
parte_del_salto = contenido_original[posicion_del_salto: posicion_del_salto + cantidad_de_bytes]
parte_2 = contenido_original[posicion_del_salto + cantidad_de_bytes:]

print(" Bytes originales del salto:", parte_del_salto.hex())

nuevos_bytes = b"\x90" * cantidad_de_bytes
contenido_nuevo = parte_1 + nuevos_bytes + parte_2

archivo_nuevo = open(nombre_archivo_nuevo, "wb")
archivo_nuevo.write(contenido_nuevo)
archivo_nuevo.close()

print("\n El parche se aplico correctamente")
print(" Nombre del parche:", nombre_archivo_nuevo)
