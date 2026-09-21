import os

Cabeceras = {"FFD8FF": "jpeg", "66747970": "mp4"} 
Final = {"FFD9": "jpeg"} 

NOMBRE_ARCHIVO = "disk.img"
CARPETA_SALIDA = "Archivos_recuperados"


def es_inicio_valido_jpeg(data, i):
    if data[i+3:i+4] == b'\xe0' and data[i+6:i+10] == b'JFIF':
        return True
    return data[i+3:i+4] == b'\xe1' and data[i+6:i+10] == b'Exif'


def fin_jpeg(data, i):
    pos = i + 2
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            return None
        m = data[pos + 1]
        if m == 0xD9:
            return pos + 2
        if 0xD0 <= m <= 0xD7 or m == 0x01:
            pos += 2
        elif m == 0xDA:
            largo = (data[pos+2] << 8) | data[pos+3]
            pos += 2 + largo
            while True:
                pos = data.index(b'\xff', pos)
                sig = data[pos+1]
                if sig == 0x00 or 0xD0 <= sig <= 0xD7:
                    pos += 2
                else:
                    break
        else:
            largo = (data[pos+2] << 8) | data[pos+3]
            pos += 2 + largo
    return None


def fin_mp4(data, i):
    validos = {b'ftyp', b'moov', b'mdat', b'free', b'skip', b'wide', b'udta'}
    pos, fin = i, None
    while pos + 8 <= len(data):
        tam = int.from_bytes(data[pos:pos+4], 'big')
        if data[pos+4:pos+8] not in validos:
            break
        if tam == 1:
            tam = int.from_bytes(data[pos+8:pos+16], 'big')
        elif tam == 0:
            tam = len(data) - pos
        if tam <= 0:
            break
        pos += tam
        fin = pos
    return fin


def buscar_y_extraer(data):
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    n_jpg = n_mp4 = 0
    Cache = []
    i = 0
    while i < len(data):
        Cache.append(data[i])
        if len(Cache) > 4:
            Cache.pop(0)

        if Cache[-3:] == [0xFF, 0xD8, 0xFF] and es_inicio_valido_jpeg(data, i-2):
            fin = fin_jpeg(data, i-2)
            if fin:
                nombre = f"{CARPETA_SALIDA}/foto_{n_jpg}.jpg"
                with open(nombre, 'wb') as f:
                    f.write(data[i-2:fin])
                print(f"[jpeg] {nombre}  offset {i-2}-{fin}")
                n_jpg += 1
                i, Cache = fin, []
                continue

        elif Cache == [0x66, 0x74, 0x79, 0x70]:  
            inicio = i - 7
            fin = fin_mp4(data, inicio) if inicio >= 0 else None
            if fin:
                nombre = f"{CARPETA_SALIDA}/video_{n_mp4}.mp4"
                with open(nombre, 'wb') as f:
                    f.write(data[inicio:fin])
                print(f"[mp4] {nombre}  offset {inicio}-{fin}")
                n_mp4 += 1
                i, Cache = fin, []
                continue
        i += 1

    print(f"\nTotal: {n_jpg} foto(s), {n_mp4} video(s)")


if __name__ == "__main__":
    with open(NOMBRE_ARCHIVO, 'rb') as entrada:
        buscar_y_extraer(entrada.read())
