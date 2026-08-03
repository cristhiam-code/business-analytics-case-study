# Farmanorte Analytics

## Diccionario de datos ejecutivo

Este documento describe el contexto del dato en el proyecto, su rol dentro del análisis y su utilidad para decisiones de negocio.

## 1. ¿Qué representa este proyecto?

El proyecto combina información de inventario, ventas y comercialización para responder preguntas de negocio sobre:

- valor generado por laboratorio,
- desempeño de productos,
- estado del inventario,
- métricas de participación comercial.

## 2. Archivos y tablas principales

### `kardex_productos.csv`

Fuente base de inventario. Su objetivo principal es describir el stock disponible por producto y laboratorio.

### `productos`

Tabla central del análisis de inventario.

- `codigo_barras`: identificador único del artículo.
- `laboratorio`: laboratorio asociado al producto.
- `producto`: nombre del producto.
- `existencias_cajas`: cantidad disponible en cajas.
- `existencias_unidades`: cantidad disponible en unidades.
- `valor_unitario`: precio unitario del artículo.
- `valor_total`: valor total del inventario asociado.

### `matriz_bcg`

Tabla analítica que permite evaluar valor comercial, rotación y rentabilidad relativa.

- `codigo_barras`: producto clave.
- `producto`: nombre del producto.
- `laboratorio`: laboratorio responsable.
- `existencia`: unidades en inventario.
- `precio_venta`: precio de venta del producto.
- `unid_vendidas`: volumen vendido.
- `val_vendido`: valor comercial generado.
- `rentabilidad`: margen o rendimiento asociado al producto.
- `ranking_final`: posición relativa del producto dentro del ranking analítico.
- `grupo`: agrupación o segmento del producto dentro de la matriz.

### `productos_especiales`

Tabla de productos con condiciones especiales o promociones.

- `codigo_barras`: identidad del producto.
- `laboratorio`: laboratorio.
- `descripcion_completa`: descripción del producto.
- `precio_venta`: precio de venta.
- `porcentaje_esp`: porcentaje asociado al producto especial.
- `valor`: valor comercial estimado.
- `r30d`: indicador de la promoción o beneficio asociado.

### `vendedores`

Tabla de identificación de vendedores.

- `id_vendedor`: identificador interno.
- `nombre_vendedor`: nombre del vendedor.

### `ventas_especiales`

Tabla transaccional de ventas especiales.

- `fecha`: fecha de la venta.
- `id_vendedor`: vínculo con el vendedor.
- `producto`: producto comercializado.
- `valor_base`: valor base de la venta.
- `cantidad`: cantidad vendida.
- `valor_comision`: comisión asociada.

## 3. KPI del proyecto

### `val_vendido`

Indica el valor generado por un producto o laboratorio. Es una de las métricas más importantes para entender qué líneas aportan más al negocio.

### `existencia`

Muestra la cantidad disponible en inventario. Sirve para detectar riesgo de desabastecimiento o sobre-stock.

### `rentabilidad`

Ayuda a entender cuán eficiente es el producto desde la perspectiva de margen o retorno asociado.

### `unid_vendidas`

Permite medir la rotación o volumen comercial por producto.

### `valor_stock`

Se calcula como el valor asociado al inventario disponible. Es clave para evaluar qué elementos del stock requieren una revisión operativa.

## 4. Observaciones técnicas relevantes

- El archivo base de inventario llega con nombres de columnas en formato no canónico y debe normalizarse.
- El código de barras se maneja como texto para evitar pérdida de integridad.
- Los valores monetarios se convierten a tipos numéricos para permitir agregaciones y rankings.
- El análisis se apoya en SQL para responder preguntas de negocio de forma reproducible.

## 5. Uso práctico del diccionario

Este diccionario sirve para que cualquier lector del proyecto comprenda:

- qué está midiendo cada tabla,
- qué significa cada KPI,
- por qué importan esas métricas para el negocio,
- y dónde cada campo encaja dentro del caso analítico general.
