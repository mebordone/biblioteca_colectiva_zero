# Plan de Despliegue: Biblioteca Colectiva en PythonAnywhere

Este documento detalla el proceso paso a paso para desplegar la rama `dev` en PythonAnywhere con configuración de emails usando **Mailgun**.

> **Nota:** Este plan está basado en el tutorial de Django Girls: https://tutorial.djangogirls.org/es/deploy/

---

## Fase 1: Preparación Local (Antes de Desplegar)

### 1.1 Verificar Estado del Repositorio

```bash
# Asegúrate de estar en la rama dev
git checkout dev
git pull origin dev

# Verifica que no haya cambios sin commitear
git status
```

### 1.2 Verificar que `.gitignore` Incluya Archivos Sensibles

El `.gitignore` ya incluye:
- `.env` ✓
- `db.sqlite3` ✓
- `__pycache__` ✓
- `staticfiles/` (verificar si es necesario agregarlo)

### 1.3 Asegurar que `staticfiles/` esté en `.gitignore`

Agregar a `.gitignore` si no está:
```
staticfiles/
```

### 1.4 Verificar que `requirements.txt` esté Actualizado

Ya incluye:
- Django>=5.1.4
- django-environ>=0.11.0
- openpyxl>=3.1.0
- pytest y dependencias

### 1.5 Hacer Commit y Push de Cambios Pendientes

```bash
# Si hay cambios, hacer commit
git add .
git commit -m "chore: preparar para despliegue en PythonAnywhere"
git push origin dev
```

---

## Fase 2: Configuración de Mailgun (Servicio de Email)

### ⚠️ IMPORTANTE: PythonAnywhere y SMTP

**PythonAnywhere bloquea conexiones SMTP salientes en planes gratuitos.** Por lo tanto:
- ❌ **NO podemos usar SMTP** (Gmail, Mailgun SMTP, etc.)
- ✅ **SÍ podemos usar la API HTTP de Mailgun** (compatible con PythonAnywhere)

El proyecto usa `django-anymail` que permite usar la API HTTP de Mailgun en lugar de SMTP.

### 2.1 Crear Cuenta en Mailgun

1. Ir a https://www.mailgun.com/
2. Registrarse (plan gratuito disponible: 100 emails/día)
3. Verificar el email de registro

### 2.2 Configurar Dominio

**Opción A: Usar Dominio Sandbox (Para Pruebas)**
- Mailgun proporciona un dominio sandbox automáticamente
- Formato: `sandboxXXXXX.mailgun.org`
- Puedes enviar emails a direcciones autorizadas (debes agregarlas en Mailgun)
- Ideal para pruebas iniciales

**Opción B: Verificar Tu Propio Dominio (Para Producción)**
1. En Mailgun: **Sending** → **Domains** → **Add New Domain**
2. Ingresa tu dominio (ej: `bibliotecacolectiva.com`)
3. Sigue las instrucciones para verificar el dominio
4. Configura los registros DNS según las instrucciones

### 2.3 Obtener API Key de Mailgun

1. En Mailgun: **Sending** → **API Keys**
2. Copia tu **API Key** (o crea una nueva si prefieres)
3. Anota tu **Sender Domain**:
   - Si usas sandbox: `sandboxXXXXX.mailgun.org`
   - Si usas dominio propio: `mg.bibliotecacolectiva.com` o el dominio que configuraste

**Formato de credenciales para API:**
- **API Key:** `key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (formato que te da Mailgun)
- **Sender Domain:** `sandboxXXXXX.mailgun.org` o `mg.tu-dominio.com`

---

## Fase 3: Configuración en GitHub

### 3.1 Verificar que la Rama `dev` esté en GitHub

```bash
# Verificar que dev esté en origin
git branch -r | grep dev

# Si no está, hacer push
git push origin dev
```

### 3.2 Obtener la URL del Repositorio

- URL de clonación: `https://github.com/<tu-usuario>/biblioteca_colectiva_zero.git`
- URL de la rama dev: `https://github.com/<tu-usuario>/biblioteca_colectiva_zero.git` (branch: dev)

