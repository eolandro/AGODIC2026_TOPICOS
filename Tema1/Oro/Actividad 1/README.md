# Actividad 1

Esta es una explicación punto a punto de lo que hace el programa

El archivo Extractv2.py es un archivo python monolitico, eso significa que todo se ejecuta de golpe, no hay funciones a llamar, todo se ejecuta linea por linea.

Las primeras declaraciones son arreglos que contienen codigo hexadecimal, ya sea del formato de la imagen, de las cabeceras y finales de los archivos, y arreglos vacios.

La primera parte del programa abre la imagen en modo de lectura de bytes, la condicional sirve para encontrar la cabecera de la imagen, especificamente la CabeceraPrimaria.

De ahi lo que le sigue es un ciclo que recorre las Cabeceras en busca de resultados exactos a los declarados en el arreglo de Cabeceras, y los guarda en el arreglo Cache.

El segundo ciclo permite identificar el fin de cada archivo, realizando la separación de cada archivo a unitario.

El ultimo ciclo simplemente escribe en archivos nuevos y los genera para su visualizacion (Esto ya fuera del programa).

![Golshi](https://i.pinimg.com/736x/3a/d5/03/3ad503a6206fb1d7979a435d5aec1c6d.jpg)