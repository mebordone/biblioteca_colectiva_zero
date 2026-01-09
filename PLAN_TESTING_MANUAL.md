# Plan de Testing Manual - Sistema de Cambio de Contraseña

## Objetivo

Validar manualmente que todas las funcionalidades del sistema de cambio de contraseña funcionan correctamente en el entorno de desarrollo local.

---

## Pre-requisitos

- ✅ Servidor Django corriendo en `http://127.0.0.1:8000/`
- ✅ Base de datos con migraciones aplicadas
- ✅ Modo consola activado (emails se muestran en terminal)
- ✅ Al menos un usuario de prueba creado

---

## Escenario 1: Cambio de Contraseña desde Login (Usuario NO Autenticado)

### Objetivo
Verificar que un usuario que olvidó su contraseña puede solicitarla y cambiarla.

### Pasos

1. **Acceder a la página de login**
   - URL: `http://127.0.0.1:8000/login/`
   - Verificar que aparece el enlace "¿Olvidaste tu contraseña?"

2. **Hacer clic en "¿Olvidaste tu contraseña?"**
   - Debe redirigir a `/password/solicitar/`
   - Verificar que aparece el formulario con campo de email

3. **Ingresar email de usuario existente**
   - Ingresar el email de un usuario que existe en el sistema
   - Hacer clic en "Enviar Enlace"

4. **Verificar email en consola**
   - En la terminal donde corre el servidor, buscar el email
   - Verificar que contiene:
     - Asunto: "Cambio de contraseña - Biblioteca Colectiva"
     - Enlace con el token
     - Información de seguridad (expiración, no compartir)

5. **Copiar y abrir el enlace**
   - Copiar el enlace completo del email (del HTML en la terminal)
   - Abrir en el navegador
   - Verificar que aparece el formulario para nueva contraseña

6. **Cambiar la contraseña**
   - Ingresar nueva contraseña (mínimo 8 caracteres)
   - Confirmar contraseña
   - Hacer clic en "Cambiar Contraseña"

7. **Verificar cambio exitoso**
   - Debe redirigir a login
   - Debe mostrar mensaje de éxito
   - Intentar iniciar sesión con la nueva contraseña
   - Debe funcionar correctamente

### Resultado Esperado
✅ Usuario puede cambiar su contraseña exitosamente y puede iniciar sesión con la nueva.

---

## Escenario 2: Cambio de Contraseña desde Perfil (Usuario Autenticado)

### Objetivo
Verificar que un usuario autenticado puede cambiar su contraseña desde su perfil.

### Pasos

1. **Iniciar sesión**
   - Login con usuario de prueba
   - Verificar que se redirige al home

2. **Acceder al perfil**
   - URL: `http://127.0.0.1:8000/perfil/`
   - Verificar que aparece la sección "Seguridad" con botón "Cambiar Contraseña"

3. **Hacer clic en "Cambiar Contraseña"**
   - Debe redirigir a `/password/cambiar/`
   - Verificar que aparece el formulario con:
     - Campo "Contraseña actual"
     - Campo "Nueva contraseña"
     - Campo "Confirmar nueva contraseña"

4. **Completar formulario**
   - Ingresar contraseña actual correcta
   - Ingresar nueva contraseña
   - Confirmar nueva contraseña
   - Hacer clic en "Solicitar Cambio"

5. **Verificar email en consola**
   - En la terminal, buscar el email de confirmación
   - Verificar que contiene el enlace

6. **Completar cambio desde email**
   - Copiar enlace del email
   - Abrir en navegador
   - La contraseña se cambia automáticamente (ya se validó la actual)

7. **Verificar cambio**
   - Cerrar sesión
   - Iniciar sesión con nueva contraseña
   - Debe funcionar

### Resultado Esperado
✅ Usuario autenticado puede cambiar su contraseña y la nueva contraseña funciona.

---

## Escenario 3: Validaciones y Casos de Error

### 3.1 Email No Existente

**Pasos:**
1. Ir a `/password/solicitar/`
2. Ingresar un email que NO existe en el sistema
3. Hacer clic en "Enviar Enlace"

**Resultado Esperado:**
✅ Muestra mensaje genérico (no revela si el email existe)
✅ No se crea token
✅ No se envía email

---

### 3.2 Token Expirado

**Pasos:**
1. Crear un token manualmente en la base de datos
2. Modificar `expires_at` a una fecha pasada
3. Intentar usar el enlace con ese token

**Resultado Esperado:**
✅ Muestra mensaje de error: "El enlace ha expirado"
✅ Redirige a solicitar nuevo cambio

---

### 3.3 Token Usado Dos Veces

**Pasos:**
1. Solicitar cambio de contraseña
2. Usar el enlace del email para cambiar contraseña
3. Intentar usar el mismo enlace nuevamente

**Resultado Esperado:**
✅ Muestra mensaje de error: "El enlace ya fue utilizado"
✅ No permite cambiar la contraseña nuevamente

---

