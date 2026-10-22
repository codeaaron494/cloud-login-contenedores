from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Práctica de Flask</h1>
    <p>Servidor funcionando correctamente.</p>
    <a href="/saludo">Ir al saludo</a>
    """

@app.route("/saludo")
def saludo():
    nombre = request.args.get("nombre", "Estudiante")
    return f"<h1>Hola, {nombre}!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
