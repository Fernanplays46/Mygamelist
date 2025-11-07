

# 🎮 ElJueguitos

Un proyecto web para **gestionar y explorar juegos**, con API en **FastAPI** y vistas **HTML (Jinja2)**.  
Incluye assets estáticos, base de datos SQLite y CLI con Typer.

---

## ✨ Características

- API basada en **FastAPI**
- Vistas con **Jinja2/HTML**
- Carpeta **static/** para CSS, JS e imágenes
- Modelado de datos con **SQLModel**
- Base de datos **SQLite** incluida
- Stack: `Python · FastAPI · SQLModel/SQLite · Jinja2 · Typer (CLI) · Pytest · pdoc`

---

## 🧩 1) Requisitos

- **Python 3.12** (recomendado)  
- **Windows**, macOS o Linux  
- (Opcional) **Git**

---

## ⚙️ 2) Instalación (Windows PowerShell)

💡 Si PowerShell bloquea la activación del entorno virtual:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 1️⃣ Ir a la carpeta del proyecto
```powershell
cd C:\Mygamelist-main\mygamelist
```

### 2️⃣ Crear y activar entorno virtual
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3️⃣ Actualizar pip
```powershell
python -m pip install -U pip
```

### 4️⃣ Instalar el paquete en modo editable  (Hace que `mgl` sea importable)
```powershell
python -m pip install -e .
```

### 5️⃣ Instalar dependencias necesarias
```powershell
python -m pip install "passlib[bcrypt]==1.7.4" "bcrypt==4.0.1" python-multipart itsdangerous jinja2
```

---

## 🗄️ 3) Base de datos y datos de ejemplo

El proyecto usa **SQLite** (`mgl.db` en la raíz).  
Si no existe, se **crea y migra automáticamente** al iniciar la aplicación.

---

## 🚀 4) Ejecutar la aplicación web

### 🪟 Windows
```powershell
python -m uvicorn mgl.api:app --reload
```

### 🐧 Linux / macOS
```bash
uvicorn mgl.api:app --reload
```

---

## 🌍 5) URLs útiles

| Tipo | URL | Descripción |
|------|-----|-------------|
| 🔐 Login | http://127.0.0.1:8000/login | Página de inicio de sesión |
| 🏠 Home | http://127.0.0.1:8000/ | Página principal con destacados |
| 🔎 Buscador | http://127.0.0.1:8000/buscar?q=zelda | Búsqueda de juegos |
| 📄 Ficha | http://127.0.0.1:8000/juego/1 | Detalle de un juego |
| ⚙️ Admin | http://127.0.0.1:8000/admin | Panel de administración |
| 📘 API Docs | http://127.0.0.1:8000/docs | Swagger UI (documentación interactiva) |

> 🧩 `/admin` usa formularios (requiere `python-multipart`)  
> 🔑 La app añade middleware de sesiones (requiere `itsdangerous`)

---

## 💻 6) CLI (Typer)

Ejecuta la CLI incluida:

```powershell
python -m mgl.cli demo
```

Arranca la API y muestra ejemplos de uso.

---

## 🧪 7) Tests y cobertura

### Windows PowerShell
```powershell
pytest --cov=src\mgl --cov-report=term-missing
```

### Linux / macOS
```bash
pytest --cov=src/mgl --cov-report=term-missing
```

---

## 📘 8) Documentación (pdoc)

Genera documentación HTML automática:

```powershell
python -m pip install pdoc
pdoc -o docs/ src/mgl
```

Luego abre `docs/index.html` en tu navegador.

---

## 🧱 9) Estructura del proyecto

```
ElJueguitos/
├── docs/
│   ├── mgl/
│   │   ├── api/
│   │   │   └── routes.html
│   │   ├── domain/
│   │   │   └── models.html
│   │   ├── infra/
│   │   │   └── db.html
│   │   ├── repos/
│   │   │   └── juegos.html
│   │   ├── services/
│   │   │   └── search.html
│   │   ├── api.html
│   │   ├── domain.html
│   │   ├── infra.html
│   │   ├── repos.html
│   │   └── services.html
│   ├── index.html
│   ├── mgl.html
│   └── search.js
├── src/
│   ├── mgl/
│   │   ├── api/
│   │   │   ├── main.py
│   │   │   └── routes.py
│   │   ├── domain/
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── infra/
│   │   │   ├── auth.py
│   │   │   ├── database.py
│   │   │   └── db.py
│   │   ├── repos/
│   │   │   ├── juegos.py
│   │   │   ├── user_repo.py
│   │   │   └── usuarios.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── search.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── juegos.html
│   │   │   ├── juego_detalle.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── favoritos.html
│   │   ├── static/css/styles.css
│   │   ├── web/
│   │   │   ├── games.py
│   │   │   ├── users.py
│   │   │   └── shared.py
│   │   └── cli.py
├── tests/
│   ├── test_api_favoritos.py
│   ├── test_repos_filters.py
│   ├── test_repos_juegos.py
│   └── test_search.py
├── mgl.db
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 🌐 10) Rutas principales

### 🧭 API

| Método | Ruta | Descripción |
|:-------|:------|:-------------|
| `POST` | `/admin/borrar` | Borrar juego (formulario) |
| `GET`  | `/api/juegos` | Lista de juegos |
| `GET`  | `/api/juegos/{id}` | Detalle de un juego |
| `POST` | `/api/favoritos` | Añadir a favoritos |
| `DELETE` | `/api/favoritos/{id}` | Eliminar favorito |
| `POST` | `/api/login` | Autenticación usuario |
| `POST` | `/api/register` | Registro nuevo usuario |
| `GET`  | `/api/usuarios/{id}` | Obtener datos usuario |
| `GET`  | `/api/search` | Buscar juegos |

---

### 🖥️ WEB

| Archivo | Ruta base | Plantilla | Propósito |
|----------|------------|------------|-----------|
| `games.py` | `/juegos`, `/juego/{id}` | `juegos.html`, `juego_detalle.html` | Lista y detalle de juegos |
| `users.py` | `/login`, `/register`, `/favoritos`, `/logout` | `login.html`, `register.html`, `favoritos.html` | Manejo de usuarios |
| `shared.py` | `/`, `/home` | `home.html` | Página principal o dashboard |
