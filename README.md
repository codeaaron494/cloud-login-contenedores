# Cloud Login - Docker Compose

Aplicación web de autenticación con Flask, PostgreSQL y Nginx.

## Arquitectura

- Nginx: proxy inverso y entrada HTTP.
- Flask + Gunicorn: aplicación web y autenticación.
- PostgreSQL 17: almacenamiento de usuarios.
- Docker Compose: coordinación de servicios y redes.
- Volumen Docker: persistencia de datos.

## Requisitos

- Docker
- Docker Compose
- Python 3 para generar el SQL de inicialización

## Configuración local

1. Copiar `.env.example` como `.env`.
2. Reemplazar las credenciales de ejemplo.
3. Instalar bcrypt y python-dotenv.
4. Generar `db/init.sql` con `python3 db/generar_init.py`.
5. Ejecutar `docker compose up -d --build`.
6. Abrir el puerto 8080.

## Seguridad

Las credenciales se configuran fuera del repositorio.
Las contraseñas se almacenan usando bcrypt.
PostgreSQL no tiene un puerto publicado al host.

## Estado

Versión de desarrollo para pruebas en Codespaces.
El despliegue público requiere HTTPS y controles
adicionales de seguridad.
