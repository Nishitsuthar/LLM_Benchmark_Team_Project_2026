# LLM Data Extraction Benchmark: Structured vs. Unstructured Data

This repository contains a benchmark test designed to evaluate the ability of Large Language Models (LLMs) to accurately extract and compute data from completely unstructured text files. 

The dataset consists of 1,000 random movies (stratified by year and rating) from the IMDb database, formatted into natural language paragraphs. Below are the 5 benchmark questions, the PostgreSQL queries used to establish the "ground truth" answer key from the structured CSV, and the results.

---

### 1. The "Frequent Collaborators" Benchmark (Multi-Entity Co-occurrence)

**Question:** Which pair of actors or directors appear together in the most movies in this dataset? Name the pair and list the titles of the movies they collaborated on.

**Why this breaks LLMs:** LLMs struggle with large-scale combinatorial matching. To answer this from unstructured text, the model must cross-reference every cast list with every other cast list and maintain a perfect running tally of pairs.

#### The SQL Query
```sql
WITH unnested_cast AS (
    SELECT tconst, primaryTitle, TRIM(person) AS person_name
    FROM benchmark_movies, 
    unnest(string_to_array(Cast_and_Crew, ',')) AS person
    WHERE Cast_and_Crew != 'No Cast Data'
),
pairs AS (
    SELECT a.person_name AS person1, b.person_name AS person2, COUNT(*) as movie_count, STRING_AGG(a.primaryTitle, ', ') as movies
    FROM unnested_cast a
    JOIN unnested_cast b 
      ON a.tconst = b.tconst AND a.person_name < b.person_name
    GROUP BY 1, 2
)
SELECT person1, person2, movie_count, movies
FROM pairs
ORDER BY movie_count DESC
LIMIT 1;
```

#### Query 1 Result
| person1 | person2 | movie_count | movies |
| :--- | :--- | :--- | :--- |
| Akira Ishida (actor) | Megumi Hayashibara (actress) | 9 | Evangelion: 3.0 You Can (Not) Redo, Evangelion: 3.0 You Can (Not) Redo, Evangelion: 3.0 You Can (Not) Redo, A Chinese Ghost Story: The Tsui Hark Animation, Neon Genesis Evangelion: The End of Evangelion, Neon Genesis Evangelion: The End of Evangelion, A Chinese Ghost Story: The Tsui Hark Animation, A Chinese Ghost Story: The Tsui Hark Animation, A Chinese Ghost Story: The Tsui Hark Animation |

---

### 2. The "Conditional Average" Benchmark (Running Mathematics)

**Question:** Calculate the exact average user rating for all movies categorized as 'Comedy' that were released strictly between the years 2000 and 2005.

**Why this breaks LLMs:** LLMs cannot natively perform bulk mathematics. The model must accurately extract the rating of every applicable comedy, hold those floats in its context window, sum them, and divide without skipping a single record.

#### The SQL Query
```sql
SELECT 
    ROUND(AVG(averageRating), 2) AS exact_avg_rating,
    COUNT(*) as total_comedies_found
FROM benchmark_movies
WHERE genres LIKE '%Comedy%' 
  AND startYear BETWEEN 2000 AND 2005;
```

#### Query 2 Result
| exact_avg_rating | total_comedies_found |
| :--- | :--- |
| 5.99 | 101 |

---

### 3. The "Prolific but Poor" Benchmark (Grouping and Thresholding)

**Question:** Identify the single actor or director who is associated with the highest total number of movies rated strictly below 5.0. How many low-rated movies are they credited in?

**Why this breaks LLMs:** This requires the model to filter records based on a numerical threshold, extract every human entity from the surviving records, and construct an invisible frequency dictionary to find the maximum. 

#### The SQL Query
```sql
WITH unnested_bad_cast AS (
    SELECT TRIM(person) AS person_name
    FROM benchmark_movies, 
    unnest(string_to_array(Cast_and_Crew, ',')) AS person
    WHERE averageRating < 5.0 
      AND Cast_and_Crew != 'No Cast Data'
)
SELECT person_name, COUNT(*) as bad_movie_count
FROM unnested_bad_cast
GROUP BY person_name
ORDER BY bad_movie_count DESC
LIMIT 1;
```

#### Query 3 Result
| person_name | bad_movie_count |
| :--- | :--- |
| Vinnie Jones (actor) | 4 |

---

### 4. The "Negative Space" Benchmark (Identifying Absence)

**Question:** Are there any years in this dataset where not a single 'Action' movie received a rating of 8.0 or higher? If so, list the specific years.

**Why this breaks LLMs:** AI models are generative; they are designed to find and produce existing data. Identifying the *absence* of data requires mapping all successful action movies to a timeline and subtracting that from the absolute dataset boundaries.

#### The SQL Query
```sql
WITH all_years AS (
    SELECT DISTINCT startYear FROM benchmark_movies
),
years_with_good_action AS (
    SELECT DISTINCT startYear FROM benchmark_movies
    WHERE genres LIKE '%Action%' AND averageRating >= 8.0
)
SELECT a.startYear AS missing_years
FROM all_years a
LEFT JOIN years_with_good_action g ON a.startYear = g.startYear
WHERE g.startYear IS NULL
ORDER BY a.startYear;
```

#### Query 4 Result
| missing_years |
| :--- |
| 2001 |
| 2002 |
| 2004 |
| 2007 |
| 2011 |
| 2013 |
| 2014 |
| 2015 |

---

### 5. The "Opposing Metrics" Benchmark (Sorting by Secondary Traits)

**Question:** Among all the movies in the dataset that received more than 500,000 user votes, which one has the absolute lowest average rating?

**Why this breaks LLMs:** This mixes large-number extraction (filtering by a 6-digit integer) with complex comparative sorting (organizing the remaining pool by a separate decimal value). It easily causes context-window confusion.

#### The SQL Query
```sql
SELECT primaryTitle, startYear, numVotes, averageRating
FROM benchmark_movies
WHERE numVotes > 500000
ORDER BY averageRating ASC
LIMIT 1;
```

#### Query 5 Result
| primarytitle | startyear | numvotes | averagerating |
| :--- | :--- | :--- | :--- |
| The Amazing Spider-Man | 2012 | 760969 | 6.9 |

