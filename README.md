
# SAC Ríos del Desierto – Backend Django  
## Explicación de la Prueba Técnica + Documentación General + Guía de Implementación

Este documento unifica en un solo archivo:

- La **explicación de la prueba técnica** (qué pedían, objetivos y entregables).
- El **README general** del backend en Django (instalación, uso y endpoints). fileciteturn1file1  
- La **guía de despliegue en ambiente productivo** con Gunicorn + Nginx. fileciteturn1file0  

El resultado es un documento único, coherente y listo para entregar/defender en entrevista.

---

# 0. Explicación de la Prueba Técnica

La prueba técnica consiste en construir una herramienta de consultas para el sistema de fidelización de clientes **SAC – Ríos del Desierto S.A.S.**, compuesta por:

- Un **backend** en Python (preferiblemente **Django** o **Flask**) que exponga una API REST.
- Un **frontend web** sencillo que consuma esa API.

## 0.1 Objetivo funcional

A partir de un **tipo de documento** y un **número de documento** de un cliente, el sistema debe:

1. Consultar al cliente en la base de datos.
2. Mostrar sus **datos básicos** (nombre, documento, contacto).
3. Listar sus **compras**.
4. Permitir **exportar** la información del cliente y sus compras a **CSV**.
5. Generar un **reporte de clientes fidelizados** en Excel, considerando:
   - Compras del **último mes / últimos 30 días**.
   - Clientes cuyo total de compras en ese periodo supere un umbral (por ejemplo, **5.000.000 COP**).

## 0.2 Entregables solicitados

De acuerdo con la descripción de la prueba, se esperan al menos los siguientes entregables:

1. **Guía de Implementación** (paso a paso para instalar y desplegar la solución en un ambiente productivo).
2. **Código fuente en un repositorio Git** (GitHub/GitLab/Azure DevOps, etc.).
3. **Documentación técnica básica** del backend (modelo de datos, endpoints, tecnologías).
4. **Video corto** explicando funcionamiento de la aplicación y los módulos desarrollados.
5. **Base de datos implementada** con datos de prueba suficientes para demostrar:
   - Búsqueda de un cliente real.
   - Compras recientes que permitan probar el reporte de fidelización.

## 0.3 Consideraciones técnicas de la prueba

- Se recomienda el uso de **Django** o **Flask** para el backend.
- Para la automatización y cálculos se valora el uso de **pandas**.
- Se valora el uso de un **ORM** (Django ORM en este caso) en lugar de armar toda la base de datos “a mano”.
- Se penaliza un modelo de datos excesivamente simple:
  - Solo 2 tablas (por ejemplo, `Users` y `Purchases`) **no es suficiente**.
  - Se espera un modelo algo más elaborado (tipos de documento, clientes, compras, etc.).
- El frontend debe consumir realmente la API, no “simular” datos.

Este backend en Django cumple con esos lineamientos y se integra con el resto de entregables de la prueba.

---

# 1. Descripción General del Proyecto

El backend desarrollado en **Django + Django REST Framework** implementa las funcionalidades de la herramienta SAC Ríos del Desierto:

1. Consultar un cliente por tipo y número de documento.  
2. Obtener el historial de compras del cliente.  
3. Exportar los datos en **CSV**.  
4. Generar un reporte de **clientes fidelizados** en formato **Excel** usando `openpyxl` (o librería similar).  
5. Dar servicio a un frontend HTML/JS mediante consumo por HTTP.  

Por defecto, la base de datos es **SQLite**, pero la guía de despliegue contempla PostgreSQL o SQL Server según el entorno.

---

# 2. Requisitos Previos

## 2.1 Entorno local (desarrollo)

- Python 3.10+
- pip
- Git  
- Navegador web  
Opcionales:
- SQLite (incluida por defecto con Django)
- Postman o similar para pruebas de API

## 2.2 Entorno productivo

- Servidor Linux (Ubuntu)
- Python 3 + `venv` + `pip`
- Gunicorn
- Nginx
- Base de datos PostgreSQL o SQL Server (o SQLite para pruebas)

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

## 3.4 Configuración de Django (settings.py)

Por defecto se usa SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

En producción se puede cambiar a PostgreSQL o SQL Server leyendo variables de entorno.

## 3.5 Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## 3.6 Usuario administrador

```bash
python manage.py createsuperuser
```

Ingresar luego a:

```
http://127.0.0.1:8000/admin/
```

## 3.7 Carga de datos de prueba

Crear:

- Tipos de documento: `CC`, `NIT`, `PAS`.
- Uno o varios clientes con compras recientes (> 5.000.000 COP en últimos 30 días) para probar el reporte de fidelización.

## 3.8 Ejecutar el servidor en desarrollo

```bash
python manage.py runserver
```

---

# 4. Endpoints de la API

