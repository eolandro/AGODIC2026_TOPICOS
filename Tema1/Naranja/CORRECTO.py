import os
import io
import struct
from PIL import Image

ARCHIVO_IMAGEN = "disk.img"
CARPETA_SALIDA = "recuperados"
CABECERA_JPEG = b'\xFF\xD8\xFF'
FINAL_JPEG = b'\xFF\xD9'
FIRMA_FTYP = b'ftyp'
FIRMA_RIFF = b'RIFF' 
FIRMA_EBML = b'\x1A\x45\xDF\xA3' 

os.makedirs(CARPETA_SALIDA, exist_ok=True)

with open(ARCHIVO_IMAGEN, "rb") as archivo:
    datos = archivo.read()

def validar_jpeg(contenido):
    try:
        imagen = Image.open(io.BytesIO(contenido))
        imagen.load()
        return True, imagen.size

    except Exception:
        return False, None

posicion = 0
contador_fotos = 0
cabeceras_jpeg = 0

while True:
    inicio = datos.find(CABECERA_JPEG, posicion)
    if inicio == -1:
        break
    cabeceras_jpeg += 1
    buscar_desde = inicio + len(CABECERA_JPEG)
    recuperado = False
    while True:
        fin = datos.find(FINAL_JPEG, buscar_desde)
        if fin == -1:
            break
        fin_real = fin + len(FINAL_JPEG)
        posible_imagen = datos[inicio:fin_real]
        valido, dimensiones = validar_jpeg(posible_imagen)
        if valido:
            nombre = os.path.join(
                CARPETA_SALIDA,
                f"foto_recuperada_{contador_fotos}.jpg"
            )
            with open(nombre, "wb") as salida:
                salida.write(posible_imagen)
            print("    [OK] Fotografía recuperada correctamente")
            print(f"    Archivo: {nombre}")
            print(f"    Tamaño: {len(posible_imagen)} bytes")
            print(
                f"    Dimensiones: "
                f"{dimensiones[0]} x {dimensiones[1]}"
            )
            contador_fotos += 1
            posicion = fin_real
            recuperado = True
            break
        else:
            buscar_desde = fin_real

    if not recuperado:
        posicion = inicio + len(CABECERA_JPEG)

def obtener_tamano_video(datos, inicio):
    posicion = inicio
    ultimo_final_valido = inicio
    MINIMO_VIDEO = 1024
    while posicion + 8 <= len(datos):
        try:
            tamano = struct.unpack(
                ">I",
                datos[posicion:posicion + 4]
            )[0]
            tipo = datos[
                posicion + 4:
                posicion + 8
            ]

        except:
            break
        if tamano >= 8:
            siguiente = posicion + tamano
            if siguiente > len(datos):
                break
        elif tamano == 1:
            if posicion + 16 > len(datos):
                break
            tamano_extendido = struct.unpack(
                ">Q",
                datos[posicion + 8:
                      posicion + 16]
            )[0]
            siguiente = posicion + tamano_extendido
            if siguiente > len(datos):
                break
        elif tamano == 0:
            siguiente = len(datos)
        else:
            break
        try:
            nombre_box = tipo.decode("ascii")
        except:
            break
        ultimo_final_valido = siguiente
        posicion = siguiente
        if ultimo_final_valido - inicio > 500_000_000:
            break
    tamano_total = ultimo_final_valido - inicio
    if tamano_total >= MINIMO_VIDEO:
        return ultimo_final_valido
    return None
def obtener_tamano_avi(datos, inicio):
    MINIMO_VIDEO = 1024
    if inicio + 12 > len(datos):
        return None
    if datos[inicio + 8:inicio + 12] != b'AVI ':
        return None
    try:
        tamano = struct.unpack("<I", datos[inicio + 4:inicio + 8])[0]
    except struct.error:
        return None
    fin = inicio + 8 + tamano
    if fin > len(datos):
        fin = len(datos)
    if fin - inicio >= MINIMO_VIDEO:
        return fin
    return None

