# Guía de Testing Local - Cambio de Contraseña

## Configuración Actual

✅ **Modo Consola Activado**: Los emails se mostrarán en la terminal, no se envían realmente.
✅ **Migraciones Aplicadas**: El modelo `PasswordResetToken` está listo.
✅ **Sin Configuración Necesaria**: No necesitas crear archivo `.env` para desarrollo.

---

## Pasos para Probar el Sistema

### 1. Iniciar el Servidor

```bash
cd libro_prestamos
source ../.venv/bin/activate  # Si no está activado
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

### 2. Crear un Usuario de Prueba (si no tienes uno)

1. Ve a: `http://127.0.0.1:8000/registro/`
2. Completa el formulario de registro
3. Inicia sesión con el usuario creado

### 3. Probar Cambio de Contraseña desde Login

**Flujo: Usuario NO autenticado**

1. Ve a: `http://127.0.0.1:8000/login/`
2. Haz clic en **"¿Olvidaste tu contraseña?"**
3. Ingresa el email del usuario de prueba
4. Haz clic en **"Enviar Enlace"**

**Lo que verás:**
- En la **terminal** donde corre el servidor, aparecerá el email completo con el enlace
- Copia el enlace que aparece en la terminal (algo como: `http://127.0.0.1:8000/password/confirmar/TOKEN_AQUI/`)
- Abre ese enlace en el navegador
- Ingresa la nueva contraseña
- Confirma el cambio

### 4. Probar Cambio de Contraseña desde Perfil

**Flujo: Usuario autenticado**

1. Inicia sesión
2. Ve a: `http://127.0.0.1:8000/perfil/`
3. En la sección **"Seguridad"**, haz clic en **"Cambiar Contraseña"**
4. Ingresa:
   - Contraseña actual
   - Nueva contraseña
   - Confirmar nueva contraseña
5. Haz clic en **"Solicitar Cambio"**

**Lo que verás:**
- Mensaje de confirmación en la página
- En la **terminal**, aparecerá el email con el enlace de confirmación
- Copia el enlace de la terminal y ábrelo
- La contraseña se cambiará automáticamente (ya validaste la contraseña actual)

### 5. Verificar que Funciona

1. Cierra sesión
2. Intenta iniciar sesión con la **nueva contraseña**
3. Deberías poder iniciar sesión correctamente

---

## Ejemplo de Email en Consola

Cuando se envía un email, verás algo así en la terminal:

```
-------------------------------------------------------------------------------
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Cambio de contraseña - Biblioteca Colectiva
From: noreply@bibliotecacolectiva.com
To: usuario@ejemplo.com
Date: ...

<!DOCTYPE html>
<html>
...
<a href="http://127.0.0.1:8000/password/confirmar/TOKEN_AQUI/">Cambiar Contraseña</a>
...
</html>
-------------------------------------------------------------------------------
```

**Copia el enlace** que aparece en el HTML y ábrelo en el navegador.

---

## URLs Disponibles

- **Login**: `http://127.0.0.1:8000/login/`
- **Registro**: `http://127.0.0.1:8000/registro/`
- **Perfil**: `http://127.0.0.1:8000/perfil/`
- **Solicitar cambio de contraseña**: `http://127.0.0.1:8000/password/solicitar/`
- **Confirmar cambio (con token)**: `http://127.0.0.1:8000/password/confirmar/TOKEN/`

---

## Testing Checklist

- [ ] Crear usuario de prueba
- [ ] Solicitar cambio de contraseña desde login
- [ ] Ver email en consola
- [ ] Usar enlace del email para cambiar contraseña
- [ ] Verificar que la nueva contraseña funciona
- [ ] Probar cambio desde perfil (usuario autenticado)
- [ ] Probar con token expirado (cambiar `expires_at` manualmente en BD)
- [ ] Probar con token usado dos veces
- [ ] Verificar validaciones de contraseña (mínimo 8 caracteres, etc.)

---

## Troubleshooting

### No veo el email en la consola

- Verifica que el servidor esté corriendo
- Revisa que no haya errores en la terminal
- Asegúrate de que `DEBUG = True` en `settings.py`

### El enlace no funciona

- Verifica que copiaste el enlace completo
- Asegúrate de que el token no haya expirado (24 horas)
- Verifica que el token no haya sido usado antes

### Error al cambiar contraseña

- Verifica que la nueva contraseña cumpla los requisitos (mínimo 8 caracteres)
- Revisa los mensajes de error en la página
- Verifica que las contraseñas coincidan

---

## Próximos Pasos

Una vez que hayas probado todo en local:

1. **Para producción en PythonAnywhere:**
   - Configura Mailgun (ver `CONFIGURACION_EMAIL.md`)
   - Agrega las variables de entorno en PythonAnywhere
   - Prueba el envío de emails reales

2. **Mejoras futuras:**
   - Agregar rate limiting para prevenir spam
   - Mejorar diseño de emails
   - Agregar más validaciones de seguridad
