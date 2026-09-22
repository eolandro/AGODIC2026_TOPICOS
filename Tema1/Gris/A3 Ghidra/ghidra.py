import sys


def main():
    nombre_salida = "datos.json"
    if len(sys.argv) >= 2:
        nombre_salida = sys.argv[1]

    nombre = "Equipo Gris"
    carrera = "Equipo Gris"
    edad = 20

    try:
        archivo = open(nombre_salida, "w")                   
    except IOError:
        print("Error: no se pudo crear el archivo")         
        return 1

    with archivo:
        archivo.write("{\n")                                
        archivo.write(f'  "nombre": "{nombre}",\n')           
        archivo.write(f'  "edad": {edad},\n')                 
        archivo.write(f'  "carrera": "{carrera}"\n')        
        archivo.write("}\n")                                  

    print("Archivo datos.json generado correctamente")        

    with open("prueba.txt", "w") as prueba:
        prueba.write("Equipo Gris")

    return 0


main()