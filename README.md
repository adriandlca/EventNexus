# EventNexus

Plataforma de gestion y descubrimiento de eventos construida con Django + Django REST Framework en el backend y React (via CDN) en el frontend.

## Caracteristicas

- Registro y login de usuarios (autenticacion por sesion + JWT opcional).
- Creacion de eventos con titulo, fecha, ubicacion, precio e imagen de portada.
- Listado publico de eventos en la home.
- API REST para consumo externo.
- Panel admin de Django para gestion avanzada.

## Stack

- Python 3.11+
- Django 5.2+
- Django REST Framework
- djangorestframework-simplejwt
- Pillow (manejo de imagenes)
- React 18 + Babel (cargados via CDN, sin build step)

## Instalacion

```bash
git clone <repo-url>
cd EventNexus

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_events
python manage.py runserver
```

Visita `http://127.0.0.1:8000`.

### Usuario demo (opcional)

El comando `seed_events` crea automaticamente un usuario de prueba:

- Usuario: `demo`
- Contrasena: `demo12345`

## Uso

- Home: `/` — lista todos los eventos.
- Registro: `/register/`
- Login: `/login/`
- Crear evento: `/events/create/` (requiere login)
- Admin: `/admin/` (requiere superusuario — `python manage.py createsuperuser`)

## API

| Metodo | Endpoint                       | Auth      | Descripcion                          |
|--------|--------------------------------|-----------|--------------------------------------|
| POST   | `/api/auth/register/`          | No        | Crear cuenta                         |
| POST   | `/api/auth/token/`             | No        | Obtener JWT (access + refresh)       |
| GET    | `/api/events/`                 | No        | Listar eventos                       |
| GET    | `/api/events/<id>/`            | No        | Detalle de evento                    |
| POST   | `/api/events/create/`          | Sesion    | Crear evento (multipart/form-data)   |

## Estructura del proyecto

```
EventNexus/
├── EventNexus/           # Configuracion del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Auth, home, comandos de gestion
│   └── management/commands/seed_events.py
├── events/               # Modelo Event + vistas/API
├── tickets/              # Modulo de tickets
├── notifications/        # Modulo de notificaciones
├── Templates/            # Templates Django + scripts React inline
├── media/                # Uploads de usuarios (gitignored)
├── db.sqlite3            # Base de datos dev (gitignored)
├── manage.py
└── requirements.txt
```

## Notas

- Proyecto de portafolio. `SECRET_KEY` y `DEBUG=True` son aceptables para desarrollo local, no para produccion.
- Para resetear la base de datos: borrar `db.sqlite3` y volver a correr `migrate` + `seed_events`.
