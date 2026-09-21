from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/login", methods=["POST", "GET", "OPTIONS"])
def login():
    # Lee el JSON que envía Lazarus (espera USR y PASS)
    datos = request.get_json(silent=True) or request.form.to_dict() or {}
    print(f"\n[+] PETICIÓN RECIBIDA EN /login!")
    print(f"    Datos recibidos desde el ejecutable: {datos}")

    # Estructura que responde con R: 200 y resetea cualquier contador de bloqueos
    respuesta = {
        "R": 200,
        "status": "success",
        "attempts": 0,
        "attempts_remaining": 999,
        "blocked": False,
        "message": "Acceso concedido",
    }

    print("    [->] Enviando R: 200 y reseteo de intentos a Lazarus...\n")
    return jsonify(respuesta), 200


# Ruta comodín para capturar cualquier otra verificación que haga la app
@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "OPTIONS"])
def catch_all(path):
    print(f"\n[!] PETICIÓN RECIBIDA EN RUTA COMODÍN: /{path}")
    return (
        jsonify(
            {
                "R": 200,
                "status": "success",
                "attempts": 0,
                "attempts_remaining": 999,
                "blocked": False,
            }
        ),
        200,
    )

if __name__ == "__main__":
    print("==================================================")
    print(" Servidor Mock Activo (Bypass de Validación)")
    print(" Escuchando en 0.0.0.0:8080 (Todas las interfaces)")
    print("==================================================")
    # CAMBIO CLAVE: host='0.0.0.0' para responder en la IP 45.76.173.114 de Loopback
    app.run(host="0.0.0.0", port=8080, debug=True)