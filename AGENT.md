# AGENT.md

## Propósito
Guía completa para agentes/IA y colaboradores al trabajar en este proyecto Django (`biblioteca_colectiva_zero`). Este documento define el flujo de trabajo, estándares de código, y proceso de desarrollo para mantener calidad y consistencia.

---

## Principios Fundamentales

- **Código simple, claro, corto y mantenible**: Un desarrollador nuevo no debería tener que adivinar qué hace el código.
- **Sistema modular**: Responsabilidades bien separadas entre modelos, vistas, servicios y utilidades.
- **Reutilizar Django**: Usar auth, admin, forms, CBVs, validaciones y utilidades nativas antes de reescribir.
- **Cambios incrementales**: Cambios pequeños que aporten valor inmediato, evitando overengineering.
- **Tests obligatorios**: Todo cambio funcional debe estar cubierto por tests.

---

## Flujo de Trabajo del Agente

### Ciclo de Desarrollo Completo

1. **Tomar un ticket** del backlog (`docs/tickets/BACKLOG.md`)
2. **Crear branch** desde `develop`: `feature/TICKET-XXX-descripcion-corta` o `bugfix/TICKET-XXX-descripcion-corta`
3. **Desarrollar** la funcionalidad siguiendo los principios y estándares
4. **Escribir tests** antes de hacer commit (o durante el desarrollo)
5. **Ejecutar tests** antes de cada commit: `pytest` o `python manage.py test`
6. **Verificar DoD**: Cumplir con el Definition of Done
7. **Merge a develop**: Una vez aprobado, mergear a `develop`

### Commits

- **Commits pequeños y frecuentes**: Un commit por cambio lógico pequeño
- **Mensajes descriptivos**: `feat: agregar autocompletado de autores` o `fix: corregir validación de ISBN`
- **Tests pasando**: Nunca commitear código que rompa los tests

### Separación de Entornos

- **Desarrollo (local)**: Entorno de trabajo diario, puede tener configuraciones más permisivas
- **Producción**: Configuración estricta, variables de entorno, sin credenciales hardcodeadas
- **Configuración**: Usar `django-environ` para variables de entorno, nunca hardcodear valores sensibles

---

## Instrucciones para Agentes/IA

### ⚠️ REGLA FUNDAMENTAL: Proponer, No Implementar Directamente

**Los agentes/IA deben:**

1. **Proponer cambios** antes de implementarlos
2. **Consultar decisiones técnicas** cuando haya múltiples opciones
3. **Esperar aprobación explícita** antes de implementar cambios significativos
4. **Trabajar de forma incremental**: Cambios pequeños y controlados
5. **Verificar cada paso**: Confirmar que los cambios funcionan antes de continuar

### Proceso de Trabajo con Agentes

1. **Análisis**: El agente analiza el ticket o requerimiento
2. **Propuesta**: El agente propone la solución, incluyendo:
   - Qué archivos se modificarán
   - Qué cambios se harán
   - Por qué esta solución es la mejor
   - Alternativas consideradas
3. **Consulta**: El agente hace preguntas si hay decisiones técnicas a tomar
4. **Aprobación**: El desarrollador aprueba o solicita cambios
5. **Implementación**: Solo después de aprobación, el agente implementa
6. **Verificación**: El agente verifica que los cambios funcionan y cumplen DoD

### Delegación de Tareas

El desarrollador delega principalmente:
- ✅ **Tests**: Escribir tests unitarios y de integración
- ✅ **Documentación**: Actualizar README, guías, comentarios
- ⚠️ **Refactor**: Con supervisión y aprobación previa
- 🔍 **Implementación**: Con propuesta y aprobación previa

---

## Criterio de Valor (Scrum)

Toda funcionalidad sugerida o implementada debe:

- Seguir la lógica de **Scrum**
- Priorizar **el menor cambio posible que genere el mayor valor actual**
- Evitar overengineering y funcionalidades a futuro sin uso inmediato
- Preferir incrementos funcionales pequeños y validables
- Trabajar dentro del contexto de los **releases** definidos en `README.md` y `docs/PLAN_DESARROLLO_PRODUCCION.md`

---

## Reglas Obligatorias

