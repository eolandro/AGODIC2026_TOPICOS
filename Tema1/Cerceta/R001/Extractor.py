# 1. ENCABEZADOS DE INICIO (Firmas Binarias / Magic Numbers)
Encabezado = {
    'JPEG': b'\xFF\xD8\xFF',
    'PNG':  b'\x89PNG\r\n\x1a\n',
    'MP4':  b'ftyp',
    'AVI':  b'RIFF'
}

# Cola de final para las imágenes
Cola_JPEG = b'\xFF\xD9'
Cola_PNG  = b'IEND\xaeB`\x82'

# Función sencilla para ordenar la lista sin usar lambda
def obtener_inicio(archivo):
    return archivo['inicio']

# Leer todo el disco en modo binario
with open('disk.img', 'rb') as archivo:
    contenido = archivo.read()

# =====================================================================
# PASO 1: ENCONTRAR CADA ARCHIVO
# =====================================================================
archivos_encontrados = []

for tipo, firma in Encabezado.items():
    inicio_busqueda = 0
    while True:
        posicion = contenido.find(firma, inicio_busqueda)
        if posicion == -1:
            break
        
        # Ajuste para MP4: tomar 4 bytes atrás para incluir la cabecera completa
        inicio_real = posicion - 4 if tipo == 'MP4' and posicion >= 4 else posicion
        
        # Validar que si es AVI diga 'AVI ' a los 8 bytes
        if tipo == 'AVI' and contenido[posicion+8:posicion+12] != b'AVI ':
            inicio_busqueda = posicion + len(firma)
            continue

        archivos_encontrados.append({'tipo': tipo, 'inicio': inicio_real})
        
        # Salto de seguridad para ignorar miniaturas incrustadas en metadatos
        inicio_busqueda = posicion + 100000

# Ordenar los archivos por su posición en el disco (Sin lambda)
archivos_encontrados.sort(key=obtener_inicio)

# =====================================================================
# PASO 2: BUSCAR LA COLA Y EXTRAER
# =====================================================================
contador = 1

if archivos_encontrados:
    for i in range(len(archivos_encontrados)):
        elemento = archivos_encontrados[i]
        inicio = elemento['inicio']
        tipo = elemento['tipo']
        
        # Definir el límite seguro (donde empieza el SIGUIENTE archivo)
        siguiente_inicio = archivos_encontrados[i+1]['inicio'] if i + 1 < len(archivos_encontrados) else len(contenido)

        # SI ES FOTO JPEG: Buscamos la COLA real (FF D9) usando rfind
        if tipo == 'JPEG':
            pos_cola = contenido.rfind(Cola_JPEG, inicio, siguiente_inicio)
            fin = pos_cola + len(Cola_JPEG) if pos_cola != -1 else siguiente_inicio

        # SI ES FOTO PNG: Buscamos su COLA IEND
        elif tipo == 'PNG':
            pos_cola = contenido.rfind(Cola_PNG, inicio, siguiente_inicio)
            fin = pos_cola + len(Cola_PNG) if pos_cola != -1 else siguiente_inicio

        # SI ES VIDEO: Corta directo hasta donde empieza el siguiente archivo
        else:
            fin = siguiente_inicio

        # Recortar los bytes del archivo
        bytes_archivo = contenido[inicio:fin]

        # Filtro de seguridad: descarta fragmentos de menos de 100 KB
        if tipo in ['JPEG', 'PNG'] and len(bytes_archivo) < 100000:
            continue

        # Asignar extensión y guardar
        extension = 'jpg' if tipo == 'JPEG' else tipo.lower()
        nombre_salida = f"extraido_{contador}.{extension}"

        with open(nombre_salida, 'wb') as salida:
            salida.write(bytes_archivo)

        print(f"[{tipo}] Extraído con éxito: {nombre_salida} ({len(bytes_archivo)} bytes)")
        contador += 1

else:
    print("No se encontraron firmas binarias en la memoria.")