# LLM Data Extraction Benchmark: Structured vs. Unstructured Data

This repository contains a benchmark test designed to evaluate the ability of Large Language Models (LLMs) to accurately extract and compute data from completely unstructured text files. 

The dataset consists of 1,000 random movies (stratified by year and rating) from the IMDb database, formatted into natural language paragraphs. Below are the 5 benchmark questions, the PostgreSQL queries used to establish the "ground truth" answer key from the structured CSV, and the results.

---

### 1. The "Frequent Collaborators" Benchmark (Multi-Entity Co-occurrence)

**Question:** Which pair of actors or directors appear together in the most movies in this dataset? Name the pair and list the titles of the movies they collaborated on.

#### The SQL Query
```sql
WITH unnested_cast AS (
    SELECT DISTINCT tconst, primaryTitle, TRIM(person) AS person_name
    FROM benchmark_movies, 
    unnest(string_to_array(Cast_and_Crew, ',')) AS person
    WHERE Cast_and_Crew != 'No Cast Data'
),
pairs AS (
    SELECT 
        a.person_name AS person1, 
        b.person_name AS person2, 
        COUNT(*) as movie_count, 
        STRING_AGG(a.primaryTitle, ', ') as movies
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
| Deborah Aquila (casting_director) | Tricia Wood (casting_director) | 7 | The A-Team, Good Boy, Evan Almighty, Devil's Knot, R.I.P.D., The Spirit, Red State |

---

### 2. The "Conditional Average" Benchmark (Running Mathematics)

**Question:** Calculate the exact average user rating for all movies categorized as 'Comedy' that were released strictly between the years 2000 and 2005.

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

### 3. The 3-Way Combinatorial

**Question:** Identify the maximum number of times any Actor/Director/Producer trio collaborated on Action or Drama movies between 2001 and 2010 with a rating between 5.0 and 8.0. Then, list all trios that achieved this maximum, along with the titles of the specific movies they collaborated on.

#### The SQL Query
```sql
WITH filtered_movies AS (
    SELECT tconst, primaryTitle, genres
    FROM benchmark_movies
    WHERE startYear BETWEEN 2001 AND 2010
      AND (genres LIKE '%Action%' OR genres LIKE '%Drama%')
      AND averageRating > 5.0 
      AND averageRating < 8.0
),
cast_list AS (
    SELECT tconst, TRIM(person) AS person_name
    FROM benchmark_movies,
    unnest(string_to_array(Cast_and_Crew, ',')) AS person
),
trio_counts AS (
    SELECT 
        c1.person_name AS actor_actress, 
        c2.person_name AS director, 
        c3.person_name AS producer, 
        COUNT(*) as collaboration_count,
        STRING_AGG(f.primaryTitle, ', ') as movies
    FROM filtered_movies f
    JOIN cast_list c1 ON f.tconst = c1.tconst AND (c1.person_name LIKE '%(actor)%' OR c1.person_name LIKE '%(actress)%')
    JOIN cast_list c2 ON f.tconst = c2.tconst AND c2.person_name LIKE '%(director)%'
    JOIN cast_list c3 ON f.tconst = c3.tconst AND c3.person_name LIKE '%(producer)%'
    GROUP BY 1, 2, 3
)
SELECT * FROM trio_counts
WHERE collaboration_count = (SELECT MAX(collaboration_count) FROM trio_counts)
ORDER BY actor_actress;
```

#### Query 3 Result
| actor_actress | director | producer | collaboration_count | movies |
| :--- | :--- | :--- | :--- | :--- |
| Alba Gaïa Bellugi (actress) | Jean-Pierre Améris (director) | Fabienne Vonier (producer) | 2 | Call Me Elisabeth, Call Me Elisabeth |
| Ayesha Jhulka (actress) | Imtiaz Ali (director) | Dharmendra (producer) | 2 | Socha Na Tha, Socha Na Tha |
| Birte Heribertson (actress) | Jan Troell (director) | Christer Nilson (producer) | 2 | Everlasting Moments, Everlasting Moments |
| Birte Heribertson (actress) | Jan Troell (director) | Tero Kaukomaa (producer) | 2 | Everlasting Moments, Everlasting Moments |
| Birte Heribertson (actress) | Jan Troell (director) | Thomas Stenderup (producer) | 2 | Everlasting Moments, Everlasting Moments |
| Bruce Glover (actor) | Peter McGennis (director) | Peter McGennis (producer) | 2 | Buffalo Bushido, Buffalo Bushido |
| Carrie-Anne Moss (actress) | Nick Guthe (director) | Dana Brunetti (producer) | 2 | Mini's First Time, Mini's First Time |
| Carrie-Anne Moss (actress) | Nick Guthe (director) | Edward Bass (producer) | 2 | Mini's First Time, Mini's First Time |
| Carrie-Anne Moss (actress) | Nick Guthe (director) | Evan Astrowsky (producer) | 2 | Mini's First Time, Mini's First Time |
| Carrie-Anne Moss (actress) | Nick Guthe (director) | Kevin Spacey (producer) | 2 | Mini's First Time, Mini's First Time |
| Inge Appelt (actress) | Vinko Bresan (director) | Ivan Maloca (producer) | 2 | Will Not End Here, Will Not End Here |
| Kalabhavan Mani (actor) | Rajasenan (director) | B.Rakesh (producer) | 2 | Malayalimamanu Vanakkam, Malayalimamanu Vanakkam |
| Kalabhavan Mani (actor) | Saran (director) | B. Gurunath (producer) | 2 | Gemini, Gemini |
| Kalabhavan Mani (actor) | Saran (director) | Balasubramanian M. (producer) | 2 | Gemini, Gemini |
| Kalabhavan Mani (actor) | Saran (director) | Guhan M.S. (producer) | 2 | Gemini, Gemini |
| Kalabhavan Mani (actor) | Saran (director) | Saravanan M. (producer) | 2 | Gemini, Gemini |
| Luke Wilson (actor) | Nick Guthe (director) | Dana Brunetti (producer) | 2 | Mini's First Time, Mini's First Time |
| Luke Wilson (actor) | Nick Guthe (director) | Edward Bass (producer) | 2 | Mini's First Time, Mini's First Time |
| Luke Wilson (actor) | Nick Guthe (director) | Evan Astrowsky (producer) | 2 | Mini's First Time, Mini's First Time |
| Luke Wilson (actor) | Nick Guthe (director) | Kevin Spacey (producer) | 2 | Mini's First Time, Mini's First Time |
| Yves Verhoeven (actor) | Jeanne Waltz (director) | Didier Haudepin (producer) | 2 | A Parting Shot, A Parting Shot |
| Yves Verhoeven (actor) | Jeanne Waltz (director) | Pierre-Alain Meier (producer) | 2 | A Parting Shot, A Parting Shot |

---

### 4. The "Year-Over-Year Drop"

**Question:** Looking exclusively at movies containing the 'Sci-Fi' genre, which specific release year saw the largest drop in the average rating compared to the year immediately preceding it? State the two years and the exact difference in the average rating.

#### The SQL Query
```sql
WITH yearly_averages AS (
    SELECT startYear, AVG(averageRating) as avg_rating
    FROM benchmark_movies
    WHERE genres LIKE '%Sci-Fi%'
    GROUP BY startYear
),
year_over_year AS (
    SELECT 
        startYear as current_year,
        avg_rating as current_rating,
        LAG(startYear) OVER (ORDER BY startYear) as previous_year,
        LAG(avg_rating) OVER (ORDER BY startYear) as previous_rating,
        (avg_rating - LAG(avg_rating) OVER (ORDER BY startYear)) as rating_delta
    FROM yearly_averages
)
SELECT previous_year, current_year, ROUND(rating_delta, 2) AS largest_drop
FROM year_over_year
WHERE previous_year IS NOT NULL
ORDER BY rating_delta ASC
LIMIT 1;
```

#### Query 4 Result
| previous_year | current_year | largest_drop |
| :--- | :--- | :--- |
| 2004 | 2005 | -2.85 |

---

### 5. The "Weighted Average"

**Question:** Calculate the weighted average rating of all 'Thriller' movies released in or after the year 2015, weighted by the total number of votes (numVotes). Round your final answer to two decimal places.

#### The SQL Query
```sql
SELECT 
    ROUND(
        SUM(averageRating * numVotes) / SUM(numVotes), 
    2) AS weighted_avg_rating
FROM benchmark_movies
WHERE genres LIKE '%Thriller%'
  AND startYear >= 2015;
```

#### Query 5 Result
| weighted_avg_rating |
| :--- |

---
### Response Summaries
Check out the [response](Sprint 1/Response.md) from various LLMs.