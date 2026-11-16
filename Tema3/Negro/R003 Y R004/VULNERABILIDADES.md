# Vulnerabilidades parchadas - insecure-webapi (index.py)

Repositorio (fork): https://github.com/joshgarcia-x/insecure-webapi

Servidor: https://negrowebapi.duckdns.org (Debian 13 en DigitalOcean, gunicorn + systemd + nginx + Let's Encrypt)

## Evidencias

| Evidencia | Enlace |
|---|---|
| Fork con los parches | https://github.com/joshgarcia-x/insecure-webapi |
| Video 1: API funcionando y sobrevive al cerrar SSH | PEGAR_ENLACE_YOUTUBE |
| Video 2: certificado de Let's Encrypt | PEGAR_ENLACE_YOUTUBE |

## Resumen

| # | Vulnerabilidad | OWASP Top 10 (2025) | CWE | Commit |
|---|---|---|---|---|
| 1 | Inyección SQL | A05 Injection | 89 | 50f3664 |
| 2 | Contraseñas con MD5 sin sal | A04 Cryptographic Failures | 916, 759 | 9312254 |
| 3 | Tokens predecibles y sin expiración | A07 Authentication Failures | 330, 613 | 070e64f |
| 4 | Descarga sin control de acceso (IDOR) | A01 Broken Access Control | 639, 862 | fbd387d |
| 5 | Subida de archivos sin restricciones | A06 Insecure Design / A01 Broken Access Control | 434, 22, 400 | e06b2d6 |
| 6 | Contraseñas y tokens en logs, modo debug | A09 Logging and Alerting Failures / A02 Security Misconfiguration | 532, 209, 778 | ded019e |
| 7 | Credenciales en el repositorio y privilegios excesivos | A02 Security Misconfiguration | 798, 540, 250 | f35c8ce |
| 8 | Falta de validación de entradas y manejo de errores | A10 Mishandling of Exceptional Conditions | 20, 755, 772 | 5b65a15 |
| 9 | Tráfico sin cifrar, sin límite de intentos ni cabeceras de seguridad | A02 / A04 / A07 | 319, 307, 693 | 22841e0 |
| 10 | Autenticación de un solo factor (se agrega TOTP) | A07 Authentication Failures | 308, 294, 204 | d599a80 |
| 11 | Imágenes en gzip sin límite de descompresión | A06 Insecure Design | 409, 400 | de99a0d |
| 12 | Descarga con URL predecible (se usa URL aleatoria) | A01 Broken Access Control | 639, 330, 524 | 3a8bac7 |

Requisitos indicados por el profesor:

| Requisito | Dónde se cumple |
|---|---|
| bcrypt en registro y login | Parche 2 |
| TOTP en registro y login | Parche 10 |
| Imagen comprimida con gzip y después en base64 | Parche 11 |
| Descarga regresa URL aleatoria | Parche 12 |
| Certificado de Let's Encrypt | Parche 9 y video 2 |

Cada commit incluye una descripción larga con la vulnerabilidad, una prueba de concepto, la corrección y cómo se verificó (`git show <commit>`).

## 1. Inyección SQL
- **Dónde:** /Registro, /Login, /Imagen y /Descargar.
- **Problema:** los datos del JSON se pegaban directamente en las consultas SQL con f-strings o con el operador `+`.
- **Ejemplo de ataque:** en /Login, enviar `uname = ana" -- ` comentaba el resto de la consulta y entregaba un token válido sin conocer la contraseña.
- **Riesgo:** saltarse el login y leer, modificar o borrar información de la base de datos.
- **Parche:** todas las consultas usan parámetros (`%s`) del conector de MySQL, que envía los valores separados del SQL. En /Imagen se usa `cursor.lastrowid` en lugar de `select max(id)`, que además tenía condición de carrera.
- **Commit:** 50f3664

## 2. Contraseñas con MD5 sin sal
- **Dónde:** /Registro y /Login.
- **Problema:** las contraseñas se guardaban como `md5(password)`, calculado por MySQL. MD5 es muy rápido de romper y, sin sal, dos usuarios con la misma contraseña tienen el mismo hash. Además la contraseña viajaba dentro del texto SQL.
- **Riesgo:** si se filtra la tabla Usuario, las contraseñas se recuperan con tablas rainbow o fuerza bruta.
- **Parche:** se usa **bcrypt** con factor de costo 12 (sal aleatoria incluida en el hash). La verificación se hace con `bcrypt.checkpw`, que compara en tiempo constante. La contraseña se limita a 72 bytes, el máximo que procesa bcrypt.
- **Nota:** los usuarios registrados antes del parche deben registrarse de nuevo.
- **Commit:** 9312254

