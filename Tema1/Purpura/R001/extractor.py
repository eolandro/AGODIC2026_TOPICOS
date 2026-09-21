from pathlib import Path
CABECERAS_HEX = {'jpeg': 'FFD8FFE1', 'mp4': '00000018667479706D703432'}
FINALES_HEX = {'jpeg': 'FFD9', 'mp4': '6D646174'}

def hex_a_bytes(cadena_hex: str) -> bytes:
    return bytes.fromhex(cadena_hex)
CABECERA_JPEG = hex_a_bytes(CABECERAS_HEX['jpeg'])
CABECERA_MP4 = hex_a_bytes(CABECERAS_HEX['mp4'])
TAM_VENTANA = max(len(CABECERA_JPEG), len(CABECERA_MP4))

def extraer_jpeg(entrada, ruta_salida: Path) -> None:
    with ruta_salida.open('wb') as salida:
        salida.write(CABECERA_JPEG)
        tam_bytes = entrada.read(2)
        if len(tam_bytes) < 2:
            return
        salida.write(tam_bytes)
        tam_segmento = tam_bytes[0] * 256 + tam_bytes[1]
        salida.write(entrada.read(tam_segmento - 2))
        anterior = None
        while True:
            byte = entrada.read(1)
            if byte == b'':
                break
            salida.write(byte)
            if anterior == b'\xff' and byte == b'\xd9':
                break
            anterior = byte

def extraer_mp4(entrada, ruta_salida: Path) -> None:
    with ruta_salida.open('wb') as salida:
        salida.write(CABECERA_MP4)
        salida.write(entrada.read(12))
        while True:
            tam_bytes = entrada.read(4)
            tipo_bytes = entrada.read(4)
            if len(tam_bytes) < 4 or len(tipo_bytes) < 4:
                break
            salida.write(tam_bytes)
            salida.write(tipo_bytes)
            tam_caja = int.from_bytes(tam_bytes, byteorder='big')
            if tam_caja == 1:
                tam_grande = entrada.read(8)
                salida.write(tam_grande)
                tam_caja = int.from_bytes(tam_grande, byteorder='big')
                datos = entrada.read(tam_caja - 16)
            else:
                datos = entrada.read(tam_caja - 8)
            salida.write(datos)
            if tipo_bytes == b'mdat':
                break

def recuperar_archivos(ruta_disco: Path, carpeta_salida: Path):
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    contador_foto = 0
    contador_video = 0
    ventana = bytearray()
    with ruta_disco.open('rb') as entrada:
        while True:
            byte = entrada.read(1)
            if byte == b'':
                break
            ventana.append(byte[0])
            if len(ventana) > TAM_VENTANA:
                ventana.pop(0)
            if ventana.endswith(CABECERA_JPEG):
                contador_foto += 1
                ruta_salida = carpeta_salida / f'foto_{contador_foto}.jpeg'
                extraer_jpeg(entrada, ruta_salida)
                print(f'Fotografia recuperada: {contador_foto} -> {ruta_salida.name}')
                ventana.clear()
            elif bytes(ventana) == CABECERA_MP4:
                contador_video += 1
                ruta_salida = carpeta_salida / f'video_{contador_video}.mp4'
                extraer_mp4(entrada, ruta_salida)
                print(f'Video recuperado: {contador_video} -> {ruta_salida.name}')
                ventana.clear()
    print()
    print('Fotografias recuperadas:', contador_foto)
    print('Videos recuperados:', contador_video)
if __name__ == '__main__':
    recuperar_archivos(ruta_disco=Path('disk.img'), carpeta_salida=Path('recuperados'))