---

## Fase 4: Configuración en PythonAnywhere

### 4.1 Crear Cuenta en PythonAnywhere

1. Ir a https://www.pythonanywhere.com/
2. Crear cuenta "Beginner" (gratis)
3. Elegir nombre de usuario (la URL será `tuusuario.pythonanywhere.com`)

### 4.2 Crear API Token de PythonAnywhere

1. En el dashboard: **Account** → **API token**
2. **Create new API token**
3. Copiar el token (solo se muestra una vez)

### 4.3 Instalar Herramienta de Autoconfiguración

1. Abrir una consola **Bash** en PythonAnywhere
2. Instalar la herramienta:
```bash
pip3.10 install --user pythonanywhere
```

### 4.4 Ejecutar Autoconfiguración de Django

En la consola de PythonAnywhere:
```bash
# Reemplaza <tu-usuario-github> con tu usuario de GitHub
pa_autoconfigure_django.py --python=3.10 https://github.com/<tu-usuario-github>/biblioteca_colectiva_zero.git --branch=dev
```

**Nota:** Si `pa_autoconfigure_django.py` no soporta `--branch`, clonar manualmente la rama dev.

### 4.5 Si el Autoconfigurador no Soporta Ramas

```bash
# Clonar manualmente
cd ~
git clone -b dev https://github.com/<tu-usuario-github>/biblioteca_colectiva_zero.git
cd biblioteca_colectiva_zero/libro_prestamos

# Crear virtualenv
python3.10 -m venv myvenv
source myvenv/bin/activate

# Instalar dependencias
pip install --user -r ../requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

---

## Fase 5: Configuración de Variables de Entorno en PythonAnywhere

### 5.1 Crear Archivo `.env` en PythonAnywhere

1. En PythonAnywhere: **Files** → navegar a `~/biblioteca_colectiva_zero/`
2. Crear archivo `.env` con este contenido:

```env
# Django Settings
SECRET_KEY=tu_secret_key_generada_aqui
DEBUG=False
ALLOWED_HOSTS=tuusuario.pythonanywhere.com

# Email Configuration - Mailgun vía API HTTP (NO SMTP)
# IMPORTANTE: PythonAnywhere bloquea SMTP, por eso usamos API HTTP
EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
MAILGUN_API_KEY=key-tu_api_key_de_mailgun
MAILGUN_SENDER_DOMAIN=sandboxXXXXX.mailgun.org
DEFAULT_FROM_EMAIL=noreply@bibliotecacolectiva.com
```

**Para dominio propio verificado:**
```env
MAILGUN_SENDER_DOMAIN=mg.bibliotecacolectiva.com
```

**Nota:** 
- `MAILGUN_API_KEY`: Obténla de Mailgun → Sending → API Keys
- `MAILGUN_SENDER_DOMAIN`: Tu dominio sandbox o verificado en Mailgun

### 5.2 Generar SECRET_KEY

En la consola de PythonAnywhere:
```bash
cd ~/biblioteca_colectiva_zero/libro_prestamos
source ../myvenv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar el resultado y pegarlo en `.env` como `SECRET_KEY=...`

### 5.3 Configurar Mailgun en `.env`

- `MAILGUN_API_KEY`: La API Key de Mailgun (formato `key-xxxxx...`)
- `MAILGUN_SENDER_DOMAIN`: Tu dominio sandbox o verificado (ej: `sandboxXXXXX.mailgun.org`)
- `DEFAULT_FROM_EMAIL`: Email verificado en Mailgun o `noreply@bibliotecacolectiva.com`

**Importante:** Si usas el dominio sandbox, debes agregar las direcciones de email autorizadas en Mailgun:
1. Ve a **Sending** → **Authorized Recipients**
2. Agrega las direcciones de email a las que quieres enviar
3. Verifica cada email (te llegará un email de verificación)

