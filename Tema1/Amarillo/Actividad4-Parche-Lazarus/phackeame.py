from pathlib import Path

RutaOriginal = Path('.') / 'phackeame.exe'
RutaParche = Path('.') / 'phackeame_parche.exe'

Desplazamiento = 0x29666
BytesOriginales = b'\x75\x1c'
BytesParche = b'\x90\x90'

if not RutaOriginal.exists():
    print('No se encontro:', RutaOriginal.resolve())
    raise SystemExit(1)

with RutaOriginal.open('rb') as original:
    Buffer0 = original.read(Desplazamiento)
    BytesActuales = original.read(len(BytesOriginales))
    Buffer1 = original.read()

if BytesActuales != BytesOriginales:
    print('Los bytes esperados no coinciden.')
    print('Bytes encontrados:', BytesActuales.hex(' '))
    raise SystemExit(1)

with RutaParche.open('wb') as parche:
    parche.write(Buffer0)
    parche.write(BytesParche)
    parche.write(Buffer1)

print('Parche aplicado correctamente.')
print('Cambio:', BytesOriginales.hex(' '), '->', BytesParche.hex(' '))
print('Archivo generado:', RutaParche.resolve())