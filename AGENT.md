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

## Nota para agentes
Antes de proponer código nuevo:
1. ¿Django ya lo resuelve?
2. ¿Este cambio es el mínimo necesario?
3. ¿Aporta valor hoy?
4. ¿Está cubierto por tests?
