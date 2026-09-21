import os
import io
from PIL import Image

# Carpetas de salida
DIR_VIDEOS = "videos_final"
DIR_IMAGENES = "imagen_final"

os.makedirs(DIR_VIDEOS, exist_ok=True)
os.makedirs(DIR_IMAGENES, exist_ok=True)

# Firmas (Magic Numbers)
MAGIC_JPEG_START = b'\xff\xd8\xff'
MAGIC_JPEG_END = b'\xff\xd9'

MAGIC_MP4 = b'ftyp'
VALID_MP4_BOXES = {
    b'ftyp', b'moov', b'mdat', b'free', b'skip',
    b'meta', b'uuid', b'wide', b'pdin', b'moof',
    b'mfra', b'styp', b'sidx'
}

def comprobar_imagen(datos_bytes):
    try:
        with Image.open(io.BytesIO(datos_bytes)) as img:
            img.verify()
        return True
    except (IOError, SyntaxError, Exception):
        return False


def buscar_todas_posiciones(data, patron):
    posiciones = []
    pos = 0
    while True:
        idx = data.find(patron, pos)
        if idx == -1:
            break
        posiciones.append(idx)
        pos = idx + 1
    return posiciones


print("=== Leyendo disk.img ===")
with open("disk.img", "rb") as f:
    data = f.read()


# EXTRACCIÓN DE MP4 

print("\n--- Buscando videos MP4 ---")
mp4_positions = buscar_todas_posiciones(data, MAGIC_MP4)
mp4_starts = []
mp4_count = 0

for ftyp_pos in mp4_positions:
    start = ftyp_pos - 4
    if start < 0:
        continue

    ftyp_size = int.from_bytes(data[start:start+4], 'big')
    if 8 <= ftyp_size <= 1024:
        mp4_starts.append(start)
        curr = start
        while curr < len(data):
            if curr + 8 > len(data):
                break
            box_size = int.from_bytes(data[curr:curr+4], 'big')
            box_type = data[curr+4:curr+8]

            if box_type not in VALID_MP4_BOXES or box_size <= 0:
                break

            if box_size == 1:
                if curr + 16 > len(data):
                    break
                ext_size = int.from_bytes(data[curr+8:curr+16], 'big')
                curr += ext_size
            else:
                curr += box_size

        datos_video = data[start:curr]
        ruta_salida = os.path.join(DIR_VIDEOS, f"salida{mp4_count}.mp4")
        with open(ruta_salida, "wb") as f_out:
            f_out.write(datos_video)

        print(f"[MP4] Video guardado: {ruta_salida} ({len(datos_video)} bytes)")
        mp4_count += 1

# EXTRACCIÓN Y COMPROBACIÓN DE IMÁGENES JPEG COMPLETAS
print("\n--- Buscando etiquetas de inicio y fin de JPEG ---")
jpeg_starts_raw = buscar_todas_posiciones(data, MAGIC_JPEG_START)
jpeg_ends = buscar_todas_posiciones(data, MAGIC_JPEG_END)

inicios_principales = []
cursor = 0
for s in jpeg_starts_raw:
    if s < cursor:
        continue
    inicios_principales.append(s)
    if s + 6 <= len(data) and 0xe0 <= data[s+3] <= 0xef:
        app_len = int.from_bytes(data[s+4:s+6], "big")
        cursor = s + 4 + app_len

print(f"Inicios principales de JPEG: {len(inicios_principales)}")
print(f"Finales de JPEG encontrados: {len(jpeg_ends)}")

todos_limites = sorted(inicios_principales + mp4_starts + [len(data)])

img_count = 0
for start in inicios_principales:
    next_limit = [lim for lim in todos_limites if lim > start][0]

    min_end = start
    if start + 6 <= len(data) and 0xe0 <= data[start+3] <= 0xef:
        app_len = int.from_bytes(data[start+4:start+6], "big")
        min_end = start + 4 + app_len

    candidatos_ends = [e for e in jpeg_ends if min_end <= e < next_limit]

    for end in reversed(candidatos_ends):
        candidato_bytes = data[start : end + 2]

        if comprobar_imagen(candidato_bytes):
            ruta_salida = os.path.join(DIR_IMAGENES, f"salida{img_count}.jpeg")
            with open(ruta_salida, "wb") as f_out:
                f_out.write(candidato_bytes)

            with Image.open(io.BytesIO(candidato_bytes)) as img_info:
                dimensiones = f"{img_info.size[0]}x{img_info.size[1]}"

            print(f"[JPEG 4K VÁLIDA] Guardada: {ruta_salida} (Inicio: {start}, Fin: {end+2}, Tamaño: {len(candidato_bytes)} bytes, Res: {dimensiones})")
            img_count += 1
            break

print("\n=== Proceso finalizado ===")
print(f"Total videos extraídos en '{DIR_VIDEOS}': {mp4_count}")
print(f"Total imágenes válidas guardadas en '{DIR_IMAGENES}': {img_count}")
