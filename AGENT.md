# AGENT.md

## Propósito
Guía mínima para agentes/IA y colaboradores al trabajar en este proyecto Django (`biblioteca_colectiva_zero`).

## Principios
- Código simple, claro, corto y mantenible.
- Sistema modular con responsabilidades bien separadas.
- Reutilizar Django antes de reescribir.
- Cambios pequeños que aporten valor inmediato.
- Todo cambio funcional debe estar cubierto por tests.

## Criterio de valor (Scrum)
Toda funcionalidad sugerida o implementada debe:
- Seguir la lógica de **Scrum**.
- Priorizar **el menor cambio posible que genere el mayor valor actual**.
- Evitar overengineering y funcionalidades a futuro sin uso inmediato.
- Preferir incrementos funcionales pequeños y validables.

## Reglas obligatorias
1. **Tests**: no se acepta código funcional sin tests.
2. **Reusar Django**: auth, admin, forms, CBVs, validaciones y utilidades nativas siempre que aplique.
3. **Modularidad**:
   - `models`: datos y validaciones.
   - `views`: orquestación HTTP.
   - `services`: lógica de negocio.
4. **No reescritura innecesaria**: refactorizar sólo si mejora claridad o reduce complejidad, siempre con tests.
5. **Estilo**: PEP8, nombres descriptivos, funciones chicas.

## Gitflow
- `main`: estable / producción  
- `develop`: integración  
- `feature/*`, `bugfix/*`, `hotfix/*`
- PRs pequeños, enfocados y con tests.

## Checklist de PR
- [ ] Tests pasan
- [ ] Cambio pequeño y con valor claro
- [ ] Sin duplicar lógica existente
- [ ] Sin credenciales
- [ ] Documentación actualizada si aplica

## Definition of Done (DoD)
Antes de cerrar un ticket, verificar:

1. **Cumplimiento del objetivo**: La funcionalidad implementada cumple con el objetivo descrito en el ticket.
2. **Tests unitarios**: Todos los tests unitarios pasan (`python manage.py test` o `pytest`).
3. **Test manual propuesto**: Incluir en el ticket/PR una descripción clara de cómo un compañero puede reproducir y validar la funcionalidad manualmente:
   - Pasos específicos a seguir.
   - Datos de prueba necesarios (si aplica).
   - Resultado esperado.
   - Casos edge o escenarios alternativos a probar.

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

## Nota para agentes
Antes de proponer código nuevo:
1. ¿Django ya lo resuelve?
2. ¿Este cambio es el mínimo necesario?
3. ¿Aporta valor hoy?
4. ¿Está cubierto por tests?
