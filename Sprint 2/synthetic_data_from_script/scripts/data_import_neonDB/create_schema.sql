-- ============================================================================
-- NeonDB Schema Creation Script for Music Industry Synthetic Data
-- ============================================================================
-- This script creates all tables with proper relationships and constraints
-- Run this BEFORE importing CSV data

-- Drop existing tables (if any) in correct order to handle foreign keys
DROP TABLE IF EXISTS charts CASCADE;
DROP TABLE IF EXISTS awards CASCADE;
DROP TABLE IF EXISTS playlists CASCADE;
DROP TABLE IF EXISTS royalties CASCADE;
DROP TABLE IF EXISTS streams CASCADE;
DROP TABLE IF EXISTS collaborations CASCADE;
DROP TABLE IF EXISTS track_features CASCADE;
DROP TABLE IF EXISTS tracks CASCADE;
DROP TABLE IF EXISTS albums CASCADE;
DROP TABLE IF EXISTS artists CASCADE;
DROP TABLE IF EXISTS record_labels CASCADE;

-- ============================================================================
-- 1. RECORD LABELS (Root table - no dependencies)
-- ============================================================================
CREATE TABLE record_labels (
    label_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    founding_year INTEGER,
    label_type VARCHAR(50),
    royalty_rate_per_stream DECIMAL(10, 5)
);

CREATE INDEX idx_labels_country ON record_labels(country);
CREATE INDEX idx_labels_type ON record_labels(label_type);

-- ============================================================================
-- 2. ARTISTS (Depends on: record_labels)
-- ============================================================================
CREATE TABLE artists (
    artist_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    primary_genre VARCHAR(50),
    secondary_genre VARCHAR(50),
    debut_year INTEGER,
    label_id VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    popularity_score DECIMAL(5, 3),

    FOREIGN KEY (label_id) REFERENCES record_labels(label_id)
);

CREATE INDEX idx_artists_genre ON artists(primary_genre);
CREATE INDEX idx_artists_label ON artists(label_id);
CREATE INDEX idx_artists_popularity ON artists(popularity_score);