---

## Fase 6: Configuración de la Aplicación Web en PythonAnywhere

### 6.1 Configurar la Aplicación Web

1. En PythonAnywhere: **Web**
2. **Add a new web app** → **Manual configuration** → **Python 3.10**
3. **Source code:** `/home/tuusuario/biblioteca_colectiva_zero/libro_prestamos`
4. **Working directory:** `/home/tuusuario/biblioteca_colectiva_zero/libro_prestamos`

### 6.2 Configurar WSGI

1. En **Web** → **WSGI configuration file**
2. Editar el archivo WSGI y reemplazar con:

```python
import os
import sys

# Añadir el directorio del proyecto al path
path = '/home/tuusuario/biblioteca_colectiva_zero/libro_prestamos'
if path not in sys.path:
    sys.path.insert(0, path)

# Añadir el directorio del virtualenv al path
venv_path = '/home/tuusuario/biblioteca_colectiva_zero/myvenv'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'libro_prestamos.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6.3 Configurar Archivos Estáticos

1. En **Web** → **Static files**
2. Agregar:
   - **URL:** `/static/`
   - **Directory:** `/home/tuusuario/biblioteca_colectiva_zero/libro_prestamos/staticfiles/`

### 6.4 Recopilar Archivos Estáticos

En la consola:
```bash
cd ~/biblioteca_colectiva_zero/libro_prestamos
source ../myvenv/bin/activate
python manage.py collectstatic --noinput
```

---

## Fase 7: Configuración de Base de Datos

### 7.1 Ejecutar Migraciones

```bash
cd ~/biblioteca_colectiva_zero/libro_prestamos
source ../myvenv/bin/activate
python manage.py migrate
```

### 7.2 Crear Superusuario

```bash
python manage.py createsuperuser
```

---

## Fase 8: Verificación y Pruebas

### 8.1 Recargar la Aplicación Web

1. En PythonAnywhere: **Web** → **Reload**
2. Esperar unos segundos

### 8.2 Verificar que el Sitio Funciona

1. Visitar `https://tuusuario.pythonanywhere.com/`
2. Verificar que carga correctamente

### 8.3 Probar el Sistema de Emails con Mailgun

1. **Si usas dominio sandbox:**
   - Ve a Mailgun → **Sending** → **Authorized Recipients**
   - Agrega tu email de prueba
   - Verifica el email de autorización que te llegue

2. **Probar envío de emails:**
   - Ir a `/login/`
   - Clic en "¿Olvidaste tu contraseña?"
   - Ingresar un email válido (debe estar autorizado si usas sandbox)
   - Verificar que llegue el email (revisar spam si no aparece)

3. **Probar otras funcionalidades de email:**
   - Probar cambio de email (si está implementado)
   - Probar cambio de contraseña
   - Verificar que los enlaces funcionen correctamente

### 8.4 Verificar Logs en Caso de Errores

1. En PythonAnywhere: **Web** → **Error log**
2. Revisar errores recientes

### 8.5 Verificar Logs de Mailgun

1. En Mailgun: **Sending** → **Logs**
2. Verificar que los emails se estén enviando correctamente
3. Revisar si hay errores de entrega

---

## Fase 9: Configuración Adicional de Seguridad

### 9.1 Verificar que DEBUG=False

Confirmar en `.env`:
```env
DEBUG=False
```

### 9.2 Verificar ALLOWED_HOSTS

En `.env`:
```env
ALLOWED_HOSTS=tuusuario.pythonanywhere.com
```

### 9.3 Verificar que `.env` no esté en el Repositorio

```bash
# En local, verificar
git ls-files | grep .env
# No debería mostrar nada
```

---

## Fase 10: Documentación y Mantenimiento

### 10.1 Documentar Credenciales (de Forma Segura)

- Guardar credenciales en un gestor de contraseñas
- No commitear credenciales

