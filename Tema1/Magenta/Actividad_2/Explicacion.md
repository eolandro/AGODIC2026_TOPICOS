# Resumen de la Práctica: Parchear un `.exe` y Automatizarlo en Python

---

## 1. Crackeando el Ejecutable con x32dbg

* **Primer intento:** 
  * Al ejecutar el programa mediante `wine T.exe`, saltó un mensaje indicando la falta de contraseña.
  * Se probó pasando la contraseña como argumento de línea de comandos (`wine T.exe mi_clave`), obteniendo como resultado: **"Acceso no concedido"**.

* **Aplicación del parche:**
  1. Se abrió el ejecutable en **x32dbg** y se realizó una búsqueda de cadenas de texto (*strings*), localizando `"Acceso concedido"`.
  2. Al inspeccionar el ensamblador cercano, se identificó que la lógica de validación dependía de la instrucción de salto condicional `JNE` (*Jump if Not Equal*).
  3. Se modificó la instrucción cambiando `JNE` por `JE` (*Jump if Equal*) para invertir la condición de acceso.
  4. Se guardó/parcheó el archivo y se verificó que el bypass funcionó correctamente.

---

## 2. Automatización del Parche con Python

El siguiente objetivo fue replicar el parche de manera programática mediante un script en Python:

* **Análisis de Opcodes (Hexadecimal):**
  * Se abrieron ambos ejecutables (original y parcheado) en **GHex** para comparar las diferencias a nivel de bytes.
  * En la arquitectura **x86**, la instrucción `JNE` corresponde al opcode `0F 85`, mientras que `JE` corresponde a `0F 84`. Por lo tanto, la modificación requerida consistía únicamente en cambiar el byte `85` por `84`.

* **Localización del Byte:**
  * El byte objetivo se ubicó en el *offset* decimal **585** (correspondiente a `0x249` en hexadecimal).

* **Implementación en el Script:**
  * Se tomó la estructura del script base, actualizando las rutas de los archivos e indicando la posición `249` (`0x249`) para la modificación exacta del byte.

---

## 3. Comparativa de Bytes mediante Hexdiff en Python

Para visualizar la diferencia entre el ejecutable original y el parcheado a modo de *hexdump diff*:

* Se utilizó la librería estándar `difflib` de Python.
* Se adaptó una rutina de comparación visual para resaltar el byte modificado dentro de la estructura hexadecimal del ejecutable.

---


