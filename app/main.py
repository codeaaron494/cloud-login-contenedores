import os
import bcrypt
import psycopg

from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import (
    Flask, request, render_template,
    redirect, url_for, session
)

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri="memory://",
    default_limits=[]
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("COOKIE_SECURE", "true").lower() == "true"
)


def conectar_db():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url, connect_timeout=5)

    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5
    )


@app.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("bienvenida"))

    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            error = "Completa todos los campos."
        else:
            try:
                with conectar_db() as conexion:
                    with conexion.cursor() as cursor:
                        cursor.execute(
                            """
                            SELECT id, username, password_hash, nombre
                            FROM cuentas_demo
                            WHERE username = %s
                            """,
                            (username,)
                        )
                        usuario = cursor.fetchone()

                if usuario and bcrypt.checkpw(
                    password.encode("utf-8"),
                    usuario[2].encode("utf-8")
                ):
                    session.clear()
                    session["usuario_id"] = usuario[0]
                    session["username"] = usuario[1]
                    session["nombre"] = usuario[3]
                    return redirect(url_for("bienvenida"))

                error = "Usuario o contraseña incorrectos."

            except psycopg.Error:
                app.logger.exception("Error de conexión a PostgreSQL")
                error = "No se pudo verificar el acceso."

    return render_template("login.html", error=error)


@app.route("/bienvenida")
def bienvenida():
    if not session.get("usuario_id"):
        return redirect(url_for("login"))

    return render_template(
        "bienvenida.html",
        nombre=session["nombre"]
    )


@app.route("/salir", methods=["POST"])
def salir():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
