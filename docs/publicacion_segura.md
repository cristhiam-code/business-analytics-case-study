# Publicación segura — versión safe publish

Esta versión del repositorio está preparada para presentarse como caso de análisis de negocio en GitHub o LinkedIn sin exponer información operativa sensible.

## Qué se mantiene público

La versión pública debe incluir:

- código fuente de limpieza, importación y normalización,
- consultas SQL y documentación de negocio,
- notebook con narrativa analítica,
- datos procesados agregados o ya no sensibles,
- documentación técnica y de hallazgos.

## Qué debe quedarse local

Los siguientes artefactos no deben publicarse en el repositorio abierto:

- `data/raw/`
- `database/*.db`
- `database/*.db.bak`
- archivos con información operativa detallada o identificadores internos

## Política recomendada

1. Mantener el código y la narrativa pública.
2. Excluir la base local y las fuentes crudas del repositorio abierto.
3. Usar únicamente los outputs ya preparados para análisis de negocio.
4. Documentar claramente que la ejecución completa requiere datos locales no públicos.

## Objetivo

La versión safe publish permite mostrar el valor analítico del proyecto sin comprometer datos reales de operación.
