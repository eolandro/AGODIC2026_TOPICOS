Cabeceras = {
    "FFD8FFE1": "jpeg",
    "00000018667479706D703432": "mp4"
}

Final = {
    "FFD9": "jpeg",
    "6D646174": "mp4"
}

Datos = None
cache = []

CabeceraFoto = [
    b'\xff', b'\xd8', b'\xff', b'\xe1'
]

CabeceraVideo = [
    b'\x00', b'\x00', b'\x00', b'\x18',
    b'f', b't', b'y', b'p',
    b'm', b'p', b'4', b'2'
]

foto = 0
video = 0

with open('disk.img', 'rb') as entrada:
    bt = True

    while bt:
        bt = entrada.read(1)

        if bt == b'':
            break

        cache.append(bt)

        if len(cache) > 12:
            cache = cache[1:]

        if cache[-4:] == CabeceraFoto:
            foto = foto + 1

            with open('foto_' + str(foto) + '.jpeg', 'wb') as salida:

                for dato in CabeceraFoto:
                    salida.write(dato)

                tam1 = entrada.read(1)
                tam2 = entrada.read(1)

                salida.write(tam1)
                salida.write(tam2)

                tam = tam1[0] * 256 + tam2[0]

                Datos = entrada.read(tam - 2)
                salida.write(Datos)

                anterior = None

                while True:
                    bt = entrada.read(1)

                    if bt == b'':
                        break

                    salida.write(bt)

                    if anterior == b'\xff' and bt == b'\xd9':
                        break

                    anterior = bt

            print('Fotografia recuperada:', foto)
            cache = []

        elif cache == CabeceraVideo:
            video = video + 1

            with open('video_' + str(video) + '.mp4', 'wb') as salida:

                for dato in CabeceraVideo:
                    salida.write(dato)

                Datos = entrada.read(12)
                salida.write(Datos)

                while True:
                    tam = entrada.read(4)
                    tipo = entrada.read(4)

                    if len(tam) < 4 or len(tipo) < 4:
                        break

                    salida.write(tam)
                    salida.write(tipo)

                    tamCaja = 0

                    for dato in tam:
                        tamCaja = tamCaja * 256 + dato

                    if tamCaja == 1:
                        tamGrande = entrada.read(8)
                        salida.write(tamGrande)

                        tamCaja = 0

                        for dato in tamGrande:
                            tamCaja = tamCaja * 256 + dato

                        Datos = entrada.read(tamCaja - 16)

                    else:
                        Datos = entrada.read(tamCaja - 8)

                    salida.write(Datos)

                    if tipo == b'mdat':
                        break

            print('Video recuperado:', video)
            cache = []

print()
print('Fotografias recuperadas:', foto)
print('Videos recuperados:', video)