def obtener_tamano_mkv(datos, inicio, limite=200_000_000):
    MINIMO_VIDEO = 1024
    fin = inicio + limite
    if fin > len(datos):
        fin = len(datos)
    if fin - inicio >= MINIMO_VIDEO:
        return fin
    return None

posicion_busqueda = 0
contador_videos = 0
posibles_videos = 0

while True:
    posicion_ftyp = datos.find(FIRMA_FTYP, posicion_busqueda)
    if posicion_ftyp == -1:
        break
    inicio_video = posicion_ftyp - 4
    if inicio_video < 0:
        posicion_busqueda = posicion_ftyp + 4
        continue
    posibles_videos += 1
    fin_video = obtener_tamano_video(
        datos,
        inicio_video
    )
    if fin_video is not None:
        video = datos[inicio_video:fin_video]
        if len(video) >= 1024:
            marca = datos[
                posicion_ftyp + 4:
                posicion_ftyp + 8
            ]
            try:
                marca_nombre = marca.decode("ascii")
            except:
                marca_nombre = "desconocido"
            if marca == b'qt  ':
                extension = "mov"
            else:
                extension = "mp4"
            nombre = os.path.join(
                CARPETA_SALIDA,
                f"video_recuperado_{contador_videos}.{extension}"
            )
            with open(nombre, "wb") as salida:
                salida.write(video)
            print("    [OK] Video (MP4/MOV) recuperado correctamente")
            print(f"    Archivo: {nombre}")
            print(f"    Tamaño: {len(video)} bytes")
            contador_videos += 1
    else:
        print(
            "    [X] La estructura del video "
            "no pudo determinarse correctamente"
        )
    posicion_busqueda = posicion_ftyp + 4

posicion_busqueda = 0

while True:
    posicion_riff = datos.find(FIRMA_RIFF, posicion_busqueda)
    if posicion_riff == -1:
        break
    fin_video = obtener_tamano_avi(datos, posicion_riff)
    if fin_video is not None:
        posibles_videos += 1
        video = datos[posicion_riff:fin_video]
        nombre = os.path.join(
            CARPETA_SALIDA,
            f"video_recuperado_{contador_videos}.avi"
        )
        with open(nombre, "wb") as salida:
            salida.write(video)
        print("    [OK] Video (AVI) recuperado correctamente")
        print(f"    Archivo: {nombre}")
        print(f"    Tamaño: {len(video)} bytes")
        contador_videos += 1
    posicion_busqueda = posicion_riff + len(FIRMA_RIFF)

posicion_busqueda = 0

while True:
    posicion_ebml = datos.find(FIRMA_EBML, posicion_busqueda)
    if posicion_ebml == -1:
        break
    posibles_videos += 1
    fin_video = obtener_tamano_mkv(datos, posicion_ebml)
    if fin_video is not None:
        video = datos[posicion_ebml:fin_video]
        nombre = os.path.join(
            CARPETA_SALIDA,
            f"video_recuperado_{contador_videos}.mkv"
        )
        with open(nombre, "wb") as salida:
            salida.write(video)
        print("    [OK] Video (MKV/WEBM) recuperado correctamente (tamaño aproximado)")
        print(f"    Archivo: {nombre}")
        print(f"    Tamaño: {len(video)} bytes")
        contador_videos += 1
    else:
        print(
            "    [X] La estructura del video MKV/WEBM "
            "no pudo determinarse correctamente"
        )
    posicion_busqueda = posicion_ebml + len(FIRMA_EBML)

print("\n==========================================")
print(" RESULTADOS FINALES")
print("==========================================")
print(f"Cabeceras JPEG encontradas: {cabeceras_jpeg}")
print(f"Fotografías recuperadas:    {contador_fotos}")
print()
print(f"Posibles videos encontrados: {posibles_videos}")
print(f"Videos recuperados:          {contador_videos}")
print("\n==========================================")
print(" PROCESO TERMINADO")
print("==========================================")
