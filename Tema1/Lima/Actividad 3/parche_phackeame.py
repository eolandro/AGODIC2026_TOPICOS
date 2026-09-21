from pathlib import Path

DirectorioScript = Path(__file__).parent

RutaOriginal = DirectorioScript / 'phackeame.exe'
RutaParche = DirectorioScript / 'phackeame_parche.exe'

# Firma de bytes correspondiente a:
#   0042A25F   cmp dword ptr ss:[ebp-1C], C8000000   (81 7D E4 C8 00 00 00)
#   0042A266   jne phackeame.42A284                  (75 1C)
Firma = bytes.fromhex('817DE4C800000075')
Parche = b'\x90\x90'   # NOP NOP: anula el salto y siempre "habilita" el acceso

if RutaOriginal.exists():
    with RutaOriginal.open('rb') as original:
        Datos = bytearray(original.read())

    Posicion = Datos.find(Firma)

    if Posicion == -1:
        print('No se encontro la firma esperada. Verifica que sea la version correcta del exe.')
    else:
        InicioJne = Posicion + 7  # los ultimos 2 bytes de la firma son el jne (75 1C)
        Datos[InicioJne:InicioJne + 2] = Parche

        with RutaParche.open('wb') as parche:
            parche.write(Datos)
        print('Parche generado:', RutaParche.resolve())
else:
    print('No se encontro:', RutaOriginal.resolve())
