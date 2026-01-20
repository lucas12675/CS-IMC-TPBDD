-- Exercice 0
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- Exercice 1
SELECT birthYear
FROM tArtist
WHERE primaryName = 'Hugh Grant ';

-- Exercice 2
SELECT COUNT(*) AS nb_artistes
FROM tArtist;

-- Exercice 3a
SELECT primaryName
FROM tArtist
WHERE birthYear = 1960;

-- Exercice 3b
SELECT COUNT(*) AS nb
FROM tArtist
WHERE birthYear = 1960;

-- Exercice 4
SELECT TOP 1 WITH TIES a.birthYear, COUNT(DISTINCT a.idArtist) AS nb_acteurs
FROM tArtist a
JOIN tJob j ON j.idArtist = a.idArtist
WHERE j.category = 'actor' AND a.birthYear <> 0
GROUP BY a.birthYear
ORDER BY nb_acteurs DESC;

-- Exercice 5
SELECT a.primaryName, COUNT(DISTINCT j.idFilm) AS nb_films
FROM tArtist a
JOIN tJob j ON j.idArtist = a.idArtist
WHERE j.category = 'actor'
GROUP BY a.idArtist, a.primaryName
HAVING COUNT(DISTINCT j.idFilm) > 1
ORDER BY nb_films DESC, a.primaryName;

-- Exercice 6
SELECT a.primaryName, COUNT(DISTINCT j.category) AS nb_responsabilites
FROM tArtist a
JOIN tJob j ON j.idArtist = a.idArtist
GROUP BY a.idArtist, a.primaryName
HAVING COUNT(DISTINCT j.category) > 1
ORDER BY nb_responsabilites DESC, a.primaryName;

-- Exercice 7
SELECT TOP 1 WITH TIES f.primaryTitle, COUNT(DISTINCT j.idArtist) AS nb_acteurs
FROM tFilm f
JOIN tJob j ON j.idFilm = f.idFilm
WHERE j.category = 'actor'
GROUP BY f.idFilm, f.primaryTitle
ORDER BY nb_acteurs DESC;

-- Exercice 8
SELECT a.primaryName, f.primaryTitle, COUNT(DISTINCT j.category) AS nb_roles
FROM tJob j
JOIN tArtist a ON a.idArtist = j.idArtist
JOIN tFilm f ON f.idFilm = j.idFilm
GROUP BY a.idArtist, a.primaryName, f.idFilm, f.primaryTitle
HAVING COUNT(DISTINCT j.category) > 1
ORDER BY nb_roles DESC, a.primaryName, f.primaryTitle;
