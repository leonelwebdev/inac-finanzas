import environ
import os
from pathlib import Path

# Ruta base del proyecto (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializar entorno
env = environ.Env(
    DEBUG=(bool, False)
)

# Cargar .env si existe (solo local, en Azure ya se toma de env vars)
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(env_file)
