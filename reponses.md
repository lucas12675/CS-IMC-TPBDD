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

## Les requêtes SQL

#### Exercice 0
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS;

Cette requête sert à voir comment la base est construite.
Elle affiche toutes les tables, leurs colonnes et le type de chaque colonne.

#### Exercice 1
SELECT birthYear
FROM tArtist
WHERE primaryName = 'Hugh Grant ';


Ici, on cherche l’artiste Hugh Grant et on affiche son année de naissance.

#### Exercice 2
SELECT COUNT(*) AS nb_artistes
FROM tArtist;


Cette requête compte combien d’artistes il y a dans la base.
Le résultat est renommé nb_artistes pour que ce soit plus clair.

#### Exercice 3a
SELECT primaryName
FROM tArtist
WHERE birthYear = 1960;

On affiche les noms des artistes qui sont nés en 1960 en ajoutant une condition avec `WHERE <nom de la colonne> <condition>`

#### Exercice 3b
SELECT COUNT(*) AS nb
FROM tArtist
WHERE birthYear = 1960;

Même chose que l’exercice précédent, sauf qu’ici on compte le nombre d’artistes nés en 1960 au lieu de les afficher. COUNT(*) compte l'entièreté des lignes de la table demandée

#### Exercice 4
SELECT TOP 1 WITH TIES a.birthYear, COUNT(DISTINCT a.idArtist) AS nb_acteurs
FROM tArtist a
JOIN tJob j ON j.idArtist = a.idArtist
WHERE j.category = 'actor' AND a.birthYear <> 0
GROUP BY a.birthYear
ORDER BY nb_acteurs DESC;


Cette requête permet de trouver l’année de naissance avec le plus d’acteurs.

On garde seulement les artistes qui sont acteurs

On enlève ceux dont l’année de naissance est inconnue (0)

On compte combien d’acteurs sont nés chaque année

On prend l’année avec le plus grand nombre

TOP 1 WITH TIES permet de garder toutes les années à égalité si jamais il y en a plusieurs.

#### Exercice 5
SELECT a.primaryName, COUNT(DISTINCT j.idFilm) AS nb_films
FROM tArtist a
JOIN tJob j ON j.idArtist = a.idArtist
WHERE j.category = 'actor'
GROUP BY a.idArtist, a.primaryName
HAVING COUNT(DISTINCT j.idFilm) > 1
ORDER BY nb_films DESC, a.primaryName;


Ici, on cherche les artistes qui ont joué dans plus d’un film.

On ne garde que les rôles d’acteur

On compte le nombre de films par artiste

On filtre pour garder seulement ceux qui ont joué dans plusieurs films

On trie pour voir ceux qui ont le plus de films en premier

Exercice 6
SELECT a.primaryName, COUNT(DISTINCT j.category) AS nb_responsabilites
FROM tArtist a
JOIN tJob j ON j.idArtist = a.idArtist
GROUP BY a.idArtist, a.primaryName
HAVING COUNT(DISTINCT j.category) > 1
ORDER BY nb_responsabilites DESC, a.primaryName;


Cette requête sert à trouver les artistes qui ont eu plusieurs types de rôles
(par exemple acteur et réalisateur).

On compte le nombre de catégories différentes par artiste et on garde ceux qui en ont plus d’une.

#### Exercice 7
SELECT TOP 1 WITH TIES f.primaryTitle, COUNT(DISTINCT j.idArtist) AS nb_acteurs
FROM tFilm f
JOIN tJob j ON j.idFilm = f.idFilm
WHERE j.category = 'actor'
GROUP BY f.idFilm, f.primaryTitle
ORDER BY nb_acteurs DESC;


Cette requête permet de trouver le ou les films avec le plus d’acteurs.

On relie les films aux acteurs

On compte le nombre d’acteurs par film

On garde le maximum
S’il y a plusieurs films ex æquo, ils sont tous affichés.

#### Exercice 8
SELECT a.primaryName, f.primaryTitle, COUNT(DISTINCT j.category) AS nb_roles
FROM tJob j
JOIN tArtist a ON a.idArtist = j.idArtist
JOIN tFilm f ON f.idFilm = j.idFilm
GROUP BY a.idArtist, a.primaryName, f.idFilm, f.primaryTitle
HAVING COUNT(DISTINCT j.category) > 1
ORDER BY nb_roles DESC, a.primaryName, f.primaryTitle;


Ici, on cherche les cas où un artiste a eu plusieurs rôles dans le même film.

Par exemple : acteur et réalisateur sur un même film.
On regroupe par artiste et par film, puis on garde ceux qui ont plus d’un type de rôle.

## Conversion Neo4J

### 2.1

Pour convertir vers Neo4J on doit créer et insérer des objects: nodes et relations. Chaques lignes présentent dans les table tArtist et tFilms deviendrons une node et les relations sont représenté dans la table tJob.

Voici le code pour les nodes de Films
```bash
    # Films
    exportedCount = 0
    cursor.execute("SELECT COUNT(1) FROM tFilm")
    totalCount = cursor.fetchval()
    cursor.execute("SELECT idFilm, primaryTitle, startYear FROM tFilm") #On demande les informations des nodes dans la BDD
    while True:
        importData = []
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break

        i = 0
        for row in rows:
            # Créer un objet Node avec comme label Film et les propriétés adéquates
            n = Node("Film", idFilm=row.idFilm, primaryTitle=row.primaryTitle, startYear=row.startYear) #On map ici la table récupérée dans des nodes avec les bons champs
            importData.append(n)
            i += 1

        try:
            create_nodes(graph.auto(), importData, labels={"Film"}) #On exporte la node dans Neo4J
            exportedCount += len(rows)
            print(f"{exportedCount}/{totalCount} title records exported to Neo4j")
        except Exception as error:
            print(error)

```

