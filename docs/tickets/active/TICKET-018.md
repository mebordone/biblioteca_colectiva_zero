# TICKET-018: Agregar tests para carga masiva de libros

## Información General

- **ID**: TICKET-018
- **Release**: Mejoras Técnicas - Prioridad Media
- **Prioridad**: [ALTA]
- **Estado**: [COMPLETADO]
- **Tipo**: [TEST]
- **Creado**: 2025-01-13
- **Asignado a**: Desarrollador
- **Tamaño estimado**: 2 días

---

## Descripción

Agregar tests completos para la funcionalidad de carga masiva de libros desde archivos Excel. Actualmente no existen tests para `cargar_libros_masivo()` (vista) ni para `procesar_excel_libros()` (función en utils.py).

### Contexto

La funcionalidad de carga masiva fue implementada en Release 2 pero no tiene cobertura de tests. Según AGENT.md, todo cambio funcional debe estar cubierto por tests. Esta es una funcionalidad crítica que necesita tests para garantizar su correcto funcionamiento.

### Objetivo

Crear suite completa de tests para carga masiva que cubra casos exitosos, errores, duplicados, y validaciones, alcanzando cobertura >80%.

---

## Criterios de Aceptación

- [ ] Tests para vista `cargar_libros_masivo()` implementados
- [ ] Tests para función `procesar_excel_libros()` implementados
- [ ] Tests para `generar_plantilla_excel()` implementados
- [ ] Cobertura >80% para funcionalidad de carga masiva
- [ ] Tests cubren casos exitosos, errores, duplicados, validaciones
- [ ] Todos los tests pasan

---

## Tareas Técnicas

- [ ] Crear archivo `test_carga_masiva.py`
- [ ] Crear fixtures para archivos Excel de prueba (válidos, con errores, con duplicados)
- [ ] Implementar tests para vista `cargar_libros_masivo()`:
  - Test carga exitosa
  - Test validación de formulario
  - Test mensajes de éxito/error/warning
  - Test renderizado con resultados
- [ ] Implementar tests para `procesar_excel_libros()`:
  - Test procesamiento exitoso
  - Test detección de duplicados por ISBN
  - Test detección de duplicados por nombre+autor
  - Test manejo de filas con errores
  - Test validación de campos obligatorios
  - Test creación de libros en lote
  - Test manejo de excepciones
- [ ] Implementar tests para `generar_plantilla_excel()`:
  - Test generación de plantilla válida
  - Test formato correcto del archivo
- [ ] Verificar cobertura de tests

---

## Archivos a Modificar/Crear

### Archivos Nuevos
- `libro_prestamos/tests/test_carga_masiva.py` - Tests para carga masiva

### Archivos Modificados
- `libro_prestamos/tests/conftest.py` - Agregar fixtures para archivos Excel si es necesario

---

## Consideraciones Técnicas

### Decisiones Técnicas

- **Usar openpyxl para crear archivos de prueba**: Permite crear archivos Excel programáticamente en tests
- **Fixtures reutilizables**: Crear fixtures en `conftest.py` para archivos Excel comunes
- **Tests de integración**: Probar el flujo completo desde vista hasta creación de libros

### Dependencias

- [ ] Depende de: Ninguna
- [ ] Bloquea a: Ninguna

---

## Tests

### Tests Unitarios Requeridos

**Vista `cargar_libros_masivo()`:**
- [ ] Test carga exitosa con archivo válido
- [ ] Test manejo de errores de validación de formulario
- [ ] Test mensajes de éxito cuando se crean libros
- [ ] Test mensajes de warning cuando hay duplicados
- [ ] Test mensajes de error cuando hay errores en archivo
- [ ] Test renderizado con resultados

**Función `procesar_excel_libros()`:**
- [ ] Test procesamiento exitoso de archivo Excel válido
- [ ] Test detección de duplicados por ISBN
- [ ] Test detección de duplicados por nombre+autor
- [ ] Test manejo de filas con errores (campos faltantes)
- [ ] Test validación de campos obligatorios (nombre, autor)
- [ ] Test creación de libros en lote (bulk_create)
- [ ] Test manejo de excepciones (archivo corrupto, formato incorrecto)
- [ ] Test normalización de nombres de columnas
- [ ] Test validación de longitud de campos

**Función `generar_plantilla_excel()`:**
- [ ] Test generación de plantilla válida
- [ ] Test formato correcto del archivo (.xlsx)
- [ ] Test contenido de plantilla (encabezados correctos)

### Test Manual Propuesto

```
Test manual - Carga masiva de libros:
1. Iniciar sesión
2. Ir a /libros/cargar-masivo/
3. Descargar plantilla Excel
4. Completar plantilla con 5 libros válidos
5. Subir archivo
6. Verificar mensaje de éxito
7. Verificar que los 5 libros se crearon
8. Crear archivo con libros duplicados (mismo ISBN)
9. Subir archivo
10. Verificar mensaje de warning sobre duplicados
11. Verificar que duplicados no se crearon
12. Crear archivo con errores (faltan campos obligatorios)
13. Subir archivo
14. Verificar mensaje de error
15. Verificar que se muestran errores por fila

Casos edge:
- Archivo vacío
- Archivo con formato incorrecto
- Archivo muy grande (>5MB)
- Archivo con caracteres especiales
```

---

## Notas de Desarrollo

[Espacio para notas durante el desarrollo]

---

## Verificación DoD

Antes de marcar como completado, verificar:

- [ ] ✅ Cumplimiento del objetivo: Tests completos para carga masiva
- [ ] ✅ Tests unitarios: Todos los tests pasan, cobertura >80%
- [ ] ✅ Test manual: Funcionalidad probada manualmente
- [ ] ✅ Peer review: Código revisado y aprobado
- [ ] ✅ Documentación: Tests bien documentados
- [ ] ✅ Código limpio: Sigue principios y estándares del proyecto

---

## Historial

- **2025-01-13**: Ticket creado

---

## Notas Finales

[Notas finales al completar el ticket]
