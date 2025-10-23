<h1 align="center">Sistema Pancoquito</h1>
<p align="center">Aplicación web en Django para gestionar pedidos y operaciones.</p>

<p align="center">
  <!-- Tech badges -->
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://www.djangoproject.com/"><img alt="Django" src="https://img.shields.io/badge/Django-4.x-092E20?logo=django&logoColor=white"></a>
  <a href="https://www.sqlite.org/"><img alt="SQLite" src="https://img.shields.io/badge/SQLite-DB-003B57?logo=sqlite&logoColor=white"></a>
  <a href="https://www.postgresql.org/"><img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-Optional-4169E1?logo=postgresql&logoColor=white"></a>
  <a href="https://www.docker.com/"><img alt="Docker" src="https://img.shields.io/badge/Docker-Dev-2496ED?logo=docker&logoColor=white"></a>
  <a href="https://developer.mozilla.org/docs/Web/HTML"><img alt="HTML5" src="https://img.shields.io/badge/HTML5-Templates-E34F26?logo=html5&logoColor=white"></a>
  <a href="https://developer.mozilla.org/docs/Web/CSS"><img alt="CSS3" src="https://img.shields.io/badge/CSS3-Styles-1572B6?logo=css3&logoColor=white"></a>
  <a href="https://developer.mozilla.org/docs/Web/JavaScript"><img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-Client-323330?logo=javascript&logoColor=F7DF1E"></a>
  <a href="https://git-scm.com/"><img alt="Git" src="https://img.shields.io/badge/Git-Flow-F05032?logo=git&logoColor=white"></a>
  <a href="https://github.com/features/actions"><img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub%20Actions-CI/CD-2088FF?logo=githubactions&logoColor=white"></a>
</p>

---

## ⚙️ Requisitos
- Python 3.10+
- `pip` y `venv`
- (Opcional) Docker & Docker Compose
- DB por defecto: SQLite (puede migrarse a PostgreSQL)

## 🚀 Puesta en marcha (local)
```bash
# 1) Entorno virtual
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 2) Dependencias
pip install -r requirements.txt

# 3) Migraciones y superusuario
python manage.py migrate
python manage.py createsuperuser

# 4) Correr el servidor
python manage.py runserver
# http://127.0.0.1:8000
