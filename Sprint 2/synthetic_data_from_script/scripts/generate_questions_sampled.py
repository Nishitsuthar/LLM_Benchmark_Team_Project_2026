#!/usr/bin/env python3
"""
Generate 20 LLM Benchmark Questions for Sampled Dataset
- 6 Medium questions
- 7 Hard questions
- 7 Extremely Hard questions
"""

import pandas as pd
from pathlib import Path

# Output file
OUTPUT_FILE = Path(__file__).parent.parent.parent / 'llm_benchmark_questions_sampled.csv'

# ============================================================================
# QUESTION DEFINITIONS
# ============================================================================

questions = []

# ============================================================================
# MEDIUM QUESTIONS (6 questions)
# Basic aggregations, simple JOINs (2-3 tables), percentage calculations
# ============================================================================

questions.append({
    'question_id': 'Q001',
    'category': 'Medium',
    'question': 'Which artist has the highest popularity score and how many albums have they released?',
    'sql_query': '''SELECT a.name, a.popularity_score, COUNT(DISTINCT al.album_id) as album_count
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
WHERE a.popularity_score = (SELECT MAX(popularity_score) FROM artists)
GROUP BY a.artist_id, a.name, a.popularity_score;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q002',
    'category': 'Medium',
    'question': 'What is the average track duration in minutes across all tracks?',
    'sql_query': '''SELECT ROUND(AVG(duration_ms) / 1000.0 / 60.0, 2) as avg_duration_minutes
FROM tracks;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q003',
    'category': 'Medium',
    'question': 'Which music genre has the most artists and how many?',
    'sql_query': '''SELECT primary_genre, COUNT(*) as artist_count
FROM artists
GROUP BY primary_genre
ORDER BY artist_count DESC
LIMIT 1;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q004',
    'category': 'Medium',
    'question': 'What percentage of artists are currently active?',
    'sql_query': '''SELECT
    ROUND(100.0 * SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END) / COUNT(*), 2) as active_percentage
FROM artists;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q005',
    'category': 'Medium',
    'question': 'How many tracks have explicit content?',
    'sql_query': '''SELECT COUNT(*) as explicit_tracks
FROM tracks
WHERE is_explicit = true;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q006',
    'category': 'Medium',
    'question': 'Which record label has signed the most artists?',
    'sql_query': '''SELECT rl.name, COUNT(a.artist_id) as artist_count
FROM record_labels rl
JOIN artists a ON rl.label_id = a.label_id
GROUP BY rl.label_id, rl.name
ORDER BY artist_count DESC
LIMIT 1;''',
    'answer': ''
})

# ============================================================================
# HARD QUESTIONS (7 questions)
# Complex JOINs (4+ tables), CTEs, window functions, conditional aggregations
# ============================================================================

questions.append({
    'question_id': 'Q007',
    'category': 'Hard',
    'question': 'What is the average number of tracks per album for each genre?',
    'sql_query': '''SELECT
    a.primary_genre,
    ROUND(AVG(track_count), 2) as avg_tracks_per_album
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
JOIN (
    SELECT album_id, COUNT(*) as track_count
    FROM tracks
    GROUP BY album_id
) t ON al.album_id = t.album_id
GROUP BY a.primary_genre
ORDER BY avg_tracks_per_album DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q008',
    'category': 'Hard',
    'question': 'Which artists have won at least one award and how many awards have they won in total?',
    'sql_query': '''SELECT
    a.name,
    COUNT(aw.award_id) as total_awards,
    SUM(CASE WHEN aw.won = true THEN 1 ELSE 0 END) as awards_won
FROM artists a
JOIN awards aw ON a.artist_id = aw.artist_id
GROUP BY a.artist_id, a.name
HAVING SUM(CASE WHEN aw.won = true THEN 1 ELSE 0 END) > 0
ORDER BY awards_won DESC, total_awards DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q009',
    'category': 'Hard',
    'question': 'What is the distribution of album types (Single, EP, Album) by record label type (Major, Independent)?',
    'sql_query': '''SELECT
    rl.label_type,
    al.album_type,
    COUNT(*) as count
FROM record_labels rl
JOIN artists a ON rl.label_id = a.label_id
JOIN albums al ON a.artist_id = al.artist_id
GROUP BY rl.label_type, al.album_type
ORDER BY rl.label_type, count DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q010',
    'category': 'Hard',
    'question': 'Which tracks have the highest energy and danceability scores combined?',
    'sql_query': '''SELECT
    t.title,
    a.name as artist_name,
    tf.energy,
    tf.danceability,
    (tf.energy + tf.danceability) as combined_score
FROM tracks t
JOIN artists a ON t.artist_id = a.artist_id
JOIN track_features tf ON t.track_id = tf.track_id
ORDER BY combined_score DESC
LIMIT 5;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q011',
    'category': 'Hard',
    'question': 'What is the average popularity score for artists from each country?',
    'sql_query': '''SELECT
    country,
    COUNT(*) as artist_count,
    ROUND(AVG(popularity_score), 3) as avg_popularity
FROM artists
GROUP BY country
ORDER BY avg_popularity DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q012',
    'category': 'Hard',
    'question': 'Which artists have tracks in multiple albums and how many albums do they have?',
    'sql_query': '''SELECT
    a.name,
    COUNT(DISTINCT al.album_id) as album_count,
    COUNT(DISTINCT t.track_id) as track_count
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
JOIN tracks t ON al.album_id = t.album_id
GROUP BY a.artist_id, a.name
HAVING COUNT(DISTINCT al.album_id) > 1
ORDER BY album_count DESC, track_count DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q013',
    'category': 'Hard',
    'question': 'What is the average speechiness score for explicit vs non-explicit tracks?',
    'sql_query': '''SELECT
    t.is_explicit,
    COUNT(*) as track_count,
    ROUND(AVG(tf.speechiness), 3) as avg_speechiness
FROM tracks t
JOIN track_features tf ON t.track_id = tf.track_id
GROUP BY t.is_explicit
ORDER BY t.is_explicit DESC;''',
    'answer': ''
})

# ============================================================================
# EXTREMELY HARD QUESTIONS (7 questions)
# Multiple nested CTEs, advanced window functions, complex business logic
# ============================================================================

questions.append({
    'question_id': 'Q014',
    'category': 'Extremely Hard',
    'question': 'Calculate the "musical diversity score" for each artist based on the variance of their track features (energy, danceability, valence). Which artist has the highest diversity?',
    'sql_query': '''WITH artist_track_features AS (
    SELECT
        a.artist_id,
        a.name,
        tf.energy,
        tf.danceability,
        tf.valence
    FROM artists a
    JOIN albums al ON a.artist_id = al.artist_id
    JOIN tracks t ON al.album_id = t.album_id
    JOIN track_features tf ON t.track_id = tf.track_id
),
feature_variance AS (
    SELECT
        artist_id,
        name,
        VARIANCE(energy) as energy_var,
        VARIANCE(danceability) as dance_var,
        VARIANCE(valence) as valence_var
    FROM artist_track_features
    GROUP BY artist_id, name
    HAVING COUNT(*) >= 2
)
SELECT
    name,
    ROUND((energy_var + dance_var + valence_var) / 3.0, 4) as diversity_score
FROM feature_variance
ORDER BY diversity_score DESC
LIMIT 5;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q015',
    'category': 'Extremely Hard',
    'question': 'Identify "overperforming" artists: those whose award count is disproportionately high relative to their album count and popularity score.',
    'sql_query': '''WITH artist_metrics AS (
    SELECT
        a.artist_id,
        a.name,
        a.popularity_score,
        COUNT(DISTINCT al.album_id) as album_count,
        COUNT(DISTINCT aw.award_id) as award_count,
        SUM(CASE WHEN aw.won = true THEN 1 ELSE 0 END) as awards_won
    FROM artists a
    LEFT JOIN albums al ON a.artist_id = al.artist_id
    LEFT JOIN awards aw ON a.artist_id = aw.artist_id
    GROUP BY a.artist_id, a.name, a.popularity_score
),
expected_awards AS (
    SELECT
        *,
        CASE
            WHEN album_count > 0 THEN (popularity_score * album_count * 10)
            ELSE 0
        END as expected_award_score,
        CASE
            WHEN album_count > 0 THEN CAST(awards_won AS FLOAT) / NULLIF(album_count, 0)
            ELSE 0
        END as award_efficiency
    FROM artist_metrics
    WHERE awards_won > 0
)
SELECT
    name,
    album_count,
    awards_won,
    ROUND(popularity_score, 3) as popularity,
    ROUND(award_efficiency, 2) as awards_per_album
FROM expected_awards
ORDER BY award_efficiency DESC
LIMIT 5;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q016',
    'category': 'Extremely Hard',
    'question': 'Create a "track mood profile" by categorizing tracks based on valence and energy into quadrants (Happy/High Energy, Happy/Low Energy, Sad/High Energy, Sad/Low Energy). What is the distribution?',
    'sql_query': '''WITH mood_classification AS (
    SELECT
        t.track_id,
        t.title,
        tf.valence,
        tf.energy,
        CASE
            WHEN tf.valence >= 0.5 AND tf.energy >= 0.5 THEN 'Happy_HighEnergy'
            WHEN tf.valence >= 0.5 AND tf.energy < 0.5 THEN 'Happy_LowEnergy'
            WHEN tf.valence < 0.5 AND tf.energy >= 0.5 THEN 'Sad_HighEnergy'
            WHEN tf.valence < 0.5 AND tf.energy < 0.5 THEN 'Sad_LowEnergy'
        END as mood_quadrant
    FROM tracks t
    JOIN track_features tf ON t.track_id = tf.track_id
)
SELECT
    mood_quadrant,
    COUNT(*) as track_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM mood_classification
GROUP BY mood_quadrant
ORDER BY track_count DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q017',
    'category': 'Extremely Hard',
    'question': 'Calculate the "genre dominance score" for each genre based on artist count, album count, and average popularity. Which genre is most dominant?',
    'sql_query': '''WITH genre_metrics AS (
    SELECT
        a.primary_genre,
        COUNT(DISTINCT a.artist_id) as artist_count,
        COUNT(DISTINCT al.album_id) as album_count,
        AVG(a.popularity_score) as avg_popularity
    FROM artists a
    LEFT JOIN albums al ON a.artist_id = al.artist_id
    GROUP BY a.primary_genre
),
normalized_metrics AS (
    SELECT
        primary_genre,
        artist_count,
        album_count,
        avg_popularity,
        CAST(artist_count AS FLOAT) / NULLIF(MAX(artist_count) OVER(), 0) as norm_artists,
        CAST(album_count AS FLOAT) / NULLIF(MAX(album_count) OVER(), 0) as norm_albums,
        avg_popularity / NULLIF(MAX(avg_popularity) OVER(), 0) as norm_popularity
    FROM genre_metrics
)
SELECT
    primary_genre,
    artist_count,
    album_count,
    ROUND(avg_popularity, 3) as avg_popularity,
    ROUND((norm_artists + norm_albums + norm_popularity) / 3.0, 4) as dominance_score
FROM normalized_metrics
ORDER BY dominance_score DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q018',
    'category': 'Extremely Hard',
    'question': 'Identify "prolific years" for the music industry by counting albums released per year and calculating the year-over-year growth rate.',
    'sql_query': '''WITH yearly_albums AS (
    SELECT
        release_year,
        COUNT(*) as album_count
    FROM albums
    WHERE release_year IS NOT NULL
    GROUP BY release_year
),
growth_calculation AS (
    SELECT
        release_year,
        album_count,
        LAG(album_count) OVER (ORDER BY release_year) as prev_year_count,
        album_count - LAG(album_count) OVER (ORDER BY release_year) as absolute_growth,
        CASE
            WHEN LAG(album_count) OVER (ORDER BY release_year) > 0 THEN
                ROUND(100.0 * (album_count - LAG(album_count) OVER (ORDER BY release_year)) /
                      LAG(album_count) OVER (ORDER BY release_year), 2)
            ELSE NULL
        END as growth_rate_pct
    FROM yearly_albums
)
SELECT
    release_year,
    album_count,
    prev_year_count,
    absolute_growth,
    growth_rate_pct
FROM growth_calculation
WHERE growth_rate_pct IS NOT NULL
ORDER BY growth_rate_pct DESC
LIMIT 5;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q019',
    'category': 'Extremely Hard',
    'question': 'Calculate the "acoustic-electronic spectrum" for each genre by averaging acousticness and instrumentalness. Which genres are most acoustic vs electronic?',
    'sql_query': '''WITH genre_audio_features AS (
    SELECT
        a.primary_genre,
        AVG(tf.acousticness) as avg_acousticness,
        AVG(tf.instrumentalness) as avg_instrumentalness
    FROM artists a
    JOIN albums al ON a.artist_id = al.artist_id
    JOIN tracks t ON al.album_id = t.album_id
    JOIN track_features tf ON t.track_id = tf.track_id
    GROUP BY a.primary_genre
)
SELECT
    primary_genre,
    ROUND(avg_acousticness, 3) as avg_acousticness,
    ROUND(avg_instrumentalness, 3) as avg_instrumentalness,
    ROUND((avg_acousticness + avg_instrumentalness) / 2.0, 3) as acoustic_score,
    CASE
        WHEN (avg_acousticness + avg_instrumentalness) / 2.0 >= 0.5 THEN 'Acoustic'
        ELSE 'Electronic'
    END as spectrum_classification
FROM genre_audio_features
ORDER BY acoustic_score DESC;''',
    'answer': ''
})

