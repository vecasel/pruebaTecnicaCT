
# SAC Ríos del Desierto – Backend Django  
## Documentación General + Guía de Implementación en Producción

Este documento unifica los dos README entregados:  
- **README general del proyecto Django (instalación, ejecución y endpoints)** fileciteturn1file1  
- **Guía completa de despliegue productivo con Gunicorn + Nginx** fileciteturn1file0  

El resultado es una guía única, coherente y lista para entregar.

---

# 1. Descripción General del Proyecto

El backend desarrollado en **Django + Django REST Framework** implementa las funcionalidades de la herramienta SAC Ríos del Desierto:

1. Consultar un cliente por tipo y número de documento.  
2. Obtener el historial de compras del cliente.  
3. Exportar los datos en **CSV**.  
4. Generar un reporte de **clientes fidelizados** en formato **Excel** usando `openpyxl`.  
5. Dar servicio a un frontend HTML/JS mediante consumo por HTTP.  

La base de datos por defecto es SQLite, pero la guía de despliegue soporta PostgreSQL o SQL Server.

---

# 2. Requisitos Previos

### Local (desarrollo)
- Python 3.10+
- pip
- Git  
- Navegador web  
- SQLite (incluida por defecto)

### Producción
- Ubuntu Server  
- Python 3  
- Virtualenv  
- Gunicorn  
- Nginx  
- Base de datos PostgreSQL o SQL Server  

---

# 3. Instalación y Ejecución en Entorno Local

## 3.1 Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/rios-desierto-sac.git
cd rios-desierto-sac
```

## 3.2 Crear entorno virtual

```bash
python -m venv venv
```

Activar:

**Windows**
```bash
.env\Scriptsctivate
```

**Linux/macOS**
```bash
source venv/bin/activate
```

## 3.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

Si el archivo no existe:

```bash
pip install django djangorestframework pandas openpyxl
```

## 3.4 Configuración de base de datos

SQLite por defecto:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 3.5 Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## 3.6 Crear superusuario

```bash
python manage.py createsuperuser
```

## 3.7 Ejecutar servidor

```bash
python manage.py runserver
```

---

# 4. Endpoints del Backend Django

## 4.1 Buscar cliente
```
GET /api/client/search/?document_type=CC&document_number=123456789
```

## 4.2 Exportar cliente (CSV)
```
GET /api/client/export/?document_type=CC&document_number=123456789
```

## 4.3 Reporte de fidelización (Excel)
```
GET /api/reports/loyal-customers/
```

Todas las respuestas siguen el mismo formato establecido para la prueba técnica.

---

# 5. Estructura del Proyecto

```
rios-desierto-sac/
  manage.py
  requirements.txt
  rios_desierto/
  customers/
  templates/
  db.sqlite3
```

---

# 6. Configuración de Variables de Entorno (Producción)

Variables importantes:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS="mi-dominio.com,localhost"`
- Credenciales de la base de datos (si no se usa SQLite).

Ejemplo temporal:

```bash
export DJANGO_SECRET_KEY="clave_secreta"
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS="mi-dominio.com,localhost"
```

---

# 7. Deploy Completo en Producción (Ubuntu + Gunicorn + Nginx)

## 7.1 Preparar el servidor

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip nginx
```

Si usas PostgreSQL:

```bash
sudo apt install -y postgresql libpq-dev
```

## 7.2 Descargar código

```bash
cd /opt
sudo git clone https://github.com/tu-usuario/sac-rios-desierto-django.git
sudo chown -R $USER:$USER sac-rios-desierto-django
cd sac-rios-desierto-django
```

## 7.3 Crear entorno virtual + dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 7.4 Migraciones + archivos estáticos

```bash
python manage.py migrate
python manage.py collectstatic
```

## 7.5 Probar Gunicorn

```bash
gunicorn rios_desierto.wsgi:application --bind 0.0.0.0:8000
```

---

# 8. Crear servicio systemd (Gunicorn)

Archivo:

```bash
sudo nano /etc/systemd/system/gunicorn-rios-desierto.service
```

Contenido:

```ini
[Unit]
Description=Gunicorn Rios del Desierto Django service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/sac-rios-desierto-django
Environment="PATH=/opt/sac-rios-desierto-django/venv/bin"
ExecStart=/opt/sac-rios-desierto-django/venv/bin/gunicorn rios_desierto.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Activar:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn-rios-desierto
sudo systemctl enable gunicorn-rios-desierto
```

---

# 9. Configuración de Nginx (reverse proxy)

Archivo:

```bash
sudo nano /etc/nginx/sites-available/rios-desierto
```

Contenido:

```nginx
server {
    listen 80;
    server_name mi-dominio.com;

    location /static/ {
        alias /opt/sac-rios-desierto-django/staticfiles/;
    }

    location / {
        root /opt/sac-rios-desierto-frontend;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/rios-desierto /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

# 10. HTTPS con Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d mi-dominio.com
```

---

# 11. Arquitectura Final de Producción

| Componente | Función |
|-----------|---------|
| **Nginx** | Proxy inverso, HTTPS, archivos estáticos, frontend |
| **Gunicorn** | Servidor WSGI para ejecutar Django |
| **Django** | Lógica de negocio, REST API, generación de CSV/Excel |
| **Base de datos** | PostgreSQL / SQL Server (o SQLite en pruebas) |

---

# 12. Resumen para la Prueba Técnica

- Backend hecho con **Django + DRF**, enfocado en consultas de clientes + fidelización.  
- Endpoints funcionales: búsqueda, exportación CSV, reporte Excel.  
- Despliegue profesional usando **Gunicorn + Nginx**.  
- Documento listo para entrevista y presentación.

---

# Fin del documento
