# Vigente — Power House Gym

Sistema de gestión de membresías, control de acceso biométrico y seguimiento de entrenamiento.

Proyecto de la materia **Desarrollo Web Integral** · Universidad Tecnológica de Durango.

---

## El problema

Power House Gym lleva el control de membresías en una hoja de cálculo y una libreta en recepción. Nada bloquea a un socio con la membresía vencida y nada avisa cuando un contrato se acaba, así que hay gente entrenando semanas sin pagar. El único control real es si el recepcionista se acuerda de la cara.

Además, como no hay registro de asistencia, tampoco hay forma de saber quién está por darse de baja hasta que ya se fue.

## Qué hace el sistema

- Vence las membresías solo, con una tarea programada que corre cada hora.
- Abre el torniquete con reconocimiento facial en menos de dos segundos, con QR como respaldo.
- Cobra desde la app, con cargo automático o manual.
- Registra entrenamientos serie por serie y detecta al socio que lleva seis semanas sin subir de peso, que es la señal de abandono que aparece antes de que baje la asistencia.

---

## Equipo

| Integrante | Rol | GitHub |
|---|---|---|
| Alexander Tinoco Sánchez | Backend y Scrum Master | [@alexander-tinoco](https://github.com/alexander-tinoco) |
| Bruno Sebastián Díaz Galván | Frontend web y móvil | [@enirois](https://github.com/enirois) |
| José Luis Guzmán Pérez | Base de datos y servicio biométrico | [@Pepe543235](https://github.com/Pepe543235) |
| Ricardo Rodríguez Alarcón | Despliegue, CI/CD y cliente | [@Richardito030](https://github.com/Richardito030) |

Tablero de trabajo: [Trello — Desarrollo Web Integral](https://trello.com/b/UjR1RLOt/desarrollo-web-integral)

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Tareas programadas | Celery + Celery Beat + Redis |
| Base de datos | PostgreSQL 16 + pgvector |
| Panel web | React 19 + Vite + TypeScript |
| App móvil | React Native + Expo |
| Servicio de borde | FastAPI + ONNX Runtime |
| Contenedores | Docker Compose |

La justificación de cada decisión está en `docs/adr/`.

---

## Cómo levantarlo

```bash
git clone https://github.com/alexander-tinoco/vigente-powerhouse-gym.git
cd vigente-powerhouse-gym
cp .env.example .env          # completar valores
docker compose up -d --build
docker compose exec core python manage.py migrate
docker compose exec core python manage.py loaddata planes_iniciales
docker compose exec core pytest
```

---

## Flujo de trabajo con Git

Usamos **GitHub Flow**: `main` siempre desplegable, una rama por tarea, Pull Request obligatorio.

```
main
 └── feat/S1-maquina-estados      Alexander
 └── feat/S1-panel-recepcion      Bruno
 └── feat/S1-modelo-datos         José Luis
 └── feat/S1-infra-despliegue     Ricardo
```

**Nomenclatura de ramas**

| Prefijo | Para qué |
|---|---|
| `feat/` | Funcionalidad nueva |
| `fix/` | Corrección de un error |
| `docs/` | Documentación y ADRs |
| `chore/` | Configuración, dependencias, infraestructura |
| `test/` | Pruebas sin cambio de comportamiento |

El nombre lleva el sprint y un identificador corto: `feat/S1-maquina-estados`.

**Reglas**

1. Nadie empuja directo a `main`.
2. Todo Pull Request necesita la aprobación de un integrante distinto al autor.
3. No se fusiona con la CI en rojo.
4. Commits siguiendo Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`.

---

## Estado

Sprint 1 (29 sep – 23 oct): estructura del proyecto, modelo de datos, máquina de estados de la membresía y panel de recepción.
