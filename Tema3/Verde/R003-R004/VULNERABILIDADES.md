# Vulnerabilidades parchadas - insecure-webapi (index.py)

Repositorio:https://github.com/MichGV/insecure-webapi-VERDE

| # | Vulnerabilidad | OWASP Top 10 (2021) | Commit |
|---|---|---|---|
| 1 | SQL Injection | A03 Injection | 118fdc1 |
| 2 | Contraseñas con MD5 sin sal | A02 Cryptographic Failures | f57752e |
| 3 | Token predecible | A07 Identification and Authentication Failures | d80f102 |
| 4 | Subida de archivos sin validar | A04 Insecure Design / A01 Broken Access Control | 74c87bb |
| 5 | Descarga sin control de acceso (IDOR) | A01 Broken Access Control | 1e4b912 |
| 6 | Modo debug y registro de tokens en /tmp/log | A05 Security Misconfiguration / A09 Logging Failures | 1a2ff74 |
| 7 | Falta de validación de campos vacíos y correo | A03 Injection (validación de entrada) | 2caac4f |
| 8 | Tokens que nunca caducan | A07 Identification and Authentication Failures | 4e9a0bf |

## 1. SQL Injection
- **Dónde:** endpoints /Registro, /Login, /Imagen y /Descargar.
- **Problema:** los datos del JSON se pegaban directamente en las consultas SQL con f-strings o con el operador +.
- **Ejemplo de ataque:** en /Login, enviar `uname = x" or 1=1 #` permitía entrar sin conocer la contraseña.
- **Riesgo:** saltarse el login, leer, modificar o borrar información de la base de datos.
- **Parche:** todas las consultas usan parámetros (`%s`) y el conector de MySQL escapa los valores. También se eliminó un `print` que mostraba la contraseña en la consola.
- **Commit:** 118fdc1

## 2. Contraseñas con MD5 sin sal
- **Dónde:** /Registro y /Login.
- **Problema:** las contraseñas se guardaban con `md5()`. MD5 es muy rápido de romper y, sin sal, dos usuarios con la misma contraseña tienen el mismo hash.
- **Riesgo:** si se filtra la base de datos, las contraseñas se recuperan fácilmente con tablas rainbow o fuerza bruta.
- **Parche:** se usa PBKDF2-HMAC-SHA256 con 200,000 iteraciones y una sal aleatoria de 16 bytes por usuario. La comparación se hace con `hmac.compare_digest` para evitar ataques de tiempo. La columna `password` es `varchar(250)`, suficiente para el nuevo hash.
- **Nota:** los usuarios registrados antes del parche deben registrarse de nuevo.
- **Commit:** f57752e

## 3. Token de sesión predecible
- **Dónde:** función `getToken()`.
- **Problema:** el token se generaba con la hora actual y `random.random()`, que no es criptográficamente seguro, y luego se mezclaba con SHA1 y MD5.
- **Riesgo:** un atacante podría adivinar o reproducir tokens y hacerse pasar por otro usuario.
- **Parche:** el token se genera con `secrets.token_hex(16)` (128 bits aleatorios seguros).
- **Commit:** d80f102

## 4. Subida de archivos sin validar
- **Dónde:** endpoint /Imagen.
- **Problema:** la extensión (`ext`) la decidía el usuario y se usaba para armar la ruta del archivo. Además, si el token no existía, el código fallaba o continuaba sin sesión válida.
- **Riesgo:** guardar archivos fuera de la carpeta `img/` (por ejemplo, con `ext = ../../algo`) o subir archivos ejecutables.
- **Parche:** solo se aceptan las extensiones `png`, `jpg`, `jpeg` y `gif` (en minúsculas), y se rechaza la petición si el token no es válido.
- **Commit:** 74c87bb

## 5. Descarga sin control de acceso (IDOR)
- **Dónde:** endpoint /Descargar.
- **Problema:** se buscaba el token pero nunca se revisaba si era válido, y la imagen se buscaba solo por su `id`.
- **Riesgo:** cualquier persona, incluso sin sesión, podía descargar las imágenes de otros usuarios cambiando el `id`.
- **Parche:** se exige un token válido y la consulta filtra por `id_Usuario`, de modo que solo el dueño puede descargar su imagen. También se quitó un `print` que exponía rutas internas del servidor.
- **Commit:** 1e4b912

## 6. Modo debug y registro de tokens en /tmp/log
- **Dónde:** endpoint /Login y la línea final `run(...)`.
- **Problema:** el servidor se ejecutaba con `debug=True`, que muestra errores internos al cliente, y el Login escribía en `/tmp/log` las consultas con los tokens de sesión.
- **Riesgo:** cualquier usuario del servidor podía leer `/tmp/log` y robar sesiones; los errores en modo debug revelan detalles del código.
- **Parche:** se cambió a `debug=False` y se eliminó la escritura en `/tmp/log`.
- **Commit:** 1a2ff74

## 7. Falta de validación de campos vacíos y del correo
- **Dónde:** /Registro y /Login.
- **Problema:** se aceptaban usuarios, contraseñas y correos vacíos o con cualquier formato.
- **Riesgo:** registros basura, cuentas sin contraseña y datos inválidos en la base de datos.
- **Parche:** se rechazan los campos vacíos y el correo se valida con una expresión regular (`re.fullmatch`).
- **Commit:** 2caac4f

## 8. Tokens que nunca caducan
- **Dónde:** /Imagen y /Descargar.
- **Problema:** la tabla `AccesoToken` guarda la `fecha`, pero nunca se revisaba; un token servía para siempre.
- **Riesgo:** un token robado daba acceso permanente a la cuenta.
- **Parche:** el token solo es válido durante 1 hora después del login (`fecha > now() - interval 1 hour`).
- **Commit:** 4e9a0bf


