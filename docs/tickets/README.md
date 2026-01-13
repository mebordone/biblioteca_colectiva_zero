# Sistema de Tickets - Biblioteca Colectiva Zero

## Propósito

Este sistema permite gestionar el backlog, tickets activos y completados de manera autocontenida dentro del repositorio. Todo el trabajo del proyecto queda documentado y rastreable.

---

## Estructura

```
docs/tickets/
├── README.md              # Este archivo - guía de uso
├── TEMPLATE.md            # Plantilla para crear nuevos tickets
├── BACKLOG.md             # Backlog principal de tickets pendientes
├── active/                # Tickets en progreso
│   └── TICKET-XXX.md
├── done/                  # Tickets completados
│   └── TICKET-XXX.md
└── backlog/               # Tickets pendientes (opcional)
    └── TICKET-XXX.md
```

---

## Flujo de Trabajo

### 1. Crear un Ticket

1. Copiar `TEMPLATE.md` a un nuevo archivo: `TICKET-XXX.md`
2. Completar la información del ticket
3. Agregar el ticket a `BACKLOG.md` en la sección correspondiente
4. Mover el archivo a `backlog/` si se quiere separar del BACKLOG.md principal

### 2. Iniciar Trabajo en un Ticket

1. Mover el ticket de `backlog/` (o desde `BACKLOG.md`) a `active/`
2. Actualizar el estado en `BACKLOG.md` a `[EN PROGRESO]`
3. Crear branch: `feature/TICKET-XXX-descripcion` o `bugfix/TICKET-XXX-descripcion`

### 3. Completar un Ticket

1. Verificar que cumple con el Definition of Done (ver `AGENT.md`)
2. Actualizar el ticket con:
   - Estado: `[COMPLETADO]`
   - Fecha de completado
   - Test manual propuesto
   - Notas finales
3. Mover el ticket de `active/` a `done/`
4. Actualizar `BACKLOG.md` marcando el ticket como completado
5. Hacer merge del branch a `develop`

---

## Numeración de Tickets

- **Formato**: `TICKET-001`, `TICKET-002`, etc.
- **Relación con releases**: Se puede usar formato `R3-TICKET-001` para indicar Release 3, Ticket 1
- **Incremento automático**: El siguiente número disponible se toma del último ticket creado

---

## Prioridades

- **`[CRÍTICA]`**: Bloquea funcionalidad principal o producción
- **`[ALTA]`**: Importante para el release actual
- **`[MEDIA]`**: Mejora significativa pero no bloqueante
- **`[BAJA]`**: Nice-to-have, puede esperar

---

## Tamaño de Tickets

- **Tickets medianos**: 2-5 días de trabajo
- Si un ticket es muy grande, dividirlo en subtickets
- Si un ticket es muy pequeño, considerar agruparlo con otros relacionados

---

## Estados de Tickets

- **`[PENDIENTE]`**: En el backlog, esperando ser trabajado
- **`[EN PROGRESO]`**: Actualmente siendo desarrollado
- **`[EN REVISIÓN]`**: Completado, esperando peer review y verificación DoD
- **`[COMPLETADO]`**: Terminado, mergeado, y verificado
- **`[BLOQUEADO]`**: No se puede continuar por dependencias externas
- **`[CANCELADO]`**: Ya no es necesario o fue reemplazado

---

## Relación con Releases

Cada ticket debe indicar:
- **Release al que pertenece**: Ej: `Release 3: Gestión Avanzada de Préstamos`
- **Prioridad dentro del release**: `[CRÍTICA]`, `[ALTA]`, etc.

Esto permite:
- Planificar releases de manera más efectiva
- Priorizar trabajo dentro de cada release
- Rastrear qué funcionalidades pertenecen a qué release

---

## Ejemplo de Uso

### Crear un nuevo ticket:

1. Ver el último número usado en `BACKLOG.md` (ej: TICKET-015)
2. Crear `TICKET-016.md` usando `TEMPLATE.md`
3. Completar información
4. Agregar a `BACKLOG.md`:
   ```markdown
   ## Release 3: Gestión Avanzada de Préstamos
   
   - [ ] [ALTA] TICKET-016: Implementar solicitud de préstamos
     - Descripción breve...
   ```

### Iniciar trabajo:

1. Mover `TICKET-016.md` a `active/`
2. Actualizar en `BACKLOG.md`: `[EN PROGRESO]`
3. Crear branch: `feature/TICKET-016-solicitud-prestamos`

### Completar:

1. Verificar DoD
2. Actualizar ticket con test manual
3. Mover a `done/`
4. Actualizar `BACKLOG.md`: `[COMPLETADO]`
5. Merge a `develop`

---

## Mantenimiento del Backlog

- **Revisar periódicamente**: Eliminar tickets obsoletos o cancelados
- **Priorizar**: Mover tickets importantes al inicio de cada release
- **Agrupar**: Tickets relacionados pueden agruparse en epics o features mayores
- **Actualizar estados**: Mantener `BACKLOG.md` sincronizado con los archivos de tickets

---

## Integración con Git

- **Commits relacionados**: En los commits, referenciar el ticket: `feat(TICKET-016): implementar solicitud de préstamos`
- **Branches**: Usar formato `feature/TICKET-016-descripcion` o `bugfix/TICKET-016-descripcion`
- **PRs**: Incluir referencia al ticket en la descripción del PR

---

**Última actualización**: Diciembre 2024
