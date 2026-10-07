# Rama de Bruno — panel de recepción (Sprint 1)

Según la tarjeta de Trello "S1 · Panel de recepción":

- [x] Formulario de alta de socio con validación
- [ ] Lista de socios con buscador y filtro por estado
- [ ] Ficha del socio con días restantes y código de activación

## Antes de empezar

El cliente de TypeScript se genera desde el OpenAPI del backend, no se escribe
a mano:

```bash
pnpm generate:api-client
```

**Importante:** los días restantes vienen calculados desde el servidor. No los
recalcules en el panel o se desincronizan cuando el dueño cambie la regla de
días de gracia (nos la cambió de 5 a 3 en la junta del 2 de octubre).

La paleta es negro #0A0A0A con lima #D6FF3D de acento, igual que la app.

Borra este archivo cuando termines.
