# Actividad 2

Esta actividad se enfoca en buscar una condición o salto que pueda evadir el requerimiento o validación de una contraseña.

El archivo parche.py maneja la libreria PathLib para el manejo de las rutas; Se declaran 2 variables, una donde esta el archivo original y otra que es el ejecutable parcheado.

La tercera variable es el desplazamiento, el cual es en 0x245, donde esta cerca de una comparación.

Luego de eso el programa solo salta hasta el desplazamiento, y sabiendo la diferencia de los hexadecimales, hay que añadir los codigo en hexadecimal para hacer cumplir la condición, en este caso compara eax con eax, o sea es un true, luego lee los 3 bits y los ignora, para luego leer eel archivo restante.

Finalmente se unen los buffers para crear el nuevo archivo parcheado.

![Golshi](https://i.pinimg.com/736x/db/ba/13/dbba13bf2cdbf7cbe9cdfa9b72c6336f.jpg)