1. **Tests**: No se acepta código funcional sin tests. Ejecutar tests antes de cada commit.
2. **Reusar Django**: auth, admin, forms, CBVs, validaciones y utilidades nativas siempre que aplique.
3. **Modularidad**:
   - `models`: datos y validaciones
   - `views`: orquestación HTTP (delgadas, delegan a services)
   - `services`: lógica de negocio
   - `utils`: funciones auxiliares reutilizables
4. **No reescritura innecesaria**: Refactorizar sólo si mejora claridad o reduce complejidad, siempre con tests.
5. **Estilo**: PEP8, nombres descriptivos, funciones pequeñas y enfocadas.

---

## Estilo de Código

### Principio: Código Corto pero Entendible

**✅ Bueno:**
```python
def crear_prestamo(libro_id, prestatario_id, prestador_id):
    """Crea un préstamo validando que el libro esté disponible."""
    libro = Libro.objects.get(id=libro_id)
    if libro.estado != 'disponible':
        raise ValueError("El libro no está disponible")
    # ... resto de la lógica
```

**❌ Malo:**
```python
def cp(l, p, pr):  # ¿Qué hace esto?
    # Lógica críptica sin contexto
    if l.e != 'd':
        raise ValueError("Error")
```

**✅ Bueno:**
```python
# Nombre descriptivo que explica la intención
libros_disponibles = Libro.objects.filter(estado='disponible')
```

**❌ Malo:**
```python
# Nombre genérico que no explica nada
items = Libro.objects.filter(estado='disponible')
```

### Reglas de Estilo

- **Nombres descriptivos**: `crear_prestamo` en lugar de `cp`
- **Funciones pequeñas**: Una función, una responsabilidad
- **Comentarios cuando sea necesario**: Explicar el "por qué", no el "qué"
- **Código autoexplicativo**: El código debe hablar por sí mismo

---

## Gitflow

### Ramas

- **`main`**: Estable / producción (solo código probado y estable)
- **`develop`**: Integración (rama de desarrollo principal)
- **`feature/TICKET-XXX-descripcion`**: Nuevas funcionalidades
- **`bugfix/TICKET-XXX-descripcion`**: Corrección de bugs
- **`hotfix/TICKET-XXX-descripcion`**: Correcciones urgentes para producción

### Proceso de Merge

1. Crear branch desde `develop`
2. Desarrollar y hacer commits pequeños
3. Ejecutar tests antes de cada commit
4. Hacer peer review del código
5. Verificar DoD
6. Mergear a `develop` (o crear PR si se usa)
7. Solo después de validación en `develop`, mergear a `main` para producción

### Commits

- **Pequeños y frecuentes**: Un commit por cambio lógico
- **Mensajes claros**: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- **Tests pasando**: Nunca commitear código que rompa tests

---

## Gestión de Tickets

### Estructura

Los tickets se gestionan en `docs/tickets/`:

- **`BACKLOG.md`**: Lista principal de tickets pendientes
- **`TEMPLATE.md`**: Plantilla para crear nuevos tickets
- **`active/`**: Tickets en progreso
- **`done/`**: Tickets completados
- **`backlog/`**: Tickets pendientes (opcional, si se separan del BACKLOG.md)

### Formato de Tickets

- **Numeración**: `TICKET-001`, `TICKET-002`, etc.
- **Relación con releases**: Cada ticket debe indicar el release al que pertenece (ej: `R3-TICKET-001`)
- **Prioridades**: `[CRÍTICA]`, `[ALTA]`, `[MEDIA]`, `[BAJA]`
- **Tamaño**: Tickets medianos (ni muy pequeños ni muy grandes)

Ver `docs/tickets/README.md` para más detalles.

---

## Checklist de PR/Commit

Antes de hacer merge o commit, verificar:

- [ ] Tests pasan (`pytest` o `python manage.py test`)
- [ ] Cambio pequeño y con valor claro
- [ ] Sin duplicar lógica existente
- [ ] Sin credenciales hardcodeadas
- [ ] Documentación actualizada si aplica (README, guías)
- [ ] Código sigue PEP8 y estilo del proyecto
- [ ] Nombres descriptivos y código entendible

---

## Definition of Done (DoD)

Antes de cerrar un ticket y mergear, verificar:

