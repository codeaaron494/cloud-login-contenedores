import os
from pathlib import Path

import bcrypt
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

usuarios = [
    ("usuario_demo1", "DEMO_PASSWORD_1", "Estudiante Uno"),
    ("usuario_demo2", "DEMO_PASSWORD_2", "Estudiante Dos"),
]

sql = """
CREATE TABLE IF NOT EXISTS cuentas_demo (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre VARCHAR(100) NOT NULL
);
"""

for username, variable, nombre in usuarios:
    password = os.environ[variable]
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    sql += f"""
INSERT INTO cuentas_demo (username, password_hash, nombre)
VALUES ('{username}', '{hashed}', '{nombre}')
ON CONFLICT (username) DO NOTHING;
"""

destino = Path(__file__).parent / "init.sql"
destino.write_text(sql, encoding="utf-8")

print("Script SQL generado correctamente:", destino)
