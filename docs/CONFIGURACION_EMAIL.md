# Configuración de Email - Biblioteca Colectiva

Esta guía explica cómo configurar el sistema de envío de emails para desarrollo local y producción en PythonAnywhere.

## Tabla de Contenidos

1. [Configuración Local con Gmail](#configuración-local-con-gmail)
2. [Configuración en PythonAnywhere](#configuración-en-pythonanywhere)
3. [Troubleshooting](#troubleshooting)
4. [Alternativas para Producción](#alternativas-para-producción)

---

## Opción 1: Desarrollo Local sin Email Real (Recomendado para empezar)

**Esta es la opción más fácil para desarrollo local.** Los emails se mostrarán en la consola/terminal, no se envían realmente.

### Configuración Automática

El sistema está configurado para usar el backend de consola por defecto en desarrollo. **No necesitas configurar nada**, simplemente:

1. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

2. Cuando se envíe un email (cambio de contraseña, etc.), verás el contenido completo en la terminal donde corre el servidor.

3. Puedes copiar el enlace del email desde la terminal y usarlo directamente.

**Ventajas:**
- ✅ No requiere configuración
- ✅ No necesita cuenta de email
- ✅ Perfecto para desarrollo y testing
- ✅ Ve el contenido completo del email

---

## Opción 2: Configuración Local con Gmail

**Nota importante:** Google ya NO permite usar contraseñas normales. Debes usar "Contraseñas de aplicación" que requieren verificación en 2 pasos activada.

### Paso 1: Crear cuenta de Gmail (si no existe)

1. Crea una cuenta de Gmail: `bibliotecacolectivazero@gmail.com`
2. Inicia sesión en la cuenta

### Paso 2: Habilitar Verificación en 2 Pasos (OBLIGATORIO)

1. Ve a [Mi Cuenta de Google](https://myaccount.google.com/)
2. Selecciona **Seguridad** en el menú lateral
3. Busca **Verificación en 2 pasos** y actívala
   - Sigue las instrucciones para configurarla
   - **Nota:** Esto es obligatorio - sin esto NO puedes generar contraseñas de aplicación

### Paso 3: Generar Contraseña de Aplicación

1. En la misma página de **Seguridad**, busca **Contraseñas de aplicaciones**
2. Si no la ves, busca "Verificación en 2 pasos" y haz clic en "Contraseñas de aplicaciones"
3. Selecciona:
   - **Aplicación:** Correo
   - **Dispositivo:** Otro (personalizado) - escribe "Django Local"
4. Haz clic en **Generar**
5. **Copia la contraseña de 16 caracteres** que aparece (no podrás verla de nuevo)

**⚠️ IMPORTANTE:** No puedes usar tu contraseña normal de Gmail. Google bloqueó esto desde mayo de 2022.

### Paso 4: Configurar Variables de Entorno (Opcional)

**Solo si quieres enviar emails reales en desarrollo local:**

1. En la raíz del proyecto, crea un archivo `.env` (si no existe)
2. Edita el archivo `.env` y agrega:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=bibliotecacolectivazero@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # La contraseña de aplicación de 16 caracteres (sin espacios)
   DEFAULT_FROM_EMAIL=bibliotecacolectivazero@gmail.com
   ```
   **Importante:** En `EMAIL_HOST_PASSWORD` pega la contraseña de aplicación sin espacios

**Si NO creas el archivo `.env`, el sistema usará automáticamente el backend de consola (emails en terminal).**

### Paso 5: Verificar Instalación

1. Asegúrate de tener `django-environ` instalado:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
3. Prueba el envío de email:
   - Ve a la página de login
   - Haz clic en "¿Olvidaste tu contraseña?"
   - Ingresa un email de prueba
   - Revisa la consola (si usas backend de consola) o tu bandeja de entrada

---

## Configuración en PythonAnywhere

### Opción 1: Variables de Entorno (Recomendado)

1. Inicia sesión en [PythonAnywhere](https://www.pythonanywhere.com/)
2. Ve a la pestaña **Web**
3. Busca la sección **Environment variables**
4. Agrega las siguientes variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=bibliotecacolectivazero@gmail.com
   EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
   DEFAULT_FROM_EMAIL=bibliotecacolectivazero@gmail.com
   ```
5. Haz clic en **Reload** en la parte superior de la página

### Opción 3: Archivo de Configuración (Menos Seguro - No Recomendado)

Si prefieres no usar variables de entorno (no recomendado):

1. Crea un archivo `settings_production.py` en `libro_prestamos/libro_prestamos/`
2. Agrega la configuración de email (usando API de Mailgun):
   ```python
   # Para PythonAnywhere - Usar API HTTP
   EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
   ANYMAIL = {
       "MAILGUN_API_KEY": "tu_api_key_de_mailgun",
       "MAILGUN_SENDER_DOMAIN": "tu-dominio.mailgun.org",
   }
   DEFAULT_FROM_EMAIL = 'noreply@bibliotecacolectiva.com'
   ```
3. Importa en `settings.py`:
   ```python
   try:
       from .settings_production import *
   except ImportError:
       pass
   ```
4. **IMPORTANTE:** Agrega `settings_production.py` a `.gitignore` para no commitear credenciales

### Verificar en PythonAnywhere

1. Ve a la consola de PythonAnywhere
2. Ejecuta:
   ```python
   python manage.py shell
   ```
3. Prueba el envío:
   ```python
   from django.core.mail import send_mail
   send_mail('Test', 'Mensaje de prueba', 'bibliotecacolectivazero@gmail.com', ['tu_email@ejemplo.com'])
   ```
4. Revisa tu bandeja de entrada

---

## Troubleshooting

### Error: "SMTPAuthenticationError"

**Causa:** La contraseña de aplicación es incorrecta o no está configurada.

**Solución:**
1. Verifica que estés usando una **contraseña de aplicación**, no tu contraseña normal de Gmail
2. Genera una nueva contraseña de aplicación
3. Asegúrate de que la verificación en 2 pasos esté activada

### Error: "Connection refused" o timeout

**Causa:** Problemas de red o firewall.

**Solución:**
1. Verifica tu conexión a internet
2. En PythonAnywhere, asegúrate de que el servidor web esté activo
3. Verifica que el puerto 587 no esté bloqueado

### Los emails no llegan

**Causa:** Varias posibles.

**Solución:**
1. Revisa la carpeta de spam
2. Verifica que el email del destinatario sea correcto
3. Revisa los logs de Django para errores
4. En desarrollo, usa el backend de consola para ver los emails en la terminal:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

### Error: "Less secure app access"

**Causa:** Google bloqueó el acceso de aplicaciones menos seguras (ya no disponible).

**Solución:** Debes usar **Contraseñas de aplicaciones**, no la opción de "aplicaciones menos seguras".

### Límites de Gmail

Gmail tiene límites de envío:
- **Cuenta gratuita:** ~500 emails/día
- **Por minuto:** ~100 emails/minuto

Si necesitas enviar más emails, considera usar un servicio profesional (ver sección siguiente).

---

## Opción 3: Servicios de Email Profesionales (Recomendado para Producción)

Si no quieres lidiar con Gmail y verificación en 2 pasos, estos servicios son más fáciles de configurar:

### Mailgun (Recomendado para empezar)

**Ventajas:**
- ✅ Gratis hasta 100 emails/día (plan gratuito)
- ✅ Fácil de configurar (solo necesitas API Key)
- ✅ No requiere verificación en 2 pasos
- ✅ API RESTful (HTTP/HTTPS) - compatible con PythonAnywhere
- ✅ Buena documentación
- ✅ Ideal para desarrollo y producción
- ✅ **Funciona en PythonAnywhere** (usa API HTTP, no SMTP bloqueado)

**⚠️ IMPORTANTE: PythonAnywhere y SMTP**
- PythonAnywhere **bloquea conexiones SMTP salientes** en planes gratuitos
- Por eso usamos la **API HTTP de Mailgun** en lugar de SMTP
- El proyecto usa `django-anymail` que permite usar la API HTTP de Mailgun

**Configuración:**
1. Regístrate en [Mailgun](https://www.mailgun.com/) (plan gratuito disponible)
2. Una vez registrado, ve a tu dashboard
3. Selecciona tu dominio (o usa el dominio de prueba `sandbox` que viene por defecto)
4. Ve a **Sending** → **API Keys**
5. Copia tu **API Key** (o crea una nueva si prefieres)
6. Anota tu **Sender Domain** (ej: `mg.bibliotecacolectiva.com` o `sandboxXXXXX.mailgun.org`)
7. Configura en `.env`:
   ```env
   # Para producción (PythonAnywhere) - Usa API HTTP, NO SMTP
   EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=tu_api_key_de_mailgun
   MAILGUN_SENDER_DOMAIN=tu-dominio.mailgun.org
   DEFAULT_FROM_EMAIL=noreply@bibliotecacolectiva.com
   ```
   **Nota:** Si usas el dominio sandbox de Mailgun, el formato será `sandboxXXXXX.mailgun.org` donde XXXXX es tu código de sandbox.

8. Verifica tu dominio (opcional pero recomendado para producción) o usa el dominio sandbox para pruebas

**Dominio Sandbox de Mailgun:**
- Mailgun proporciona un dominio sandbox gratuito para pruebas
- Puedes enviar emails a direcciones autorizadas (debes agregarlas en Mailgun)
- Para producción, verifica tu propio dominio

**Configuración Alternativa (SMTP - Solo si NO usas PythonAnywhere):**
Si estás desplegando en otro servidor que SÍ permite SMTP, puedes usar:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@tu-dominio.mailgun.org
EMAIL_HOST_PASSWORD=tu_contraseña_smtp_de_mailgun
DEFAULT_FROM_EMAIL=noreply@bibliotecacolectiva.com
```
Pero para PythonAnywhere, **debes usar la API HTTP** (configuración anterior).

### Amazon SES

**Ventajas:**
- Muy económico ($0.10 por 1,000 emails)
- Escalable
- Requiere verificación de dominio

### SendGrid (Ya no ofrece plan gratuito)

**Nota:** SendGrid eliminó su plan gratuito. Si ya tienes una cuenta, puedes seguir usándola, pero para nuevos proyectos se recomienda Mailgun.

### Email del Dominio Propio

Si tienes un dominio (ej: `bibliotecacolectiva.com`):

1. Contrata hosting con email (o usa Google Workspace)
2. Configura registros MX del dominio
3. Usa las credenciales SMTP del proveedor de email

---

## Seguridad

### Buenas Prácticas

1. **Nunca commitees** archivos `.env` o `settings_production.py` con credenciales
2. **Usa variables de entorno** en producción
3. **Rota las contraseñas** periódicamente
4. **Usa contraseñas de aplicación** para Gmail, nunca la contraseña principal
5. **Limita el acceso** a las credenciales de email

### Verificación

Para verificar que la configuración es segura:

1. Revisa que `.env` esté en `.gitignore`
2. Verifica que no haya credenciales hardcodeadas en el código
3. Usa diferentes credenciales para desarrollo y producción

---

## Próximos Pasos

Una vez configurado el email:

1. Prueba el flujo completo de cambio de contraseña
2. Verifica que los emails lleguen correctamente
3. Revisa que los enlaces funcionen con tu dominio
4. Considera implementar un servicio profesional cuando tengas más usuarios

---

## Soporte

Si tienes problemas:

1. Revisa los logs de Django
2. Verifica la configuración paso a paso
3. Prueba con el backend de consola primero
4. Consulta la documentación de Django sobre email: https://docs.djangoproject.com/en/stable/topics/email/