### 1. Cumplimiento del Objetivo
La funcionalidad implementada cumple con el objetivo descrito en el ticket.

### 2. Tests Unitarios
- Todos los tests unitarios pasan (`python manage.py test` o `pytest`)
- Tests cubren casos exitosos y casos de error
- Cobertura adecuada para la funcionalidad implementada

### 3. Test Manual Propuesto
Incluir en el ticket/PR una descripción clara de cómo reproducir y validar la funcionalidad manualmente:

- Pasos específicos a seguir
- Datos de prueba necesarios (si aplica)
- Resultado esperado
- Casos edge o escenarios alternativos a probar

**Ejemplo de test manual:**
```
Test manual - Cambio de contraseña:
1. Ir a /perfil/
2. Click en "Cambiar contraseña"
3. Ingresar contraseña actual y nueva contraseña
4. Verificar que se muestra mensaje de éxito
5. Cerrar sesión y volver a iniciar con nueva contraseña
6. Verificar que el login funciona correctamente
```

### 4. Documentación
- README actualizado si cambia algo del sistema (instalación, configuración, uso)
- Código autoexplicativo (no requiere documentación adicional si el código es claro)
- Guías de usuario actualizadas si cambia funcionalidad visible

### 5. Peer Review
- El agente le pide al desarrollador que revise el codigo
- El desarrollador reproduce los cambios siguiendo y test manuales antes de merge, 
- Si hay cambios de documentacion revisa que sea consistente con el sistema actual
- El desarrollador acepta los cambios y el merge
- Si el desarrollador no cepta el peer review le hace una devolucion al agente para que retome el trabajo para completar el ticket.

---

## Nota para Agentes: Checklist Antes de Proponer Código

Antes de proponer código nuevo, el agente debe verificar:

1. **¿Django ya lo resuelve?** Revisar si Django tiene una solución nativa.
2. **¿Este cambio es el mínimo necesario?** Evitar overengineering.
3. **¿Aporta valor hoy?** No implementar funcionalidades "por si acaso".
4. **¿Está cubierto por tests?** Proponer tests junto con la implementación.
5. **¿El código es entendible?** Un desarrollador nuevo debería entenderlo sin adivinar.

---

## Documentación del Proyecto

### Archivos Principales

- **`README.md`**: Descripción del proyecto, instalación, uso básico
- **`AGENT.md`**: Este archivo - guía para agentes y desarrolladores
- **`docs/PLAN_DESARROLLO_PRODUCCION.md`**: Plan de releases y roadmap
- **`docs/tickets/`**: Sistema de tickets y backlog
- **`Guia de uso.md`**: Guía para usuarios finales

### Cuándo Actualizar

- **README.md**: Cuando cambia instalación, configuración, o funcionalidades principales
- **AGENT.md**: Cuando cambian procesos, estándares, o flujo de trabajo
- **Guías de usuario**: Cuando cambia funcionalidad visible para el usuario
- **Código**: Documentar durante el desarrollo, no después

---

## Separación de Entornos

### Desarrollo (Local)

- Configuraciones más permisivas para facilitar desarrollo
- Debug activado
- Emails en consola (no envío real)
- Base de datos local (SQLite o PostgreSQL local)

### Producción

- Variables de entorno para toda configuración sensible
- Debug desactivado
- Emails reales configurados (Mailgun, SMTP, etc.)
- Base de datos de producción
- HTTPS configurado
- Logs apropiados

### Configuración

- Usar `django-environ` para variables de entorno
- Nunca hardcodear credenciales o valores sensibles
- Archivo `.env.example` con ejemplos (sin valores reales)
- `.env` en `.gitignore`

---

## Resumen Rápido para Agentes

1. **Proponer antes de implementar** - Consultar decisiones técnicas
2. **Trabajar incrementalmente** - Cambios pequeños y controlados
3. **Tests obligatorios** - Todo código funcional debe tener tests
4. **Código entendible** - Nombres descriptivos, funciones pequeñas
5. **Verificar DoD** - Antes de considerar un ticket completo
6. **Documentar durante desarrollo** - No dejar para después
7. **Reusar Django** - Antes de reescribir, verificar si Django lo resuelve

---

**Última actualización**: Enero 2025
