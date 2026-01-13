# Backlog Principal - Biblioteca Colectiva Zero

Este archivo contiene el backlog principal de tickets organizados por releases y prioridad.

**Última actualización**: Diciembre 2024

---

## Leyenda de Estados

- `[PENDIENTE]` - En el backlog, esperando ser trabajado
- `[EN PROGRESO]` - Actualmente siendo desarrollado
- `[EN REVISIÓN]` - Completado, esperando peer review y verificación DoD
- `[COMPLETADO]` - Terminado, mergeado, y verificado
- `[BLOQUEADO]` - No se puede continuar por dependencias externas
- `[CANCELADO]` - Ya no es necesario o fue reemplazado

---

## Release 3: Gestión Avanzada de Préstamos

### [CRÍTICA]

- [ ] [PENDIENTE] TICKET-001: Implementar sistema de solicitud de préstamos
  - Permitir que usuarios soliciten préstamos de libros disponibles
  - Los propietarios pueden aceptar o rechazar solicitudes
  - Estados: pendiente, aceptado, rechazado

- [ ] [PENDIENTE] TICKET-002: Implementar vista de solicitudes pendientes
  - Vista para propietarios ver solicitudes recibidas
  - Botones para aceptar/rechazar
  - Notificación al solicitante del resultado

### [ALTA]

- [ ] [PENDIENTE] TICKET-003: Mejorar estados de préstamo
  - Estados: Pendiente, Aceptado, Activo, Devuelto, Rechazado
  - Transiciones de estado validadas
  - Actualización automática de estado del libro

- [ ] [PENDIENTE] TICKET-004: Historial de solicitudes
  - Ver todas las solicitudes realizadas
  - Ver todas las solicitudes recibidas
  - Filtros por estado

---

## Release 4: Gestión Avanzada de Búsquedas

### [ALTA]

- [ ] [PENDIENTE] TICKET-005: Implementar sistema de tags
  - Modelo Tag
  - Asociación muchos-a-muchos con Libro
  - Interfaz para agregar/editar tags

- [ ] [PENDIENTE] TICKET-006: Filtros avanzados en búsqueda
  - Filtro por ciudad
  - Filtro por país
  - Filtro por tags
  - Combinación de filtros

- [ ] [PENDIENTE] TICKET-007: Vista de libros de usuario
  - Página para ver todos los libros de un usuario específico
  - Filtros y búsqueda en libros de usuario

---

## Release 5: Integración de Comunidades

### [MEDIA]

- [ ] [PENDIENTE] TICKET-008: Modelo y CRUD de Comunidades
  - Modelo Comunidad con nombre, descripción, imagen
  - Crear, editar, eliminar comunidades
  - Asignar administrador

- [ ] [PENDIENTE] TICKET-009: Sistema de membresía en comunidades
  - Unirse/salir de comunidades
  - Roles: administrador, miembro
  - Validación de permisos

- [ ] [PENDIENTE] TICKET-010: Libros compartidos en comunidades
  - Asociar libros a comunidades
  - Ver libros de una comunidad
  - Compartir libros entre miembros

---

## Release 6: Notificaciones

### [ALTA]

- [ ] [PENDIENTE] TICKET-011: Modelo de Notificaciones
  - Modelo Notificación con tipo, estado, usuario, préstamo
  - Tipos: solicitud, aceptación, rechazo

- [ ] [PENDIENTE] TICKET-012: Notificaciones por email
  - Email cuando se recibe solicitud
  - Email cuando se acepta/rechaza solicitud
  - Templates de email

- [ ] [PENDIENTE] TICKET-013: Notificaciones in-app
  - Badge de notificaciones en navbar
  - Lista de notificaciones no leídas
  - Marcar como leída

---

## Release 7: Mejoras Opcionales

### [BAJA]

- [ ] [PENDIENTE] TICKET-014: Carga de imagen en comunidades
  - Subir y editar imagen de comunidad
  - Validación de tamaño y formato

- [ ] [PENDIENTE] TICKET-015: Interfaz mejorada para búsqueda por tags
  - Autocompletado de tags
  - Filtros visuales mejorados

- [ ] [PENDIENTE] TICKET-016: Implementación de geolocalización
  - Búsqueda por proximidad
  - Radio de búsqueda configurable
  - Mapa básico de ubicaciones

---

## Bugs y Mejoras Técnicas

### [CRÍTICA]

- [ ] [PENDIENTE] TICKET-XXX: [Descripción del bug crítico]

### [ALTA]

- [ ] [PENDIENTE] TICKET-XXX: [Descripción de mejora técnica importante]

---

## Notas

- Los tickets se organizan por release según el plan en `docs/PLAN_DESARROLLO_PRODUCCION.md`
- Priorizar tickets [CRÍTICA] y [ALTA] dentro de cada release
- Mover tickets a `active/` cuando se empiece a trabajar en ellos
- Mover tickets a `done/` cuando se completen
- Actualizar este archivo cuando cambie el estado de un ticket

---

## Estadísticas

- **Total de tickets**: 16
- **Completados**: 0
- **En progreso**: 0
- **Pendientes**: 16
