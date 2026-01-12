import os
import pyodbc
import pandas as pd
from tabulate import tabulate

# ===============================
# Connexion
# ===============================
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

# ===============================
# 👉 MODIFIE ICI LA REQUÊTE À TESTER
# ===============================

SQL = """
SELECT birthYear
FROM tArtist
WHERE primaryName = 'Hugh Grant';
"""
# ===============================
# Exécution
# ===============================
with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql(SQL, conn)

# ===============================
# Affichage Markdown
# ===============================
if df.empty:
    print("(aucun résultat)")
else:
    print(tabulate(df, headers="keys", tablefmt="github", showindex=False))
