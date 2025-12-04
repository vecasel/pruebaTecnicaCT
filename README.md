
# Guía de Implementación  
**Proyecto:** Herramienta de consultas SAC – Ríos del Desierto S.A.S.  
**Backend:** Python (Django + Django REST Framework + SQLite)  
**Frontend:** Página web que consume la API vía HTTP  

---

## 1. Requisitos previos

Para instalar y ejecutar el proyecto:

- Python 3.10+
- pip
- Git
- Navegador web  
Opcionales:
- Gunicorn + Nginx para productivo
- Docker

---

## 2. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/rios-desierto-sac.git
cd rios-desierto-sac
```

---

## 3. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
```

Activar:

**Windows**
```bash
.\venv\Scripts\activate
```

**Linux/macOS**
```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Si el archivo no existe:

```bash
pip install django djangorestframework pandas openpyxl
```

---

## 4. Configuración de Django

La configuración principal se encuentra en `rios_desierto/settings.py`.

SQLite se usa por defecto:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 5. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Usuario administrador

```bash
python manage.py createsuperuser
```

Ingresar a:

```
http://127.0.0.1:8000/admin/
```

---

## 7. Carga de datos de prueba

Crear:

- Tipos de documento: CC, NIT, PAS
- Cliente con compras recientes > 5.000.000 COP en últimos 30 días

---

## 8. Ejecutar el servidor

```bash
python manage.py runserver
```

---

## 9. Endpoints de la API

### 9.1 Buscar cliente

```
GET /api/client/search/?document_type=CC&document_number=123456789
```

### 9.2 Exportar cliente (CSV)

```
GET /api/client/export/?document_type=CC&document_number=123456789
```

### 9.3 Reporte de fidelización (Excel)

```
GET /api/reports/loyal-customers/
```

Genera archivo Excel con clientes que superen 5M COP en compras del último mes.

---

## 10. Frontend

Debe incluir:

- Select de tipo documento
- Campo número documento
- Button Buscar → llama `/api/client/search/`
- Button Exportar → descarga CSV

---

## 11. Despliegue productivo (resumen)

1. Clonar repo en servidor
2. Crear entorno virtual
3. Instalar dependencias
4. Migrar base
5. Crear usuario admin
6. Ejecutar con gunicorn:

```bash
gunicorn rios_desierto.wsgi:application --bind 0.0.0.0:8000
```

7. Configurar Nginx como proxy reverso

---

## 12. Estructura sugerida del proyecto

```
rios-desierto-sac/
  manage.py
  requirements.txt
  Guia_Implementacion.md
  rios_desierto/
  customers/
  templates/
  db.sqlite3
```

---

## 13. Créditos

Documento generado como parte de la prueba técnica de Falabella – Ingeniero de Desarrollo.