### 10.2 Flujo de Trabajo para Actualizaciones

```bash
# 1. En local, hacer cambios y commitear
git checkout dev
# ... hacer cambios ...
git add .
git commit -m "feat: nueva funcionalidad"
git push origin dev

# 2. En PythonAnywhere, actualizar código
cd ~/biblioteca_colectiva_zero
git pull origin dev

# 3. Recargar aplicación
# En Web → Reload
```

---

## Checklist Final

- [ ] Código en GitHub (rama `dev`)
- [ ] Cuenta en Mailgun creada y verificada
- [ ] API Key de Mailgun obtenida (NO SMTP - PythonAnywhere bloquea SMTP)
- [ ] Dominio configurado (sandbox o propio)
- [ ] `django-anymail` instalado en PythonAnywhere
- [ ] Cuenta en PythonAnywhere creada
- [ ] Aplicación Django configurada en PythonAnywhere
- [ ] Archivo `.env` creado con todas las variables (API Key, no SMTP)
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recopilados
- [ ] Sitio web accesible
- [ ] Sistema de emails funcionando (probar reset de contraseña)
- [ ] DEBUG=False en producción
- [ ] ALLOWED_HOSTS configurado correctamente

---

## Notas Importantes

1. **Mailgun:** Plan gratuito permite 100 emails/día. Suficiente para pruebas y uso inicial.
2. **PythonAnywhere:** Plan gratuito tiene limitaciones (1 app web, dominio `.pythonanywhere.com`).
3. **PythonAnywhere bloquea SMTP:** Por eso usamos la API HTTP de Mailgun (compatible con PythonAnywhere).
4. **Base de datos:** SQLite en el plan gratuito. Para producción con más tráfico, considerar MySQL/PostgreSQL.
5. **Seguridad:** Nunca commitear `.env` ni credenciales.
6. **Logs:** Revisar los logs de PythonAnywhere y Mailgun si hay errores.
7. **Dominio Sandbox:** Solo puedes enviar a emails autorizados. Para producción, verifica tu propio dominio.
8. **django-anymail:** Necesario para usar la API HTTP de Mailgun. Ya está en `requirements.txt`.

---

## Troubleshooting

### Emails no llegan con dominio sandbox

**Solución:** Asegúrate de agregar el email destinatario en Mailgun → **Sending** → **Authorized Recipients** y verificar el email.

### Error de autenticación con API de Mailgun

**Solución:** 
1. Verifica que `MAILGUN_API_KEY` sea correcta (formato `key-xxxxx...`)
2. Verifica que `MAILGUN_SENDER_DOMAIN` sea correcto (ej: `sandboxXXXXX.mailgun.org`)
3. Asegúrate de que `EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend` esté configurado
4. Verifica en Mailgun que la API Key esté activa

### Error "Connection refused" o timeout

**Solución:**
1. Verifica que estés usando la **API HTTP** (no SMTP): `EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend`
2. Verifica que `MAILGUN_API_KEY` y `MAILGUN_SENDER_DOMAIN` estén configurados correctamente
3. PythonAnywhere permite conexiones HTTP/HTTPS, pero bloquea SMTP - asegúrate de no estar usando SMTP

### Error "django-anymail not installed"

**Solución:**
```bash
cd ~/biblioteca_colectiva_zero/libro_prestamos
source ../myvenv/bin/activate
pip install --user django-anymail
```

### Error "Invalid API key" o "Forbidden"

**Solución:**
1. Verifica que la API Key sea correcta en Mailgun
2. Asegúrate de que la API Key tenga permisos de envío
3. Verifica que el dominio esté correctamente configurado en Mailgun

---

## Referencias

- [Tutorial Django Girls - Despliegue](https://tutorial.djangogirls.org/es/deploy/)
- [Documentación de Mailgun](https://documentation.mailgun.com/)
- [Configuración de Email - Biblioteca Colectiva](./CONFIGURACION_EMAIL.md)