## 3. Tokens predecibles y sin expiración
- **Dónde:** función `getToken()`, /Imagen y /Descargar.
- **Problema:** el token se generaba con la hora actual y `random.random()`, que no es criptográficamente seguro, y luego se mezclaba con SHA1 y MD5. La tabla `AccesoToken` guarda la `fecha`, pero nunca se revisaba. Con un token inválido, /Imagen fallaba con error 500.
- **Riesgo:** adivinar tokens y hacerse pasar por otro usuario; un token robado servía para siempre.
- **Parche:** el token se genera con `secrets.token_hex(32)` (256 bits). La nueva función `usuarioDesdeToken()` solo acepta tokens emitidos hace menos de 60 minutos, y un token inexistente o vencido responde `{"R": -2}`.
- **Commit:** 070e64f

## 4. Descarga sin control de acceso (IDOR)
- **Dónde:** /Descargar.
- **Problema:** se consultaba el token pero nunca se revisaba el resultado, y la imagen se buscaba solo por su `id`.
- **Ejemplo de ataque:** `{"token":"x","id":1}` entregaba la imagen 1 sin tener sesión; recorriendo los `id` se bajaban todas.
- **Riesgo:** cualquier persona podía descargar las imágenes de otros usuarios.
- **Parche:** se exige un token vigente y la consulta filtra por `id` **y** `id_Usuario`. Si la imagen no es del usuario se responde igual que si no existiera (`{"R": -3}`), para no revelar qué ids existen. Los archivos solo se sirven desde la carpeta `img/`.
- **Commit:** fbd387d

## 5. Subida de archivos sin restricciones
- **Dónde:** /Imagen.
- **Problema:** la extensión (`ext`) y el contenido los decidía el usuario, y la ruta se armaba concatenando `ext`. No había límite de tamaño ni validación del base64, y todas las subidas de un usuario usaban el mismo archivo temporal.
- **Ejemplo de ataque:** subir `<script>alert(document.cookie)</script>` con `ext = "html"`; al descargarlo se servía como `text/html` (XSS almacenado). Con `ext = "../../x"` se intentaba escribir fuera de `img/`.
- **Riesgo:** XSS almacenado, escritura fuera de la carpeta, agotamiento de disco y errores 500.
- **Parche:** lista blanca de extensiones (`png`, `jpg`, `jpeg`, `gif`), base64 validado, verificación de la firma del archivo (magic bytes) según la extensión, tamaño máximo de 5 MB, nombre en disco generado por el servidor (`img/<id>.<ext>`) y `rollback` si algo falla.
- **Commit:** e06b2d6

## 6. Contraseñas y tokens en logs, modo debug
- **Dónde:** /Login, manejo de errores y la línea final `run(...)`.
- **Problema:** /Login imprimía la consulta SQL con la contraseña en texto claro y escribía cada token en `/tmp/log`, legible por todos los usuarios del sistema. Los errores se imprimían con `print(e)` y el servidor corría con `debug=True`, que muestra trazas de Python al cliente. No se registraban los intentos fallidos.
- **Riesgo:** robo de contraseñas y sesiones leyendo los logs; exposición del código interno; ataques de fuerza bruta sin detectar.
- **Parche:** se eliminan el `print` y `/tmp/log`. Se usa el módulo `logging`: los errores registran solo el tipo de excepción y el código de MySQL, y los inicios de sesión exitosos y fallidos se registran con usuario e IP, nunca con contraseña ni token. `debug=False` y el servidor escucha solo en `127.0.0.1`.
- **Commit:** ded019e

## 7. Credenciales en el repositorio y privilegios excesivos
- **Dónde:** `db.json`, `db.sql` y la conexión a la base de datos.
- **Problema:** `db.json`, con usuario y contraseña de MySQL, estaba en un repositorio **público**, y `db.sql` repetía la contraseña y daba `GRANT ALL PRIVILEGES`.
- **Riesgo:** cualquiera que clonara el repo conocía las credenciales; con una inyección SQL se podían borrar tablas o crear usuarios.
- **Parche:** las credenciales se leen de variables de entorno que systemd carga desde `/etc/webapi/webapi.env` (propietario root, permisos 600). Se quitó `db.json` del repositorio (queda `db.json.example` y `.gitignore`). El usuario de la base solo tiene `SELECT, INSERT, UPDATE, DELETE`. La contraseña anterior se considera comprometida y se cambió en el servidor.
- **Commit:** f35c8ce

