'''
Este archivo permite parchear el ejecutable de phackeame para poder presionar
el boton sin confirmacion de la api con las credenciales que sea
'''
def parchar_jne_a_nops(ruta_entrada, ruta_salida):
    try:
        with open(ruta_entrada, "rb") as f:
            contenido = f.read()

        #cadema de bytes que debe reemplazar en el ejecutable
        bytes_originales = b"\x81\x7D\xE4\xC8\x00\x00\x00\x75\x1C"

        #Cadena de bytes por los que se van a reemplazar
        bytes_parche = b"\x81\x7D\xE4\xC8\x00\x00\x00\x90\x90"

        # 4. Buscar y reemplazar la secuencia de bytes en el binario
        if bytes_originales in contenido:
            contenido_modificado = contenido.replace(bytes_originales, bytes_parche, 1)

            # 5. Guardar el resultado en el nuevo ejecutable parchado
            with open(ruta_salida, "wb") as f:
                f.write(contenido_modificado)

            print(f"¡Éxito! El archivo parchado se ha generado correctamente como: {ruta_salida}")
        else:
            print("Error: No se encontró la secuencia de bytes exacta en el binario.")

    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo: {e}")

parchar_jne_a_nops("phackeame.exe", "phackeame_parchado.exe")