### 3.4 Contraseña Muy Corta

**Pasos:**
1. Solicitar cambio de contraseña
2. En el formulario de nueva contraseña, ingresar contraseña de menos de 8 caracteres
3. Intentar enviar

**Resultado Esperado:**
✅ Muestra error de validación
✅ No permite cambiar la contraseña

---

### 3.5 Contraseñas No Coinciden

**Pasos:**
1. Solicitar cambio de contraseña
2. En el formulario, ingresar contraseñas diferentes
3. Intentar enviar

**Resultado Esperado:**
✅ Muestra error: "Las contraseñas no coinciden"
✅ No permite cambiar la contraseña

---

### 3.6 Contraseña Actual Incorrecta (desde perfil)

**Pasos:**
1. Ir a perfil → Cambiar Contraseña
2. Ingresar contraseña actual incorrecta
3. Ingresar nueva contraseña válida
4. Intentar enviar

**Resultado Esperado:**
✅ Muestra error: "La contraseña actual es incorrecta"
✅ No permite continuar

---

## Escenario 4: Flujo Completo End-to-End

### Objetivo
Probar el flujo completo desde solicitud hasta cambio exitoso.

### Pasos

1. **Usuario olvida contraseña**
   - Ir a login
   - Clic en "¿Olvidaste tu contraseña?"

2. **Solicitar cambio**
   - Ingresar email
   - Enviar solicitud

3. **Recibir email (en consola)**
   - Verificar contenido del email
   - Copiar enlace

4. **Cambiar contraseña**
   - Abrir enlace
   - Ingresar nueva contraseña
   - Confirmar

5. **Verificar cambio**
   - Iniciar sesión con nueva contraseña
   - Verificar que funciona

6. **Email de confirmación**
   - Verificar que se envió email de confirmación
   - Verificar contenido

### Resultado Esperado
✅ Todo el flujo funciona correctamente de extremo a extremo.

---

## Escenario 5: Seguridad

### 5.1 No Revelar Existencia de Email

**Pasos:**
1. Intentar cambiar contraseña con email que NO existe
2. Observar el mensaje

**Resultado Esperado:**
✅ Muestra el mismo mensaje que para emails existentes
✅ No revela si el email está registrado o no

---

### 5.2 Token Único y Seguro

**Pasos:**
1. Solicitar cambio de contraseña dos veces
2. Verificar los tokens en la base de datos

**Resultado Esperado:**
✅ Cada token es único
✅ Tokens tienen longitud adecuada (32+ caracteres)
✅ Token anterior se marca como usado

---

### 5.3 Expiración de Token

**Pasos:**
1. Verificar en la base de datos que `expires_at` es 24 horas después de `created_at`

**Resultado Esperado:**
✅ Token expira en exactamente 24 horas

---

## Checklist de Testing

### Funcionalidades Básicas
- [ ] Solicitar cambio desde login (usuario no autenticado)
- [ ] Solicitar cambio desde perfil (usuario autenticado)
- [ ] Recibir email en consola
- [ ] Cambiar contraseña con token válido
- [ ] Iniciar sesión con nueva contraseña
- [ ] Email de confirmación se envía

### Validaciones
- [ ] Email no existente muestra mensaje genérico
- [ ] Token expirado muestra error
- [ ] Token usado muestra error
- [ ] Contraseña corta muestra error
- [ ] Contraseñas no coinciden muestran error
- [ ] Contraseña actual incorrecta muestra error

### Seguridad
- [ ] No se revela si email existe
- [ ] Tokens son únicos
- [ ] Tokens expiran correctamente
- [ ] Tokens no se pueden reutilizar

### UI/UX
- [ ] Enlaces funcionan correctamente
- [ ] Mensajes de error son claros
- [ ] Mensajes de éxito son claros
- [ ] Formularios tienen validación visual
- [ ] Navegación es intuitiva

---

## Notas para el Testing

1. **Emails en Consola:**
   - Todos los emails aparecerán en la terminal donde corre `python manage.py runserver`
   - Busca el contenido HTML del email
   - Copia el enlace completo (incluye `http://127.0.0.1:8000/password/confirmar/TOKEN/`)

2. **Base de Datos:**
   - Puedes verificar tokens en la tabla `core_passwordresettoken`
   - Usa `python manage.py shell` para inspeccionar:
     ```python
     from core.models import PasswordResetToken
     tokens = PasswordResetToken.objects.all()
     for t in tokens:
         print(f"{t.user.email} - {t.token[:20]}... - Usado: {t.used} - Expira: {t.expires_at}")
     ```

3. **Modificar Tokens para Testing:**
   - Para probar tokens expirados, modifica `expires_at` en la BD
   - Para probar tokens usados, modifica `used = True`

---

## Siguiente Paso

Una vez completado el testing manual local, el siguiente paso es:
- Configurar SendGrid en PythonAnywhere
- Probar el envío de emails reales
- Validar que los enlaces funcionan con el dominio de producción