## 8. Falta de validación de entradas y manejo de errores
- **Dónde:** todos los endpoints.
- **Problema:** solo se revisaba que existieran las llaves del JSON. Se aceptaban cuentas vacías o con tipos incorrectos, correos sin formato y unames repetidos (la BD solo exigía único el par uname+correo). Un JSON roto, un `id` no numérico o una falla de la BD daban error 500, y las conexiones a la BD quedaban abiertas al rechazar una petición.
- **Riesgo:** registros basura, suplantación de cuentas con el mismo uname y denegación de servicio por agotar conexiones.
- **Parche:** la función `cuerpoJSON()` exige un objeto JSON con campos de texto no vacíos. Se validan el formato del uname (3 a 50 caracteres), del correo y del token, la longitud de la contraseña y que el `id` sea un entero positivo. Uname y correo deben ser únicos por separado. La conexión se abre después de validar y siempre se cierra. Los errores 400, 404, 405, 413 y 500 responden un JSON genérico sin detalles internos.
- **Commit:** 5b65a15

## 9. Despliegue: tráfico sin cifrar, sin límite de intentos ni cabeceras
- **Dónde:** forma de publicar la API.
- **Problema:** la API original se publicaba con el servidor de desarrollo de Bottle y por HTTP en texto claro, sin límite de intentos en /Login ni cabeceras de seguridad.
- **Riesgo:** captura de contraseñas, tokens e imágenes en la red y fuerza bruta de contraseñas.
- **Parche:** servicio de systemd con gunicorn (sigue activo al cerrar SSH y se levanta solo al reiniciar). nginx como proxy con HTTPS de **Let's Encrypt**, redirección de HTTP a HTTPS, HSTS, cabeceras `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` y `Content-Security-Policy`, y límite de 10 peticiones por minuto por IP en /Login y /Registro (responde 429).
- **Commit:** 22841e0

## 10. Autenticación de un solo factor (se agrega TOTP)
- **Dónde:** /Registro y /Login.
- **Problema:** /Login solo pedía usuario y contraseña. Además, la respuesta tardaba distinto si el usuario existía o no, lo que permitía averiguar qué usuarios existen.
- **Riesgo:** con una contraseña filtrada el atacante entra directamente.
- **Parche:** /Registro genera un secreto TOTP de 160 bits y regresa la URI `otpauth://` para darlo de alta en una app autenticadora (Google Authenticator) con un código QR. /Login exige además el código de 6 dígitos. Cada código sirve **una sola vez** (columna `totp_ultimo` y un UPDATE atómico). Si el usuario no existe se verifica contra un hash de relleno para que la respuesta tarde lo mismo, y no se indica qué factor falló.
- **Commit:** d599a80

## 11. Imágenes en gzip sin límite de descompresión
- **Dónde:** /Imagen.
- **Problema:** el cliente debe mandar `data = base64(gzip(imagen))`. Descomprimir datos del usuario sin límite permite una "bomba gzip": unos KB que se expanden a GB.
- **Riesgo:** agotar la memoria del servidor.
- **Parche:** la función `descomprimirGzip()` exige la firma gzip y descomprime con `zlib.decompressobj` limitado a 5 MB. Rechaza archivos más grandes, truncados o con datos extra. Una bomba de 49 KB que se expande a 50 MB se rechaza sin consumir memoria.
- **Commit:** de99a0d

## 12. Descarga con URL aleatoria
- **Dónde:** /Descargar y la nueva ruta `GET /img/<enlace>`.
- **Problema:** si la descarga usara una URL predecible (por ejemplo `/img/15.png`), cualquiera podría recorrer los números y bajar todas las imágenes sin sesión.
- **Parche:** /Descargar valida token y dueño y regresa una URL `https://negrowebapi.duckdns.org/img/<43 caracteres aleatorios>` generada con `secrets.token_urlsafe(32)` (256 bits). Cada llamada genera una URL distinta, que se guarda en la tabla `EnlaceDescarga` y **caduca a los 5 minutos**. La imagen se sirve con `Cache-Control: no-store` y un enlace inválido o vencido responde 404.
- **Commit:** 3a8bac7

## Verificación

El commit 5b8c2cd agrega `deploy/cliente.py`, que reproduce los ataques de todos los parches y verifica que se rechazan:

```
python3 deploy/cliente.py https://negrowebapi.duckdns.org pruebas
...
(nginx limitó 8 peticiones con 429 por exceso de intentos; se reintentaron)

Resultado: 29 correctas, 0 fallidas
```
