
import sqlite3
import pandas as pd
from pathlib import Path
 
# Conexión a la base de datos (ruta relativa, funciona en cualquier ubicación)
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "farmanorte.db"
conn = sqlite3.connect(DB_PATH)
 
# Consulta: laboratorio que más vende
query = """
SELECT "laboratorio", SUM("val_vendido") AS total_vendido
FROM "matriz_bcg"
GROUP BY "laboratorio"
ORDER BY total_vendido DESC
LIMIT 20;
"""
 
# Traemos el resultado como DataFrame
df = pd.read_sql_query(query, conn)
 
# Formateamos el total_vendido con puntos como separador de miles
df["total_vendido"] = df["total_vendido"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
 
print(df)
 
conn.close()