Pour les relation on a :
```bash
# Relationships
    exportedCount = 0
    cursor.execute("SELECT COUNT(1) FROM tJob")
    totalCount = cursor.fetchval()
    cursor.execute(f"SELECT idArtist, category, idFilm FROM tJob") #Chaque relation utilise les id des nodes (acteurs et films)
    while True:
        importData = { "acted in": [], "directed": [], "produced": [], "composed": [] }
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break

        for row in rows:
            # tuple = (start_node_key, properties_dict, end_node_key)
            # start: idArtist, end: idFilm
            relTuple = (row.idArtist, {}, row.idFilm)
            importData[row.category].append(relTuple)

        try:
            for cat in importData:

                # On remplace les espaces par des _ pour le type de relation sinon on obtient une erreur
                rel_type = cat.replace(" ", "_").upper()

                create_relationships(
                    graph.auto(),
                    importData[cat],
                    rel_type,
                    start_node_key=("Artist", "idArtist"),
                    end_node_key=("Film", "idFilm"),
                )
```

### 2.3
On travaille dans un conteneur avec python 3.11.2 installé. L'environnement utilisé est un venv avec les requirements installé : pyodbc, py2neo, python-dotenv. Les informations de connexions ont été exportées en variable d'environnement depuis le .env

## Requête Neo4J

#### Ex 1
CREATE (Lucas:Artist { primaryName: 'Lucas Muraille'})


Cette requête crée un artiste appelé Lucas Muraille.
On ajoute un nœud avec le label Artist et on lui donne son nom grâce à la propriété primaryName.

#### Ex 2
CREATE (Lucas:Film { primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees"})


Ici, on crée un film avec pour titre L'histoire de mon 20 au cours Infrastructure de donnees.
Le film est ajouté dans la base, mais il n’est encore relié à personne.

#### Ex 3
MATCH
  (a:Artist),
  (b:Film)
WHERE a.primaryName = 'Lucas Muraille'
  AND b.primaryTitle = "L'histoire de mon 20 au cours Infrastructure de donnees"
CREATE (a)-[r:ACTED_IN]->(b)


Cette requête sert à relier Lucas au film.
On retrouve l’artiste et le film, puis on crée une relation ACTED_IN.
Cela signifie que Lucas a joué dans ce film.

#### Ex 4
CREATE (Prof1:Artist { primaryName: 'Luc VO VAN'})
CREATE (Prof2:Artist { primaryName: 'Francesca BUGIOTTI'});

MATCH
  (b:Film),
  (Prof1:Artist),
  (Prof2:Artist)
WHERE b.primaryTitle = "L'histoire de mon 20 au cours Infrastructure de donnees"
  AND Prof1.primaryName = 'Luc VO VAN'
  AND Prof2.primaryName = 'Francesca BUGIOTTI'
CREATE (Prof1)-[r:DIRECTED]->(b)
CREATE (Prof2)-[:DIRECTED]->(b);


On crée deux artistes correspondant aux professeurs.
Ensuite, on les relie au film avec la relation DIRECTED.
Cela indique que les deux professeurs ont réalisé le film.

#### Ex 5
MATCH
  (a:Artist)
WHERE a.primaryName = 'Nicole Kidman' 
RETURN a.birthYear;


Cette requête cherche l’artiste Nicole Kidman et affiche uniquement son année de naissance.
Elle permet donc de récupérer une information précise sur un artiste.

#### Ex 6
MATCH (p:Film)
RETURN p.primaryTitle;


Ici, on récupère tous les films présents dans la base.
On affiche simplement leur titre.

#### Ex 7
MATCH (p:Artist)
WHERE p.birthYear = 1963
RETURN p.primaryName;


Cette requête liste les artistes nés en 1963.
Elle filtre sur l’année de naissance et affiche leurs noms.

#### Ex 8
MATCH (p:Artist)-[:ACTED_IN]->()
WITH p, COUNT(*) AS roles
WHERE roles > 1
RETURN p.primaryName;


On cherche les artistes qui ont joué dans plus d’un film.
La requête compte le nombre de relations ACTED_IN par artiste et garde ceux qui en ont plusieurs.

#### Ex 9
MATCH (p:Artist)-[r]->()
WITH p, COUNT(DISTINCT r) AS relCount
WHERE relCount > 1
RETURN p.primaryName;


Cette requête trouve les artistes ayant plusieurs relations sortantes, peu importe le type.
Cela permet de repérer les artistes qui ont plusieurs liens dans le graphe.

#### Ex 10
MATCH (p:Artist)-[r]->(m:Film)
WITH p, m, collect(DISTINCT type(r)) AS roles
WHERE size(roles) > 1
RETURN
  p.primaryName AS artiste
ORDER BY artiste;


Ici, on cherche les artistes qui ont eu plusieurs rôles dans un même film
(par exemple acteur et réalisateur).
On récupère les types de relations et on vérifie qu’il y en a plus d’un.

#### Ex 11
MATCH (m:Film)<-[:ACTED_IN]-(a:Artist)
WITH m, COUNT(DISTINCT a) AS nbActeurs
ORDER BY nbActeurs DESC
LIMIT 1
RETURN m.primaryTitle AS film, nbActeurs;


Cette requête permet de trouver le film avec le plus d’acteurs.
On compte le nombre d’acteurs par film, on trie du plus grand au plus petit et on garde le premier.