## 4.1 Buscar cliente

```
GET /api/client/search/?document_type=CC&document_number=123456789
```

Devuelve los datos del cliente y su lista de compras.

## 4.2 Exportar cliente (CSV)

```
GET /api/client/export/?document_type=CC&document_number=123456789
```

Genera un CSV con la información del cliente y sus compras.

## 4.3 Reporte de fidelización (Excel)

```
GET /api/reports/loyal-customers/
```

Genera un archivo Excel con los clientes cuyo total de compras del último mes supere el umbral definido (por ejemplo, 5M COP).

---

# 5. Frontend esperado

El frontend (HTML + JS) debe incluir como mínimo:

- Select de **tipo de documento**.
- Campo de **número de documento**.
- Botón **Buscar** → llama a `/api/client/search/`.
- Botón **Exportar** → descarga el CSV vía `/api/client/export/`.
- Botón/acción para descargar el **reporte de fidelización** (Excel).

---

# 6. Estructura sugerida del proyecto

```text
rios-desierto-sac/
  manage.py
  requirements.txt
  Guia_Implementacion.md
  rios_desierto/        # settings, urls, wsgi, etc.
  customers/            # app de clientes/compras
  templates/            # HTML si se usan vistas renderizadas
  db.sqlite3
```

---

# 7. Configuración de Variables de Entorno (Producción)

En producción no se deben hardcodear secretos en `settings.py`. Se recomiendan variables como:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS="mi-dominio.com,localhost"`
- Variables de la BD: `DJANGO_DB_NAME`, `DJANGO_DB_USER`, etc.

Ejemplo rápido:

```bash
export DJANGO_SECRET_KEY="clave_secreta"
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS="mi-dominio.com,localhost"
```

---

# 8. Guía de Despliegue en Ambiente Productivo (Ubuntu + Gunicorn + Nginx)

A continuación se resume el despliegue típico en un servidor único (VPS u on-premise).

## 8.1 Preparar el servidor

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip nginx
```

Si usas PostgreSQL:

```bash
sudo apt install -y postgresql postgresql-contrib libpq-dev
```

## 8.2 Descargar código en `/opt`

```bash
cd /opt
sudo git clone https://github.com/tu-usuario/sac-rios-desierto-django.git
sudo chown -R $USER:$USER sac-rios-desierto-django
cd sac-rios-desierto-django
```

## 8.3 Crear entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 8.4 Migraciones y estáticos

```bash
python manage.py migrate
python manage.py collectstatic
```

## 8.5 Probar backend con Gunicorn

```bash
gunicorn rios_desierto.wsgi:application --bind 0.0.0.0:8000
```

---

# 9. Crear servicio systemd para Gunicorn

Archivo de servicio:

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

Activar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn-rios-desierto
sudo systemctl enable gunicorn-rios-desierto
sudo systemctl status gunicorn-rios-desierto
```

---

# 10. Configuración de Nginx como reverse proxy

```bash
sudo nano /etc/nginx/sites-available/rios-desierto
```

Contenido:

```nginx
server {
    listen 80;
    server_name mi-dominio.com;

    # Archivos estáticos de Django
    location /static/ {
        alias /opt/sac-rios-desierto-django/staticfiles/;
    }

    # Frontend estático (HTML + JS)
    location / {
        root /opt/sac-rios-desierto-frontend;
        try_files $uri /index.html;
    }

    # Proxy para la API Django
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar sitio y reiniciar Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/rios-desierto /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

# 11. HTTPS con Certbot (opcional pero recomendado)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d mi-dominio.com
```

---

# 12. Arquitectura Final en Producción

| Componente | Rol |
|-----------|-----|
| **Nginx** | Entrada HTTP/HTTPS, archivos estáticos, proxy hacia Gunicorn |
| **Gunicorn** | Servidor WSGI que ejecuta Django |
| **Django + DRF** | Lógica de negocio, endpoints REST, generación CSV/Excel |
| **Base de datos** | Persistencia de clientes, tipos de documento, compras |

---

# 13. Resumen para la Entrevista / Defensa

- Se implementa exactamente lo pedido en la **prueba técnica**:  
  - Consulta de clientes por documento.  
  - Listado de compras.  
  - Exportación a CSV.  
  - Reporte de fidelización en Excel.  
- Se usan tecnologías recomendadas: **Django**, **Django REST Framework**, **pandas/openpyxl**, **ORM**.
- El modelo de datos va más allá de 2 tablas y es fácilmente extensible.
- La solución está lista para ejecutarse:
  - En **desarrollo** con `runserver`.
  - En **producción** con **Gunicorn + Nginx**.

Este documento sirve tanto como **README del repositorio** como **Guía de Implementación** y base para explicar la arquitectura en una presentación técnica.

---

# Fin del documento
