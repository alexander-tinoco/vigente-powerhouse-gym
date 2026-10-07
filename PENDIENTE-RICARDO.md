# Rama de Ricardo — infraestructura y despliegue (Sprint 1)

Según la tarjeta de Trello "S1 · Ambiente, despliegue y junta con el dueño":

- [x] Docker Compose y GitHub Actions corriendo las pruebas
- [ ] Servidor de pruebas en línea para enseñarle al dueño
- [x] Junta con el dueño: precios, días de gracia y qué entregamos

## Lo que falta

1. Desplegar staging en el VPS con Caddy y TLS automático
2. Despliegue automático al fusionar a `main`
3. Respaldo diario de la base de datos
4. Proteger la rama `main` en la configuración del repositorio:
   - Requerir un pull request antes de fusionar
   - Requerir una aprobación de alguien distinto al autor
   - Requerir que la CI pase

## De la junta con el dueño (2 de octubre)

- Días de gracia: 3, no 5
- El plan de estudiante se congela en vacaciones
- El torniquete muestra el aviso de vencimiento aunque el socio esté al corriente

Borra este archivo cuando termines.
