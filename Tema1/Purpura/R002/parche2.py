from pathlib import Path

ruta_original = Path("hackame0.exe")
ruta_salida = Path("hackame0_parchado_script.exe")
offset_parche = 0x210
bytes_nuevos = b"\x39\xC0\x90"

if not ruta_original.exists():
    raise FileNotFoundError("No se encontró el ejecutable original.")

with ruta_original.open("rb") as archivo:
    inicio = archivo.read(offset_parche)
    archivo.read(len(bytes_nuevos))
    resto = archivo.read()

with ruta_salida.open("wb") as archivo:
    archivo.write(inicio)
    archivo.write(bytes_nuevos)
    archivo.write(resto)

print("Parche aplicado correctamente.")