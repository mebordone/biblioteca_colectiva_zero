# Guía para Tests Manuales - Reorganización Modular

## Estado de Tests Unitarios

✅ **Todos los tests unitarios pasan: 146/146**

## Pasos para Preparar el Entorno y Realizar Tests Manuales

### 1. Activar el Entorno Virtual

```bash
cd /home/mebordone/Documentos/brujas/biblioteca-colectiva-zero
source .venv/bin/activate
cd libro_prestamos
```

### 2. Eliminar Base de Datos de Desarrollo

```bash
# Eliminar la base de datos actual
rm db.sqlite3
```

### 3. Aplicar Migraciones desde Cero

```bash
# Crear todas las migraciones desde cero
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate
```

### 4. Crear Superusuario de Prueba

```bash
python manage.py createsuperuser
# Ingresar: username, email, password
```

### 5. Levantar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## Checklist de Tests Manuales

### Autenticación y Usuarios

- [ ] **Registro de nuevo usuario**
  - Ir a `/registro/`
  - Completar formulario con datos válidos
  - Verificar que se crea el usuario y perfil
  - Verificar redirección a login

- [ ] **Login con credenciales válidas**
  - Ir a `/login/` o `/accounts/login/`
  - Ingresar credenciales del usuario creado
  - Verificar que inicia sesión correctamente
  - Verificar redirección a home

- [ ] **Logout**
  - Estar autenticado
  - Ir a `/logout/`
  - Verificar que cierra sesión
  - Verificar redirección a home

- [ ] **Visualización de perfil**
  - Estar autenticado
  - Ir a `/perfil/`
  - Verificar que se muestra la información del perfil

- [ ] **Edición de perfil**
  - Estar autenticado
  - Ir a `/perfil/`
  - Modificar campos (teléfono, ciudad, país)
  - Guardar cambios
  - Verificar que se actualizan correctamente

- [ ] **Solicitar cambio de contraseña**
  - Ir a `/password/solicitar/`
  - Ingresar email válido
  - Verificar mensaje de éxito
  - Revisar consola del servidor para ver el email (en desarrollo)

- [ ] **Confirmar cambio de contraseña (con token)**
  - Obtener token del email en consola
  - Ir a `/password/confirmar/<token>/`
  - Ingresar nueva contraseña
  - Verificar que se cambia correctamente
  - Probar login con nueva contraseña

- [ ] **Cambiar contraseña desde perfil**
  - Estar autenticado
  - Ir a `/password/cambiar/`
  - Ingresar contraseña actual y nueva
  - Verificar que se cambia correctamente
  - Verificar email de confirmación en consola

- [ ] **Solicitar cambio de email**
  - Estar autenticado
  - Ir a `/email/solicitar/`
  - Ingresar nuevo email y contraseña actual
  - Verificar mensaje de éxito
  - Revisar consola para ver email de confirmación

- [ ] **Confirmar cambio de email (con token)**
  - Obtener token del email en consola
  - Ir a `/email/confirmar/<token>/`
  - Confirmar el cambio
  - Verificar que el email se actualiza
  - Probar login con nuevo email

- [ ] **Cerrar sesiones en todos los dispositivos**
  - Estar autenticado
  - Ir a `/security/cerrar-sesiones/`
  - Confirmar la acción
  - Verificar mensaje de éxito

### Gestión de Libros

- [ ] **Listar todos los libros**
  - Ir a `/libros/`
  - Verificar que se muestran todos los libros
  - Verificar paginación si hay muchos libros

- [ ] **Buscar libros por nombre/autor**
  - Ir a `/libros/`
  - Usar el campo de búsqueda con `?q=termino`
  - Verificar que filtra correctamente

- [ ] **Ver detalle de un libro**
  - Ir a `/libros/ver/<id>/`
  - Verificar que se muestra toda la información
  - Verificar información del propietario

- [ ] **Crear nuevo libro**
  - Estar autenticado
  - Ir a `/libros/cargar/`
  - Completar formulario con datos válidos
  - Guardar
  - Verificar que se crea y aparece en la lista

- [ ] **Editar libro (solo propietario)**
  - Estar autenticado como propietario
  - Ir a `/libros/<id>/editar/`
  - Modificar campos
  - Guardar
  - Verificar que se actualiza

- [ ] **Intentar editar libro de otro usuario**
  - Estar autenticado como usuario diferente
  - Intentar acceder a `/libros/<id>/editar/` de otro usuario
  - Verificar que muestra error 403

