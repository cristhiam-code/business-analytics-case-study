# Farmanorte Analytics

## Diccionario de Datos

Este documento describe las tablas y archivos utilizados en el proyecto Farmanorte Analytics.

---

# Archivo: kardex_productos.csv

## Descripción

Contiene el inventario de productos exportado desde el sistema de la droguería.

## Información general

| Campo | Valor |
|-------|-------|
| Archivo | kardex_productos.csv |
| Área | Inventario |
| Filas | 12.670 |
| Columnas | 7 |

## Diccionario de columnas

| Columna original | Nombre canónico | Tipo esperado | Descripción |
|------------------|-----------------|---------------|-------------|
| Laboratorio | laboratorio | Texto | Laboratorio fabricante del producto. |
| Cod_Barra | codigo_barras | Texto | Código de barras del producto. |
| Producto | producto | Texto | Nombre del producto. |
| Exist_Caja | existencias_cajas | Entero | Cantidad disponible en cajas. |
| Sist_Unid | existencias_unidades | Entero | Cantidad disponible en unidades. |
| Valor_Unitar | valor_unitario | Decimal | Precio unitario del producto. |
| Valor_Total | valor_total | Decimal | Valor total del inventario del producto. |

---

## Tablas normalizadas en SQLite

### `productos`

- `codigo_barras` (TEXT, PRIMARY KEY)
- `laboratorio` (TEXT)
- `producto` (TEXT)
- `existencias_cajas` (INTEGER)
- `existencias_unidades` (INTEGER)
- `valor_unitario` (REAL)
- `valor_total` (REAL)

### `matriz_bcg`

- `codigo_barras` (TEXT, PRIMARY KEY)
- `producto` (TEXT)
- `laboratorio` (TEXT)
- `existencia` (INTEGER)
- `precio_venta` (REAL)
- `costo_promedio` (REAL)
- `unid_vendidas` (INTEGER)
- `ranking_1` (INTEGER)
- `val_vendido` (REAL)
- `ranking_2` (INTEGER)
- `rentabilidad` (REAL)
- `ranking_3` (INTEGER)
- `suma_ranking` (INTEGER)
- `ranking_final` (INTEGER)
- `grupo` (TEXT)

### `productos_especiales`

- `codigo_barras` (TEXT, PRIMARY KEY)
- `laboratorio` (TEXT)
- `descripcion_completa` (TEXT)
- `precio_venta` (REAL)
- `porcentaje_esp` (REAL)
- `valor` (REAL)
- `r30d` (INTEGER)

### `vendedores`

- `id_vendedor` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `nombre_vendedor` (TEXT, UNIQUE)

### `ventas_especiales`

- `id_venta` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `fecha` (TEXT)
- `id_vendedor` (INTEGER)
- `producto` (TEXT)
- `valor_base` (REAL)
- `cantidad` (INTEGER)
- `valor_comision` (REAL)

## Observaciones

- `Valor_Unitar` llega como texto y debe convertirse a número.
- `Cod_Barra` se tratará como texto, no como número.
