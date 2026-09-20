import sys
import re

PATRON = re.compile(r'^\s*(-?\d+)\s*([+-])\s*(-?\d+)\s*$')

def decodificar(texto):
    datos = bytearray()
    for num_linea, linea in enumerate(texto.splitlines(), 1):
        if not linea.strip():
            continue
        m = PATRON.match(linea)
        if not m:
            print(f"[aviso] linea {num_linea} no reconocida: {linea!r}", file=sys.stderr)
            continue
        a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
        valor = a + b if op == '+' else a - b
        if not 0 <= valor <= 255:
            print(f"[aviso] linea {num_linea}: valor fuera de rango ({valor})", file=sys.stderr)
            continue
        datos.append(valor)
    return bytes(datos)

def main():
    if len(sys.argv) < 2:
        print("Uso: python decodificador.py salida.txt > reconstruido.bin", file=sys.stderr)
        return 1
    with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
        texto = f.read()
    datos = decodificar(texto)
    sys.stdout.buffer.write(datos)
    print(f"[info] {len(datos)} bytes decodificados", file=sys.stderr)
    return 0

if __name__ == '__main__':
    sys.exit(main())