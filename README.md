# Language App API

API REST para una aplicación de aprendizaje de idiomas (estilo Duolingo), construida con **Django REST Framework** y **PostgreSQL**. Incluye autenticación con **JWT**, permisos por rol (usuario normal / administrador), filtros, paginación y manejo de errores.

## 🌐 Despliegue

La API está desplegada en una VM y disponible públicamente:

- **Base de la API:** https://lazo-idiomas.uaeftt-ute.site/api/
- **Panel de administración:** https://lazo-idiomas.uaeftt-ute.site/admin/
- **Health check:** https://lazo-idiomas.uaeftt-ute.site/api/health/

El despliegue es automático mediante GitHub Actions ([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)): cada push a `main` corre los tests y, si pasan, despliega por SSH a la VM (Gunicorn + Nginx).

---

## 📑 Tabla de contenidos

- [Stack tecnológico](#-stack-tecnológico)
- [Modelo de datos](#-modelo-de-datos-7-entidades)
- [Instalación y ejecución local](#-instalación-y-ejecución-local)
- [Autenticación](#-autenticación)
- [Listado de endpoints](#-listado-de-endpoints)
- [Ejemplos de uso (con token)](#-ejemplos-de-uso-con-token)
- [Filtros, búsqueda y paginación](#-filtros-búsqueda-y-paginación)
- [Permisos](#-permisos)
- [Manejo de errores](#-manejo-de-errores)
- [Colección Postman](#-colección-postman)

---

## 🛠 Stack tecnológico

| Componente | Versión |
|---|---|
| Python | 3.12+ |
| Django | 5.2 |
| Django REST Framework | 3.17 |
| djangorestframework-simplejwt | 5.5 (JWT) |
| django-filter | 25.2 |
| PostgreSQL | 16 |
| Gunicorn + Nginx | producción |

---

## 🗄 Modelo de datos (7 entidades)

```
Language ──< Level ──< Lesson ──< Exercise
                │                     │
                │                     └──< UserProgress >── User
                └──< Enrollment >── User
User ──1:1── UserProfile
```

| Entidad | Descripción |
|---|---|
| **Language** | Idioma disponible (inglés, francés...). |
| **Level** | Nivel de un idioma (A1, B2...). Pertenece a un `Language`. |
| **Lesson** | Lección dentro de un nivel. Pertenece a un `Level`. |
| **Exercise** | Ejercicio de una lección (opción múltiple, traducir, etc.). |
| **UserProfile** | Perfil del usuario: XP, racha, idioma/nivel actual. |
| **Enrollment** | Inscripción de un usuario a un nivel. |
| **UserProgress** | Intento de un usuario en un ejercicio (correcto, puntos). |

---

## 🚀 Instalación y ejecución local

### 1. Requisitos previos

- Python 3.12+
- PostgreSQL 16 corriendo localmente
- (Opcional) [uv](https://github.com/astral-sh/uv) como gestor de paquetes

### 2. Clonar el repositorio

```bash
git clone <URL-del-repo>
cd language_api
```

### 3. Crear la base de datos en PostgreSQL

```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE languages_db;
CREATE USER languages_user WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE languages_db TO languages_user;
ALTER DATABASE languages_db OWNER TO languages_user;
\q
```

### 4. Variables de entorno

Copia el archivo de ejemplo y ajusta los valores:

```bash
cp .env.example .env
```

```ini
DEBUG=1
SECRET_KEY=dev-secret-key-cambia-esto-en-produccion
DB_NAME=languages_db
DB_USER=languages_user
DB_PASSWORD=admin123
DB_HOST=127.0.0.1
DB_PORT=5432
CORS_ORIGIN=http://localhost:3000
```

> ⚠️ En producción usa `DEBUG=0` y un `SECRET_KEY` fuerte y secreto.

### 5. Instalar dependencias

**Con uv (recomendado):**
```bash
uv sync
```

**Con pip + venv:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Migraciones y superusuario

```bash
# con uv: anteponer "uv run" a cada comando
python manage.py migrate
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

La API queda en `http://127.0.0.1:8000/api/` y el admin en `http://127.0.0.1:8000/admin/`.

---

## 🔐 Autenticación

La API usa **JWT (JSON Web Tokens)** con `djangorestframework-simplejwt`.

1. **Registro** (público): `POST /api/auth/register/`
2. **Login** (público): `POST /api/auth/login/` → devuelve `access` y `refresh`
3. Enviar el token en cada petición protegida:
   ```
   Authorization: Bearer <access_token>
   ```
4. **Refrescar** el token cuando expira: `POST /api/auth/refresh/`

> El `access` token dura **30 minutos** y el `refresh` **7 días**.

### Roles

- **Usuario normal:** puede leer el catálogo y gestionar sus propios datos (perfil, inscripciones, progreso).
- **Administrador** (`is_staff`): puede crear/editar/eliminar el catálogo (idiomas, niveles, lecciones, ejercicios) y ver los datos de todos los usuarios. Se crea con `createsuperuser` o marcando "staff" en el admin.

---

## 📋 Listado de endpoints

> Base de la API: `https://lazo-idiomas.uaeftt-ute.site/api/`

### Sistema y autenticación

| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| GET | `/api/health/` | Pública | Verifica que la API está viva. |
| POST | `/api/auth/register/` | Pública | Registrar un nuevo usuario. |
| POST | `/api/auth/login/` | Pública | Obtener tokens `access` y `refresh`. |
| POST | `/api/auth/refresh/` | Pública | Renovar el token `access`. |

### Catálogo (CRUD)

Cada recurso expone los 5 endpoints REST estándar:

| Método | Ruta | Acción |
|---|---|---|
| GET | `/api/<recurso>/` | Listar (paginado) |
| POST | `/api/<recurso>/` | Crear |
| GET | `/api/<recurso>/{id}/` | Detalle |
| PUT / PATCH | `/api/<recurso>/{id}/` | Actualizar |
| DELETE | `/api/<recurso>/{id}/` | Eliminar |

| Recurso | Leer | Crear / Editar / Eliminar |
|---|---|---|
| `languages` | Público | Solo admin |
| `levels` | Público | Solo admin |
| `lessons` | Público | Solo admin |
| `exercises` | Usuario autenticado | Solo admin |
| `profiles` | Dueño o admin | Dueño o admin |
| `enrollments` | Dueño o admin | Dueño o admin |
| `progress` | Dueño o admin | Crear: dueño · *(sin PUT/PATCH/DELETE)* |

**Endpoint extra:** `GET /api/profiles/me/` → devuelve el perfil del usuario autenticado.

---

## 💡 Ejemplos de uso (con token)

> Reemplaza `$BASE` por `https://lazo-idiomas.uaeftt-ute.site/api` (producción) o `http://127.0.0.1:8000/api` (local).

### 1. Registrar un usuario

```bash
curl -X POST $BASE/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "email": "maria@mail.com", "password": "secreta123"}'
```
Respuesta `201`:
```json
{ "id": 5, "username": "maria", "email": "maria@mail.com" }
```

### 2. Login y obtener token

```bash
curl -X POST $BASE/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "maria", "password": "secreta123"}'
```
Respuesta `200`:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
  "access":  "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}
```

Guarda el `access` en una variable para reutilizarlo:
```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOi..."
```

### 3. Listar el catálogo (lectura pública)

```bash
curl $BASE/languages/
```

### 4. Crear un idioma (requiere admin)

```bash
curl -X POST $BASE/languages/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Inglés", "codigo": "en", "bandera_emoji": "🇬🇧", "activo": true}'
```

### 5. Ver mi perfil

```bash
curl $BASE/profiles/me/ -H "Authorization: Bearer $TOKEN"
```

### 6. Inscribirse a un nivel

```bash
curl -X POST $BASE/enrollments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"level": 1}'
```

### 7. Registrar progreso en un ejercicio

```bash
curl -X POST $BASE/progress/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exercise": 3, "correcto": true}'
```
> Si `correcto` es `true`, los puntos del ejercicio se suman automáticamente al `xp_total` del perfil.

---

## 🔎 Filtros, búsqueda y paginación

### Paginación

Todas las listas están paginadas (10 por página por defecto):

```
GET /api/lessons/?page=2&page_size=20
```
Respuesta:
```json
{
  "count": 42,
  "next": "http://.../api/lessons/?page=3",
  "previous": "http://.../api/lessons/?page=1",
  "results": [ ... ]
}
```

### Búsqueda (`?search=`)

| Recurso | Busca en |
|---|---|
| `languages` | nombre, código |
| `levels` | nombre, código CEFR |
| `lessons` | título, descripción |
| `exercises` | pregunta |

```
GET /api/lessons/?search=saludos
```

### Filtros por campo

| Recurso | Filtros disponibles |
|---|---|
| `languages` | `activo` |
| `levels` | `language`, `codigo_cefr` |
| `lessons` | `level` |
| `exercises` | `lesson`, `tipo` |
| `profiles` | `language`, `level` |
| `enrollments` | `level`, `completado` |
| `progress` | `exercise`, `correcto` |

```
GET /api/exercises/?lesson=1&tipo=multiple_choice
GET /api/enrollments/?completado=true
```

### Ordenamiento (`?ordering=`)

```
GET /api/profiles/?ordering=-xp_total
```

---

## 🛡 Permisos

| Permiso | Comportamiento |
|---|---|
| `IsAdminOrReadOnly` | Cualquiera lee; solo `is_staff` escribe. (languages, levels, lessons, exercises) |
| `IsOwnerOrAdmin` | Solo el dueño del objeto o un admin accede. (profiles, enrollments, progress) |

- Los **ejercicios** ocultan el campo `respuesta_correcta` a los usuarios normales (solo el admin lo ve).
- En `profiles`, `enrollments` y `progress` cada usuario **solo ve sus propios registros**; el admin ve todos.

---

## ⚠️ Manejo de errores

La API responde con códigos HTTP estándar y cuerpo JSON:

| Código | Significado | Ejemplo |
|---|---|---|
| `400` | Datos inválidos | `{"codigo": ["This field is required."]}` |
| `401` | Sin token o token inválido | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Sin permisos (ej. usuario normal intenta crear) | `{"detail": "You do not have permission to perform this action."}` |
| `404` | Recurso no encontrado | `{"detail": "No encontrado."}` |
| `500` | Error interno del servidor | — |

---

## 📮 Colección Postman

El repositorio incluye la colección lista para importar:

**[`Language App API.postman_collection.json`](./Language%20App%20API.postman_collection.json)**

Pasos para usarla:
1. Abre Postman → **Import** → selecciona el archivo `.json`.
2. Ejecuta primero **Auth → Login** para obtener el token.
3. Copia el `access` token en la variable de entorno/colección (ej. `{{token}}`).
4. Las peticiones protegidas ya envían el header `Authorization: Bearer {{token}}`.

---

## 📂 Estructura del proyecto

```
language_api/
├── config/              # Configuración Django (settings, urls, wsgi)
├── catalog/
│   ├── models/          # 7 entidades, una por archivo
│   ├── serializers/     # Un serializer por modelo
│   ├── views/           # ViewSets + auth + health
│   ├── filters.py       # FilterSets de django-filter
│   ├── permissions.py   # IsAdminOrReadOnly, IsOwnerOrAdmin
│   ├── pagination.py     # Paginación estándar
│   └── urls.py          # Router DRF
├── .github/workflows/   # CI/CD a la VM
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 📊 Cumplimiento de la rúbrica

| Requisito | Estado |
|---|---|
| Backend + conexión PostgreSQL | ✅ |
| CRUD y endpoints REST (7 entidades) | ✅ |
| Autenticación JWT + permisos | ✅ |
| Despliegue público | ✅ https://lazo-idiomas.uaeftt-ute.site |
| Documentación + colección Postman | ✅ |
