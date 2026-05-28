-- ============================================================================
-- VERIFICATION QUERIES FOR WRONG ANSWERS
-- Run these on NeonDB to verify ground truth vs Gemini responses
-- ============================================================================

-- Q007: Average tracks per album by genre
-- Ground truth says Jazz = 2.00, Gemini says Jazz = 13.67
-- Let's check both methods:

-- METHOD 1: Using metadata column (what Gemini likely did)
SELECT 
    a.primary_genre,
    ROUND(AVG(al.total_tracks), 2) as avg_tracks_metadata
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
GROUP BY a.primary_genre
ORDER BY avg_tracks_metadata DESC;

-- METHOD 2: Counting actual tracks (ground truth method)
SELECT
    a.primary_genre,
    ROUND(AVG(track_count), 2) as avg_tracks_actual
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
JOIN (
    SELECT album_id, COUNT(*) as track_count
    FROM tracks
    GROUP BY album_id
) t ON al.album_id = t.album_id
GROUP BY a.primary_genre
ORDER BY avg_tracks_actual DESC;

-- ============================================================================
-- Q008: Artists with at least 1 award won
-- Ground truth: 6 artists (The Ortegas=12, James Brooks=1, The Bryants=1, Susan Murray MD=1, The Knights=1, The Haydens=1)
-- Gemini found: 4 artists (The Ortegas=11, The Bryants=1, Melissa Wells=1, Rodriguezx=1)
-- ============================================================================

SELECT
    a.name,
    COUNT(aw.award_id) as total_awards,
    SUM(CASE WHEN aw.won = true THEN 1 ELSE 0 END) as awards_won
FROM artists a
JOIN awards aw ON a.artist_id = aw.artist_id
GROUP BY a.artist_id, a.name
HAVING SUM(CASE WHEN aw.won = true THEN 1 ELSE 0 END) > 0
ORDER BY awards_won DESC, total_awards DESC;

-- ============================================================================
-- Q010: Top 5 tracks with highest energy + danceability
-- Ground truth: 5 tracks
-- Gemini (XML) only returned 3 tracks
-- ============================================================================

SELECT
    t.title,
    a.name as artist_name,
    tf.energy,
    tf.danceability,
    (tf.energy + tf.danceability) as combined_score
FROM tracks t
JOIN artists a ON t.artist_id = a.artist_id
JOIN track_features tf ON t.track_id = tf.track_id
ORDER BY combined_score DESC
LIMIT 5;

-- ============================================================================
-- Q012: Artists with tracks in multiple albums (album_count > 1)
-- Ground truth: 3 artists
-- Gemini found: 18 artists
-- ============================================================================

SELECT
    a.name,
    COUNT(DISTINCT al.album_id) as album_count,
    COUNT(DISTINCT t.track_id) as track_count
FROM artists a
JOIN albums al ON a.artist_id = al.artist_id
JOIN tracks t ON al.album_id = t.album_id
GROUP BY a.artist_id, a.name
HAVING COUNT(DISTINCT al.album_id) > 1
ORDER BY album_count DESC, track_count DESC;

-- ============================================================================
-- Q015: Overperforming artists
-- Ground truth formula: CAST(awards_won AS FLOAT) / NULLIF(album_count, 0)
-- Gemini (XML) used: awards / ((albums + 1) * (popularity_score + 0.001))
-- ============================================================================

-- Ground truth method:
WITH artist_metrics AS (
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
    ROUND(CAST(popularity_score AS NUMERIC), 3) as popularity,
    ROUND(CAST(award_efficiency AS NUMERIC), 2) as awards_per_album
FROM expected_awards
ORDER BY award_efficiency DESC
LIMIT 5;

-- ============================================================================
-- Q017: Genre dominance score
-- Ground truth: Rock = 0.9127
-- Gemini (XML): Rock = 2.74
-- ============================================================================

WITH genre_metrics AS (
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
    ROUND(CAST(avg_popularity AS NUMERIC), 3) as avg_popularity,
    ROUND(CAST((norm_artists + norm_albums + norm_popularity) AS NUMERIC) / 3.0, 4) as dominance_score
FROM normalized_metrics
ORDER BY dominance_score DESC;

-- ============================================================================
-- Q019: Acoustic-electronic spectrum (all genres)
-- Ground truth: Full spectrum for 10 genres
-- Gemini (XML): Only returned "Most Acoustic: Jazz, Most Electronic: Metal"
-- ============================================================================

WITH genre_audio_features AS (
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
ORDER BY acoustic_score DESC;