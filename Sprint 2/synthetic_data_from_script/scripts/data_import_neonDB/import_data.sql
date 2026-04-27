-- ============================================================================
-- CSV Import Script for NeonDB
-- ============================================================================
-- This script imports all CSV files into the database
-- Run this AFTER creating the schema with create_schema.sql

-- Import in order of dependencies (no foreign key violations)

-- 1. Record Labels (no dependencies)
\COPY record_labels FROM 'record_labels.csv' WITH (FORMAT csv, HEADER true);

-- 2. Artists (depends on labels)
\COPY artists FROM 'artists.csv' WITH (FORMAT csv, HEADER true);

-- 3. Albums (depends on artists)
\COPY albums FROM 'albums.csv' WITH (FORMAT csv, HEADER true);

-- 4. Tracks (depends on albums, artists)
\COPY tracks FROM 'tracks.csv' WITH (FORMAT csv, HEADER true);

-- 5. Track Features (depends on tracks)
\COPY track_features FROM 'track_features.csv' WITH (FORMAT csv, HEADER true);

-- 6. Collaborations (depends on tracks, artists)
\COPY collaborations FROM 'collaborations.csv' WITH (FORMAT csv, HEADER true);

-- 7. Streams (depends on tracks, artists)
\COPY streams FROM 'streams.csv' WITH (FORMAT csv, HEADER true);

-- 8. Royalties (depends on tracks, artists, labels)
\COPY royalties FROM 'royalties.csv' WITH (FORMAT csv, HEADER true);

-- 9. Playlists (depends on tracks)
\COPY playlists FROM 'playlists.csv' WITH (FORMAT csv, HEADER true);

-- 10. Awards (depends on artists, tracks)
\COPY awards FROM 'awards.csv' WITH (FORMAT csv, HEADER true);

-- 11. Charts (depends on tracks, artists)
\COPY charts FROM 'charts.csv' WITH (FORMAT csv, HEADER true);

-- Verify import
SELECT * FROM summary_stats;

-- Show success message
DO $$
BEGIN
    RAISE NOTICE '✓ All CSV files imported successfully!';
END $$;
