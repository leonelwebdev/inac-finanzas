# Gestión de finanzas - INAC Padua.

Este repositorio contiene el código para `inac-finanzas`. Seguí las instrucciones a continuación para configurar y ejecutar el proyecto localmente.

---

## Primeros pasos

Para obtener una copia del proyecto y ejecutarlo en tu máquina local, seguí estos pasos (podés copiar, pegar y ejecutar uno por uno en tu consola):

### 1. Clonar el repositorio
```bash
git clone https://github.com/leonelwebdev/inac-finanzas
```

### 2. Abrir la carpeta del proyecto
```bash
cd inac-finanzas
```

### 3. Crear y activar el entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar paquetes
```bash
pip install -r requirements.txt
```

### 5. Migrar la base de datos y crear el superusuario (van a ser las credenciales para tu usuario admin de la app, el email no es obligatorio)
```bash
cd lector
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Levantar el servidor de desarrollo
```bash
python manage.py runserver
```

### 7. Abrir proyecto
Abrí en la web la siguiente URL: http://127.0.0.1:8000/admin/ e iniciá sesión con tu usuario admin.
