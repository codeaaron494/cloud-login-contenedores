import os
from flask import Flask, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def inicio():
    return '<h1>Práctica de sesiones</h1><a href="/activar">Activar sesión de demostración</a>'

@app.route("/activar")
def activar():
    session["autorizado"] = True
    return redirect(url_for("bienvenida"))

@app.route("/bienvenida")
def bienvenida():
    if not session.get("autorizado"):
        return redirect(url_for("inicio"))
    return '<h1>Bienvenido a la página protegida</h1><a href="/salir">Cerrar sesión</a>'

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
