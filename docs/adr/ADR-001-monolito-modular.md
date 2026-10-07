# ADR-001 · Monolito modular en vez de microservicios

**Fecha:** 29 de septiembre de 2026
**Estado:** Aceptada
**Decide:** el equipo, propuesto por Alexander Tinoco

## Contexto

Power House Gym tiene alrededor de 800 socios. El sistema tiene que servir a tres clientes distintos: el panel web de recepción y dirección, la aplicación móvil del socio, y el torniquete.

Teníamos que decidir cómo repartir la lógica de negocio entre servicios.

## Alternativas que evaluamos

**Monolito clásico renderizado en el servidor.** Queda descartado de entrada: hay una aplicación móvil nativa, y eso obliga a exponer una API. El servidor no puede renderizar la interfaz del socio.

**Microservicios.** Permitiría escalar y desplegar cada módulo por separado. Para 800 socios eso no compra nada y cuesta mucho: habría que montar orquestación, descubrimiento de servicios y manejar consistencia eventual entre bases de datos. Sería escalar por moda.

**Monolito modular orientado a API.** Una sola base de código con los módulos separados por carpeta (`identidad`, `membresias`, `cobranza`, `accesos`, `biometria`, `entrenamiento`, `permanencia`, `notificaciones`), una sola base de datos, una API que sirve a los tres clientes.

## Decisión

Monolito modular orientado a API, con **un único servicio satélite** corriendo físicamente junto al torniquete.

La separación de ese servicio **no es por escalabilidad**. Son tres razones funcionales:

1. **Continuidad sin red.** Si se cae el internet del gimnasio, el torniquete tiene que seguir abriendo para los socios vigentes. El servicio de borde guarda una copia local cifrada de los vectores y las vigencias, y encola los eventos para sincronizar después.
2. **Latencia.** La identificación tiene que resolverse en menos de dos segundos. Mandar la imagen a un servidor remoto mete latencia variable sin necesidad.
3. **Minimización de datos.** La imagen del rostro nunca sale del dispositivo. Solo viaja el vector matemático y el identificador del socio. Eso reduce muchísimo la superficie de riesgo legal con datos biométricos.

## Consecuencias

**A favor:** un solo despliegue, transacciones directas sin consistencia eventual, un solo esquema de base de datos que migrar, y un equipo de cuatro personas puede mantenerlo.

**En contra:** si el gimnasio creciera a varias sucursales con mucho volumen, habría que revisar la decisión. La estructura por módulos está pensada para que esa separación sea posible después sin reescribir todo.