- [ ] **Eliminar libro (solo propietario)**
  - Estar autenticado como propietario
  - Ir a `/libros/<id>/eliminar/`
  - Confirmar eliminación
  - Verificar que se elimina

- [ ] **Cargar libros masivamente desde Excel**
  - Estar autenticado
  - Ir a `/libros/cargar-masivo/`
  - Descargar plantilla primero
  - Llenar plantilla con datos
  - Subir archivo
  - Verificar que se crean los libros

- [ ] **Descargar plantilla Excel**
  - Estar autenticado
  - Ir a `/libros/descargar-plantilla/`
  - Verificar que se descarga el archivo
  - Verificar formato del archivo

- [ ] **Verificar validación de duplicados en carga masiva**
  - Cargar mismo libro dos veces
  - Verificar mensaje de duplicados
  - Verificar que no se crean duplicados

### Gestión de Préstamos

- [ ] **Crear préstamo (libro disponible)**
  - Estar autenticado
  - Tener al menos un libro disponible
  - Ir a `/prestamos/crear`
  - Seleccionar libro y prestatario
  - Crear préstamo
  - Verificar mensaje de éxito
  - Verificar que el libro cambia a estado "prestado"

- [ ] **Listar préstamos activos (realizados y recibidos)**
  - Estar autenticado
  - Ir a `/prestamos/`
  - Verificar que se muestran préstamos realizados
  - Verificar que se muestran préstamos recibidos

- [ ] **Ver historial de préstamos**
  - Estar autenticado
  - Ir a `/prestamos/historial`
  - Verificar que se muestran todos los préstamos (incluyendo devueltos)

- [ ] **Marcar préstamo como devuelto**
  - Estar autenticado como prestador
  - Ir a `/prestamos/marcar_devuelto/<prestamo_id>/`
  - Verificar mensaje de éxito
  - Verificar que el libro vuelve a estado "disponible"

- [ ] **Verificar que el estado del libro se actualiza correctamente**
  - Crear préstamo
  - Verificar que libro está "prestado"
  - Marcar como devuelto
  - Verificar que libro vuelve a "disponible"

- [ ] **Verificar que no se puede prestar un libro ya prestado**
  - Intentar crear préstamo de un libro ya prestado
  - Verificar mensaje de error

### Navegación y UI

- [ ] **Verificar que todas las URLs funcionan correctamente**
  - Probar todas las URLs principales
  - Verificar que no hay errores 404

- [ ] **Verificar que los templates se renderizan sin errores**
  - Navegar por todas las páginas
  - Verificar que no hay errores en consola del servidor

- [ ] **Verificar que los mensajes de éxito/error se muestran correctamente**
  - Realizar acciones que generen mensajes
  - Verificar que aparecen en la página

- [ ] **Verificar que la navegación entre páginas funciona**
  - Usar los enlaces del navbar
  - Verificar que la navegación es fluida

- [ ] **Verificar que los permisos de acceso funcionan (login_required, etc.)**
  - Intentar acceder a páginas protegidas sin login
  - Verificar redirección a login
  - Después de login, verificar acceso

### Admin de Django

- [ ] **Acceder al admin de Django**
  - Ir a `/admin/`
  - Login con superusuario
  - Verificar acceso

- [ ] **Verificar que los modelos están registrados correctamente**
  - En admin, verificar que aparecen:
    - Perfil (usuarios)
    - Libro (libros)
    - Prestamo (prestamos)

- [ ] **Probar crear/editar/eliminar desde admin**
  - Crear un registro desde admin
  - Editar un registro
  - Eliminar un registro
  - Verificar que funciona correctamente

## Comandos Útiles

### Verificar estado de migraciones
```bash
python manage.py showmigrations
```

### Verificar URLs disponibles
```bash
python manage.py showurls
```

### Ejecutar tests unitarios
```bash
pytest tests/ -v
```

### Ver logs del servidor
Los emails en desarrollo se muestran en la consola donde corre el servidor.

## Notas Importantes

- En desarrollo, los emails se muestran en la consola del servidor (no se envían realmente)
- Para obtener tokens de cambio de password/email, revisar la consola donde corre `runserver`
- La base de datos SQLite se crea automáticamente al ejecutar `migrate`
- Si hay errores, revisar la consola del servidor para ver los detalles