-- ============================================================================
-- 3. ALBUMS (Depends on: artists)
-- ============================================================================
CREATE TABLE albums (
    album_id VARCHAR(20) PRIMARY KEY,
    artist_id VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    release_year INTEGER,
    release_date DATE,
    primary_genre VARCHAR(50),
    secondary_genre VARCHAR(50),
    album_type VARCHAR(50),
    total_tracks INTEGER,
    popularity_score DECIMAL(5, 3),

    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE INDEX idx_albums_artist ON albums(artist_id);
CREATE INDEX idx_albums_release_year ON albums(release_year);
CREATE INDEX idx_albums_genre ON albums(primary_genre);

-- ============================================================================
-- 4. TRACKS (Depends on: albums, artists)
-- ============================================================================
CREATE TABLE tracks (
    track_id VARCHAR(20) PRIMARY KEY,
    album_id VARCHAR(20) NOT NULL,
    artist_id VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    track_number INTEGER,
    duration_ms INTEGER,
    explicit BOOLEAN DEFAULT FALSE,
    release_date DATE,
    isrc VARCHAR(50),
    popularity_score DECIMAL(5, 3),

    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE INDEX idx_tracks_album ON tracks(album_id);
CREATE INDEX idx_tracks_artist ON tracks(artist_id);
CREATE INDEX idx_tracks_popularity ON tracks(popularity_score);
CREATE INDEX idx_tracks_release_date ON tracks(release_date);

-- ============================================================================
-- 5. TRACK FEATURES (Depends on: tracks) - 1:1 relationship
-- ============================================================================
CREATE TABLE track_features (
    track_id VARCHAR(20) PRIMARY KEY,
    tempo_bpm INTEGER,
    energy DECIMAL(5, 3),
    danceability DECIMAL(5, 3),
    valence DECIMAL(5, 3),
    acousticness DECIMAL(5, 3),
    loudness_db DECIMAL(6, 2),
    instrumentalness DECIMAL(5, 3),
    speechiness DECIMAL(5, 3),
    liveness DECIMAL(5, 3),
    key INTEGER,
    mode INTEGER,
    time_signature INTEGER,

    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
);

CREATE INDEX idx_features_tempo ON track_features(tempo_bpm);
CREATE INDEX idx_features_energy ON track_features(energy);
CREATE INDEX idx_features_danceability ON track_features(danceability);

-- ============================================================================
-- 6. COLLABORATIONS (Depends on: tracks, artists)
-- ============================================================================
CREATE TABLE collaborations (
    collab_id VARCHAR(20) PRIMARY KEY,
    track_id VARCHAR(20) NOT NULL,
    primary_artist_id VARCHAR(20) NOT NULL,
    featured_artist_id VARCHAR(20) NOT NULL,
    collab_type VARCHAR(50),

    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    FOREIGN KEY (primary_artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (featured_artist_id) REFERENCES artists(artist_id)
);

CREATE INDEX idx_collabs_track ON collaborations(track_id);
CREATE INDEX idx_collabs_primary ON collaborations(primary_artist_id);
CREATE INDEX idx_collabs_featured ON collaborations(featured_artist_id);

-- ============================================================================
-- 7. STREAMS (Depends on: tracks, artists)
-- ============================================================================
CREATE TABLE streams (
    stream_id VARCHAR(20) PRIMARY KEY,
    track_id VARCHAR(20) NOT NULL,
    artist_id VARCHAR(20) NOT NULL,
    region VARCHAR(10),
    platform VARCHAR(50),
    stream_date DATE,
    stream_count INTEGER,
    skip_rate DECIMAL(5, 3),
    completion_rate DECIMAL(5, 3),

    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE INDEX idx_streams_track ON streams(track_id);
CREATE INDEX idx_streams_artist ON streams(artist_id);
CREATE INDEX idx_streams_date ON streams(stream_date);
CREATE INDEX idx_streams_platform ON streams(platform);
CREATE INDEX idx_streams_region ON streams(region);

-- ============================================================================
-- 8. ROYALTIES (Depends on: tracks, artists, labels)
-- ============================================================================
CREATE TABLE royalties (
    royalty_id VARCHAR(20) PRIMARY KEY,
    track_id VARCHAR(20) NOT NULL,
    artist_id VARCHAR(20) NOT NULL,
    label_id VARCHAR(20) NOT NULL,
    quarter VARCHAR(20),
    streams_credited BIGINT,
    rate_per_stream DECIMAL(10, 5),
    gross_revenue_usd DECIMAL(15, 2),
    label_cut_usd DECIMAL(15, 2),
    artist_payout_usd DECIMAL(15, 2),

    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (label_id) REFERENCES record_labels(label_id)
);

CREATE INDEX idx_royalties_track ON royalties(track_id);
CREATE INDEX idx_royalties_artist ON royalties(artist_id);
CREATE INDEX idx_royalties_label ON royalties(label_id);
CREATE INDEX idx_royalties_quarter ON royalties(quarter);

-- ============================================================================
-- 9. PLAYLISTS (Depends on: tracks)
-- ============================================================================
CREATE TABLE playlists (
    playlist_entry_id VARCHAR(20) PRIMARY KEY,
    user_id VARCHAR(20),
    playlist_name VARCHAR(500),
    track_id VARCHAR(20) NOT NULL,
    platform VARCHAR(50),
    added_date DATE,
    position INTEGER,
    is_public BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
);

CREATE INDEX idx_playlists_track ON playlists(track_id);
CREATE INDEX idx_playlists_user ON playlists(user_id);
CREATE INDEX idx_playlists_platform ON playlists(platform);

-- ============================================================================
-- 10. AWARDS (Depends on: artists, tracks - optional track)
-- ============================================================================
CREATE TABLE awards (
    award_id VARCHAR(20) PRIMARY KEY,
    artist_id VARCHAR(20) NOT NULL,
    track_id VARCHAR(20),
    award_name VARCHAR(255),
    category VARCHAR(255),
    year INTEGER,
    won BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE SET NULL
);

CREATE INDEX idx_awards_artist ON awards(artist_id);
CREATE INDEX idx_awards_track ON awards(track_id);
CREATE INDEX idx_awards_year ON awards(year);

-- ============================================================================
-- 11. CHARTS (Depends on: tracks, artists)
-- ============================================================================
CREATE TABLE charts (
    chart_id VARCHAR(20) PRIMARY KEY,
    track_id VARCHAR(20) NOT NULL,
    artist_id VARCHAR(20) NOT NULL,
    chart_name VARCHAR(255),
    week_date DATE,
    peak_position INTEGER,
    current_position INTEGER,
    weeks_on_chart INTEGER,
    movement INTEGER,

    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE INDEX idx_charts_track ON charts(track_id);
CREATE INDEX idx_charts_artist ON charts(artist_id);
CREATE INDEX idx_charts_date ON charts(week_date);
CREATE INDEX idx_charts_name ON charts(chart_name);

-- ============================================================================
-- SUMMARY STATISTICS VIEW
-- ============================================================================
CREATE OR REPLACE VIEW summary_stats AS
SELECT
    'record_labels' AS table_name, COUNT(*) AS row_count FROM record_labels
UNION ALL
SELECT 'artists', COUNT(*) FROM artists
UNION ALL
SELECT 'albums', COUNT(*) FROM albums
UNION ALL
SELECT 'tracks', COUNT(*) FROM tracks
UNION ALL
SELECT 'track_features', COUNT(*) FROM track_features
UNION ALL
SELECT 'collaborations', COUNT(*) FROM collaborations
UNION ALL
SELECT 'streams', COUNT(*) FROM streams
UNION ALL
SELECT 'royalties', COUNT(*) FROM royalties
UNION ALL
SELECT 'playlists', COUNT(*) FROM playlists
UNION ALL
SELECT 'awards', COUNT(*) FROM awards
UNION ALL
SELECT 'charts', COUNT(*) FROM charts
ORDER BY row_count DESC;

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE '✓ Schema created successfully!';
    RAISE NOTICE '✓ All tables, indexes, and foreign keys created';
    RAISE NOTICE '✓ Ready to import CSV data';
END $$;