questions.append({
    'question_id': 'Q020',
    'category': 'Extremely Hard',
    'question': 'Identify "hidden gem" tracks: high audio quality features (low speechiness, high instrumentalness) from less popular artists (popularity < 0.5) that have not been heavily streamed.',
    'sql_query': '''WITH track_metrics AS (
    SELECT
        t.track_id,
        t.title,
        a.name as artist_name,
        a.popularity_score,
        tf.speechiness,
        tf.instrumentalness,
        COALESCE(SUM(s.stream_count), 0) as total_streams
    FROM tracks t
    JOIN artists a ON t.artist_id = a.artist_id
    JOIN track_features tf ON t.track_id = tf.track_id
    LEFT JOIN streams s ON t.track_id = s.track_id
    GROUP BY t.track_id, t.title, a.name, a.popularity_score, tf.speechiness, tf.instrumentalness
),
quality_score AS (
    SELECT
        *,
        (1.0 - speechiness) + instrumentalness as gem_score
    FROM track_metrics
    WHERE popularity_score < 0.5
      AND speechiness < 0.3
      AND instrumentalness > 0.3
)
SELECT
    title,
    artist_name,
    ROUND(popularity_score, 3) as artist_popularity,
    ROUND(speechiness, 3) as speechiness,
    ROUND(instrumentalness, 3) as instrumentalness,
    total_streams,
    ROUND(gem_score, 3) as hidden_gem_score
FROM quality_score
ORDER BY gem_score DESC
LIMIT 5;''',
    'answer': ''
})

# ============================================================================
# CREATE CSV
# ============================================================================

def main():
    print("="*80)
    print("GENERATING LLM BENCHMARK QUESTIONS FOR SAMPLED DATASET")
    print("="*80)
    print(f"\nTotal questions: {len(questions)}")
    print(f"  - Medium: {sum(1 for q in questions if q['category'] == 'Medium')}")
    print(f"  - Hard: {sum(1 for q in questions if q['category'] == 'Hard')}")
    print(f"  - Extremely Hard: {sum(1 for q in questions if q['category'] == 'Extremely Hard')}")

    # Create DataFrame
    df = pd.DataFrame(questions)

    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✓ Questions saved to: {OUTPUT_FILE.name}")
    print("\nNext steps:")
    print("  1. Run these queries on your NeonDB (sampled data)")
    print("  2. Fill in the 'answer' column with query results")
    print("  3. Use this file for GPT benchmarking")
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
