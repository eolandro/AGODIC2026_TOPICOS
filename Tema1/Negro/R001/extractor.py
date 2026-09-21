""""

Recupera las fotografias y videos de una imagen de memoria formateada
buscando los "magic numbers" (firmas de inicio) y los finales de archivo,
SIN usar el sistema de archivos (que fue borrado al formatear).

"""

import sys
import os
import struct


def buscar_todas(datos, firma, inicio=0, fin=None):

    fin = len(datos) if fin is None else fin
    posiciones = []
    pos = inicio
    while True:
        i = datos.find(firma, pos, fin)
        if i == -1:
            break
        posiciones.append(i)
        pos = i + 1
    return posiciones


def tamano_mp4(datos, inicio):

    n = len(datos)
    off = inicio
    total = 0
    while off + 8 <= n:
        tam = struct.unpack('>I', datos[off:off + 4])[0]
        tipo = datos[off + 4:off + 8]

        if not (tipo.isalnum() or tipo in (b'free', b'skip', b'wide')):
            break
        if tam == 0:
            total = n - inicio
            break
        if tam == 1:
            tam = struct.unpack('>Q', datos[off + 8:off + 16])[0]
        if tam < 8 or off + tam > n:
            break
        total += tam
        off += tam
    return total


def fin_jpeg(datos, inicio):

    n = len(datos)
    p = inicio + 2
    while p + 1 < n:
        if datos[p] != 0xFF:
            return -1
        m = datos[p + 1]
        if m == 0xFF:
            p += 1
            continue
        if m == 0xD9:
            return p + 2
        if m == 0x01 or 0xD0 <= m <= 0xD8:
            p += 2
            continue
        if p + 3 >= n:
            return -1
        longitud = (datos[p + 2] << 8) | datos[p + 3]
        if m == 0xDA:
            p += 2 + longitud
            while p + 1 < n:
                if datos[p] == 0xFF:
                    mm = datos[p + 1]
                    if mm == 0xD9:
                        return p + 2
                    if mm == 0x00 or 0xD0 <= mm <= 0xD7:
                        p += 2
                        continue
                    p += 1
                    continue
                p += 1
            return -1
        p += 2 + longitud
    return -1


def detectar_jpeg(datos):

    encontrados = []
    candidatos = [i for i in buscar_todas(datos, b'\xff\xd8\xff')
                  if datos[i + 3] in (0xE0, 0xE1)]
    fin_anterior = -1
    for inicio in candidatos:
        if inicio <= fin_anterior:
            continue
        fin = fin_jpeg(datos, inicio)
        if fin == -1:
            continue
        encontrados.append((inicio, 'jpg', fin - inicio))
        fin_anterior = fin
    return encontrados


def detectar_avi(datos):

    encontrados = []
    for i in buscar_todas(datos, b'RIFF'):
        if datos[i + 8:i + 12] == b'AVI ':
            tam = struct.unpack('<I', datos[i + 4:i + 8])[0] + 8
            encontrados.append((i, 'avi', tam))
    return encontrados


def detectar_mp4(datos):

    encontrados = []
    for i in buscar_todas(datos, b'ftyp'):
        inicio = i - 4
        if inicio < 0:
            continue
        tam = tamano_mp4(datos, inicio)
        if tam > 0:
            encontrados.append((inicio, 'mp4', tam))
    return encontrados

def main():
    ruta_imagen = sys.argv[1] if len(sys.argv) > 1 else 'disk.img'
    carpeta = sys.argv[2] if len(sys.argv) > 2 else 'recuperados'

    if not os.path.exists(ruta_imagen):
        sys.exit(f"[X] No se encontro la imagen: {ruta_imagen}")

    with open(ruta_imagen, 'rb') as f:
        datos = f.read()
    os.makedirs(carpeta, exist_ok=True)


    archivos = detectar_jpeg(datos) + detectar_avi(datos) + detectar_mp4(datos)
    archivos.sort()


    contador = {'jpg': 0, 'mp4': 0, 'avi': 0}
    total = 0
    for inicio, tipo, tam in archivos:
        contador[tipo] += 1
        total += 1
        nombre = os.path.join(carpeta, f"{tipo}_{contador[tipo]:03d}.{tipo}")
        with open(nombre, 'wb') as salida:
            salida.write(datos[inicio:inicio + tam])
        print(f"[+] {nombre:<28} offset={inicio:<10} {tam} bytes")

    print(f"\nRecuperados: {contador['jpg']} JPG, {contador['mp4']} MP4, "
          f"{contador['avi']} AVI  (total {total})")


if __name__ == '__main__':
    main()
