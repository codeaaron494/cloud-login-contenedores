import os
import time
import bcrypt
import psycopg


def conectar():
    url = os.getenv("DATABASE_URL")

    if url:
        return psycopg.connect(url, connect_timeout=5)

    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )


def inicializar():
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cuentas_demo (
                    id INTEGER GENERATED ALWAYS AS IDENTITY
                        PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    nombre VARCHAR(100) NOT NULL
                )
            """)

            usuarios = [
                ("usuario_demo1", "DEMO_PASSWORD_1",
                 "Estudiante Uno"),
                ("usuario_demo2", "DEMO_PASSWORD_2",
                 "Estudiante Dos"),
            ]

            for username, variable, nombre in usuarios:
                password = os.environ[variable]

                hashed = bcrypt.hashpw(
                    password.encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8")

                cursor.execute("""
                    INSERT INTO cuentas_demo
                        (username, password_hash, nombre)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) DO NOTHING
                """, (username, hashed, nombre))

    print("Base de datos inicializada correctamente.",
          flush=True)


for intento in range(1, 11):
    try:
        inicializar()
        break
    except psycopg.OperationalError as error:
        if intento == 10:
            raise
        print(f"Esperando PostgreSQL ({intento}/10)",
              flush=True)
        time.sleep(3)
