import os
import pyodbc
import pandas as pd
from tabulate import tabulate

SQL_FILE = "queries.sql"
OUT_FILE = "resultats.md"

conn_str = (
    f"DRIVER={{{os.environ['ODBC_DRIVER']}}};"
    f"SERVER={os.environ['TPBDD_SERVER']};"
    f"DATABASE={os.environ['TPBDD_DB']};"
    f"UID={os.environ['TPBDD_USERNAME']};"
    f"PWD={os.environ['TPBDD_PASSWORD']};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_(aucun résultat)_"
    return tabulate(df, headers="keys", tablefmt="github", showindex=False)

def load_queries(path: str):
    """
    Reads queries.sql and returns [(title, sql), ...]
    Each query starts with: -- Exercice X
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("-- Exercice")
    queries = []

    for block in blocks[1:]:
        lines = block.strip().splitlines()
        title = "Exercice " + lines[0].strip()
        sql = "\n".join(lines[1:]).strip().rstrip(";")
        queries.append((title, sql))

    return queries

queries = load_queries(SQL_FILE)

with pyodbc.connect(conn_str) as conn:
    output = ["# Résultats TPBDD\n"]

    for title, sql in queries:
        df = pd.read_sql(sql, conn)
        output.append(f"## {title}\n")
        output.append(md_table(df) + "\n")

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("✅ Fichier généré :", OUT_FILE)
