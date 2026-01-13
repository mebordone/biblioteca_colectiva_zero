# TICKET-017: Refactorizar vistas de autenticación moviendo lógica a services

## Información General

- **ID**: TICKET-017
- **Release**: Mejoras Técnicas - Prioridad Media
- **Prioridad**: [ALTA]
- **Estado**: [COMPLETADO]
- **Tipo**: [REFACTOR]
- **Creado**: 2025-01-13
- **Asignado a**: Desarrollador
- **Tamaño estimado**: 3 días

---

## Descripción

Refactorizar las vistas de autenticación (`solicitar_cambio_password`, `confirmar_cambio_password`, `cambiar_password_desde_perfil`, `solicitar_cambio_email`, `confirmar_cambio_email`) para mover la lógica de negocio a services, cumpliendo con los principios de AGENT.md que establecen que las vistas deben ser delgadas y solo orquestar HTTP.

### Contexto

Actualmente las vistas de autenticación contienen lógica de negocio (validaciones, creación de tokens, envío de emails, manejo de errores) que debería estar en services según AGENT.md. Esto viola el principio de modularidad y hace el código difícil de mantener y testear.

### Objetivo

Separar la lógica de negocio de las vistas, moviéndola a services, para que las vistas solo orquesten HTTP y deleguen a services. Esto mejorará la mantenibilidad, testabilidad y cumplimiento con AGENT.md.

---

## Criterios de Aceptación

- [ ] Todas las vistas de autenticación tienen menos de 30 líneas
- [ ] Lógica de negocio está en `auth_services.py` o `services.py`
- [ ] Vistas solo orquestan HTTP (validan formularios, llaman services, manejan respuestas)
- [ ] Todos los tests existentes siguen pasando
- [ ] Nuevos tests para services de autenticación
- [ ] Código sigue principios de AGENT.md

---

## Tareas Técnicas

- [ ] Crear módulo `auth_services.py` o extender `services.py` con servicios de autenticación
- [ ] Implementar `solicitar_cambio_password_service(user, email=None)`
- [ ] Implementar `confirmar_cambio_password_service(token, new_password)`
- [ ] Implementar `cambiar_password_desde_perfil_service(user, old_password, new_password)`
- [ ] Implementar `solicitar_cambio_email_service(user, new_email, password)`
- [ ] Implementar `confirmar_cambio_email_service(token)`
- [ ] Refactorizar `solicitar_cambio_password()` en views.py
- [ ] Refactorizar `confirmar_cambio_password()` en views.py
- [ ] Refactorizar `cambiar_password_desde_perfil()` en views.py
- [ ] Refactorizar `solicitar_cambio_email()` en views.py
- [ ] Refactorizar `confirmar_cambio_email()` en views.py
- [ ] Actualizar tests existentes si es necesario
- [ ] Crear tests para nuevos services

---

## Archivos a Modificar/Crear

### Archivos Nuevos
- `libro_prestamos/core/auth_services.py` - Servicios de autenticación (o extender `services.py`)

### Archivos Modificados
- `libro_prestamos/core/views.py` - Simplificar vistas de autenticación (líneas 337-583)
- `libro_prestamos/tests/test_views.py` - Actualizar tests si es necesario
- `libro_prestamos/tests/test_services.py` - Agregar tests para auth_services (o crear `test_auth_services.py`)

---

## Consideraciones Técnicas

### Decisiones Técnicas

- **Crear `auth_services.py` separado**: Mantiene `services.py` enfocado en préstamos y separa responsabilidades
- **Patrón de retorno `(resultado, error)`**: Consistente con `services.py` actual
- **Mantener logging**: Los services deben mantener el logging existente
- **Manejo de excepciones**: Los services deben capturar excepciones y retornar mensajes de error claros

### Dependencias

- [ ] Depende de: Ninguna
- [ ] Bloquea a: TICKET-019 (dividir vistas largas se beneficia de esta refactorización)

---

## Tests

### Tests Unitarios Requeridos

- [ ] Test `solicitar_cambio_password_service` - caso exitoso
- [ ] Test `solicitar_cambio_password_service` - usuario no existe
- [ ] Test `confirmar_cambio_password_service` - caso exitoso
- [ ] Test `confirmar_cambio_password_service` - token inválido
- [ ] Test `confirmar_cambio_password_service` - token expirado
- [ ] Test `cambiar_password_desde_perfil_service` - caso exitoso
- [ ] Test `cambiar_password_desde_perfil_service` - contraseña actual incorrecta
- [ ] Test `solicitar_cambio_email_service` - caso exitoso
- [ ] Test `solicitar_cambio_email_service` - email ya existe
- [ ] Test `confirmar_cambio_email_service` - caso exitoso
- [ ] Test `confirmar_cambio_email_service` - token inválido

### Test Manual Propuesto

```
Test manual - Refactorización de autenticación:
1. Ir a /password/solicitar/ sin estar autenticado
2. Ingresar email válido
3. Verificar que se envía email (o se muestra en consola)
4. Usar el enlace del email para cambiar contraseña
5. Verificar que el cambio funciona
6. Iniciar sesión con nueva contraseña
7. Ir a /perfil/ y cambiar contraseña desde perfil
8. Verificar que funciona correctamente
9. Probar cambio de email desde perfil
10. Verificar que se envía email de confirmación
11. Usar enlace para confirmar cambio de email
12. Verificar que el email cambió correctamente

Casos edge:
- Token expirado
- Token ya usado
- Email ya existe en sistema
- Contraseña actual incorrecta
```

---

## Notas de Desarrollo

[Espacio para notas durante el desarrollo]

---

## Verificación DoD

Antes de marcar como completado, verificar:

- [ ] ✅ Cumplimiento del objetivo: Lógica movida a services, vistas simplificadas
- [ ] ✅ Tests unitarios: Todos los tests pasan (nuevos y existentes)
- [ ] ✅ Test manual: Funcionalidad probada manualmente
- [ ] ✅ Peer review: Código revisado y aprobado
- [ ] ✅ Documentación: Código autoexplicativo, docstrings en services
- [ ] ✅ Código limpio: Sigue principios y estándares del proyecto

---

## Historial

- **2025-01-13**: Ticket creado

---

## Notas Finales

[Notas finales al completar el ticket]
