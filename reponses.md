# TP BDD
## Setup env 
export env variable

export $(cat .env | xargs) && env

export one by one the env variables

## Request database

Un simple script python permet de request la database :
```python
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
# Requête
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
# Affichage Markdown pour la copie de la réponse
# ===============================
if df.empty:
    print("(aucun résultat)")
else:
    print(tabulate(df, headers="keys", tablefmt="github", showindex=False))

```

## Les requêtes
