# ADR-002 · pgvector dentro de PostgreSQL en vez de una base vectorial dedicada

**Fecha:** 1 de octubre de 2026
**Estado:** Aceptada
**Decide:** el equipo, propuesto por José Luis Guzmán

## Contexto

El reconocimiento facial no guarda fotos. Guarda un vector de 512 dimensiones por socio, y para identificar a alguien hay que buscar el vector más parecido entre todos los registrados.

Eso es una búsqueda por similitud, no una consulta relacional normal, así que había que decidir dónde vivía ese índice.

## Alternativas que evaluamos

**Base vectorial dedicada** (Pinecone, Qdrant, Milvus). Están hechas para esto y escalan a millones de vectores. Pero significan un componente más que levantar, respaldar, monitorear y mantener sincronizado con PostgreSQL, y el socio quedaría partido entre dos bases: sus datos en una, su cara en otra.

**pgvector como extensión de PostgreSQL.** La búsqueda por similitud coseno se hace con SQL normal, dentro de la misma transacción y el mismo respaldo que el resto de los datos.

## Decisión

pgvector dentro de PostgreSQL 16.

Con menos de 5,000 socios, una búsqueda por similitud coseno en pgvector responde en milisegundos. Agregar una segunda base de datos para eso sería exactamente el tipo de sobreingeniería que decidimos evitar en el ADR-001.

Hay un beneficio adicional que pesó: cuando un socio ejerce su derecho de cancelación bajo la LFPDPPP, borrar su registro borra su vector en la misma operación. Con dos bases separadas habría que coordinar dos borrados y existe el riesgo de que uno falle en silencio.

## Consecuencias

**A favor:** un componente menos, respaldo único, borrado atómico de datos personales, y el equipo solo tiene que saber SQL.

**En contra:** si el padrón creciera a decenas de miles de socios habría que medir de nuevo el desempeño. El umbral donde pgvector deja de ser suficiente está muy por encima del tamaño de este gimnasio.
