# ADR-003 · GitHub Flow como estrategia de ramas

**Fecha:** 1 de octubre de 2026
**Estado:** Aceptada
**Decide:** el equipo, propuesto por Ricardo Rodríguez

## Contexto

Somos cuatro personas trabajando en paralelo sobre áreas distintas: backend, frontend, base de datos e infraestructura. Necesitábamos un flujo de ramas que evitara que nos pisáramos sin meter ceremonia que no podemos sostener.

## Alternativas que evaluamos

**Git Flow.** Tiene `develop`, `release/`, `hotfix/` y `main`. Está pensado para productos con versiones numeradas y varias en producción al mismo tiempo. Nosotros desplegamos continuo a un solo ambiente, así que `develop` sería una rama que solo agrega un paso de fusión sin resolver nada.

**Trunk-based con commits directos a `main`.** Rápido, pero sin Pull Request no hay revisión, y la materia pide evidencia de colaboración. Además con cuatro personas aprendiendo, nadie debería fusionar sin que otro vea el código.

**GitHub Flow.** `main` siempre desplegable, una rama por tarea, Pull Request para integrar.

## Decisión

GitHub Flow.

**Nomenclatura:** `<tipo>/<sprint>-<descripcion-corta>`

| Prefijo | Para qué |
|---|---|
| `feat/` | Funcionalidad nueva |
| `fix/` | Corrección de un error |
| `docs/` | Documentación y ADRs |
| `chore/` | Configuración, dependencias, infraestructura |
| `test/` | Pruebas sin cambio de comportamiento |

Ejemplo: `feat/S1-maquina-estados`.

Incluir el sprint en el nombre hace que al mirar las ramas abiertas se vea de inmediato si alguien está arrastrando trabajo de un sprint anterior.

**Política de integración:**

1. Nadie empuja directo a `main`. La rama está protegida.
2. Todo Pull Request necesita aprobación de un integrante **distinto al autor**.
3. No se fusiona con la CI en rojo.
4. Se fusiona con *squash* para que el historial de `main` sea legible.

**Quién revisa a quién:** la revisión es cruzada y rota. Alexander revisa a José Luis, José Luis a Bruno, Bruno a Ricardo, Ricardo a Alexander. Si alguien no está disponible, revisa quien siga.

## Consecuencias

**A favor:** historial limpio, nadie fusiona su propio código, y el Pull Request deja constancia escrita de qué se discutió antes de integrar.

**En contra:** si dos personas tocan el mismo archivo hay conflicto al fusionar. Lo mitigamos con la separación por módulos del ADR-001: cada quien trabaja mayormente en su carpeta.
