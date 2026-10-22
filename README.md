# Cloud Login - Docker Compose

Aplicación web con autenticación mediante Flask,
PostgreSQL y Nginx.

## Arquitectura

- Nginx: proxy inverso.
- Flask + Gunicorn: aplicación web.
- PostgreSQL 17: almacenamiento de usuarios.
- Docker Compose: redes y servicios.
- Volumen Docker: persistencia de datos.

## Ejecución local

1. Copiar .env.example a .env.
2. Configurar las variables de entorno.
3. Instalar bcrypt y python-dotenv.
4. Ejecutar python3 db/generar_init.py.
5. Ejecutar docker compose up -d --build.
6. Abrir el puerto 8080.

## Pruebas

- Inicio de sesión válido.
- Credenciales incorrectas.
- Acceso restringido sin sesión.
- Cierre de sesión.
- Persistencia de PostgreSQL.

## Seguridad

- Contraseñas almacenadas con bcrypt.
- Consultas SQL parametrizadas.
- Credenciales excluidas de Git.
- Base de datos sin puerto publicado.

## Despliegue

La aplicación está preparada para contenerización.
El despliegue cloud y las medidas adicionales de
seguridad se documentarán antes de la publicación.
