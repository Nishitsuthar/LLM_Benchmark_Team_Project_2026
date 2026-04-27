import pandas as pd
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

# --- 1. SET YOUR TARGET VOLUMES HERE ---
NUM_LABELS = 50
NUM_ARTISTS = 700
NUM_ALBUMS = 1500
NUM_TRACKS = 6000
NUM_STREAMS = 10000
NUM_PLAYLIST_ENTRIES = 3000
NUM_COLLABS = 800
NUM_ROYALTIES = 2000
NUM_AWARDS = 500
NUM_CHART_ENTRIES = 2000

print("Generating Base Entities (Labels, Artists, Albums, Tracks)...")

# --- 2. GENERATE RECORD LABELS ---
labels_data = []
for i in range(1, NUM_LABELS + 1):
    labels_data.append({
        'label_id': f'LBL_{i}',
        'name': fake.company() + " Records",
        'country': fake.country(),
        'founding_year': random.randint(1950, 2020),
        'royalty_rate_per_stream': round(random.uniform(0.003, 0.008), 5)
    })

# --- 3. GENERATE ARTISTS ---
artists_data = []
genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Electronic', 'Country', 'Classical', 'R&B']
for i in range(1, NUM_ARTISTS + 1):
    artists_data.append({
        'artist_id': f'ART_{i}',
        'name': fake.name(),
        'country': fake.country(),
        'primary_genre': random.choice(genres),
        'debut_year': random.randint(1990, 2023),
        'label_id': random.choice(labels_data)['label_id']
    })

# --- 4. GENERATE ALBUMS ---
albums_data = []
for i in range(1, NUM_ALBUMS + 1):
    artist = random.choice(artists_data)
    albums_data.append({
        'album_id': f'ALB_{i}',
        'artist_id': artist['artist_id'],
        'title': fake.catch_phrase().title(),
        'release_year': random.randint(artist['debut_year'], 2024),
        'genre': artist['primary_genre'],
        'total_tracks': random.randint(5, 18)
    })

# --- 5. GENERATE TRACKS ---
tracks_data = []
for i in range(1, NUM_TRACKS + 1):
    album = random.choice(albums_data)
    tracks_data.append({
        'track_id': f'TRK_{i}',
        'album_id': album['album_id'],
        'artist_id': album['artist_id'], 
        'title': fake.sentence(nb_words=3).replace('.', ''),
        'duration_ms': random.randint(120000, 360000), 
        'explicit': random.choice([True, False])
    })

print("Generating Secondary Entities (Features, Streams, Royalties, etc.)...")

# --- LOOKUP DICTIONARIES (For fast relational linking) ---
track_artist_map = {t['track_id']: t['artist_id'] for t in tracks_data}
artist_label_map = {a['artist_id']: a['label_id'] for a in artists_data}
label_rate_map = {l['label_id']: l['royalty_rate_per_stream'] for l in labels_data}
platforms = ['Spotify', 'Apple Music', 'Tidal', 'Amazon Music', 'YouTube Music']

# --- 6. GENERATE TRACK FEATURES (1-to-1 with Tracks) ---
track_features_data = []
for track in tracks_data:
    track_features_data.append({
        'track_id': track['track_id'],
        'tempo_bpm': random.randint(60, 180),
        'energy': round(random.uniform(0.1, 1.0), 3),
        'danceability': round(random.uniform(0.1, 1.0), 3),
        'valence': round(random.uniform(0.1, 1.0), 3),
        'acousticness': round(random.uniform(0.0, 1.0), 3),
        'loudness_db': round(random.uniform(-20.0, 0.0), 2),
        'instrumentalness': round(random.uniform(0.0, 0.9), 3)
    })

# --- 7. GENERATE COLLABORATIONS ---
collabs_data = []
for i in range(1, NUM_COLLABS + 1):
    track = random.choice(tracks_data)
    # Pick a featured artist who isn't the primary artist
    feat_artist = random.choice([a for a in artists_data if a['artist_id'] != track['artist_id']])
    collabs_data.append({
        'collab_id': f'COL_{i}',
        'track_id': track['track_id'],
        'primary_artist_id': track['artist_id'],
        'featured_artist_id': feat_artist['artist_id']
    })

# --- 8. GENERATE STREAMS ---
streams_data = []
for i in range(1, NUM_STREAMS + 1):
    track = random.choice(tracks_data)
    streams_data.append({
        'stream_id': f'STR_{i}',
        'track_id': track['track_id'],
        'artist_id': track['artist_id'],
        'region': fake.country_code(),
        'platform': random.choice(platforms),
        'stream_date': fake.date_between(start_date='-2y', end_date='today'),
        'stream_count': random.randint(100, 50000)
    })

# --- 9. GENERATE ROYALTIES ---
royalties_data = []
quarters = ['Q1-2023', 'Q2-2023', 'Q3-2023', 'Q4-2023', 'Q1-2024']
for i in range(1, NUM_ROYALTIES + 1):
    track = random.choice(tracks_data)
    artist_id = track['artist_id']
    label_id = artist_label_map[artist_id]
    rate = label_rate_map[label_id]
    streams = random.randint(50000, 1000000)
    
    royalties_data.append({
        'royalty_id': f'ROY_{i}',
        'track_id': track['track_id'],
        'artist_id': artist_id,
        'label_id': label_id,
        'quarter': random.choice(quarters),
        'streams_credited': streams,
        'rate_per_stream': rate,
        'total_payout_usd': round(streams * rate, 2)
    })

# --- 10. GENERATE PLAYLISTS ---
playlists_data = []
for i in range(1, NUM_PLAYLIST_ENTRIES + 1):
    playlists_data.append({
        'playlist_entry_id': f'PLE_{i}',
        'user_id': f'USR_{random.randint(1, 500)}',
        'playlist_name': fake.word().title() + " Vibes",
        'track_id': random.choice(tracks_data)['track_id'],
        'platform': random.choice(platforms),
        'added_date': fake.date_between(start_date='-1y', end_date='today')
    })

# --- 11. GENERATE AWARDS ---
awards_data = []
award_names = ['Global Music Award', 'Sound & Vision Prize', 'Golden Mic', 'Streaming Record Award']
categories = ['Song of the Year', 'Best New Artist', 'Best Album', 'Top Producer']
for i in range(1, NUM_AWARDS + 1):
    awards_data.append({
        'award_id': f'AWD_{i}',
        'artist_id': random.choice(artists_data)['artist_id'],
        'award_name': random.choice(award_names),
        'category': random.choice(categories),
        'year': random.randint(2010, 2024)
    })

# --- 12. GENERATE CHARTS ---
charts_data = []
chart_names = ['Top 100 Global', 'Viral 50', 'Indie Spotlight', 'Weekend Anthems']
for i in range(1, NUM_CHART_ENTRIES + 1):
    track = random.choice(tracks_data)
    charts_data.append({
        'chart_id': f'CHT_{i}',
        'track_id': track['track_id'],
        'artist_id': track['artist_id'],
        'chart_name': random.choice(chart_names),
        'week_date': fake.date_between(start_date='-1y', end_date='today'),
        'peak_position': random.randint(1, 100),
        'weeks_on_chart': random.randint(1, 52)
    })

print("Exporting all 11 files to CSV...")

# --- 13. EXPORT TO CSV ---
pd.DataFrame(labels_data).to_csv('record_labels.csv', index=False)
pd.DataFrame(artists_data).to_csv('artists.csv', index=False)
pd.DataFrame(albums_data).to_csv('albums.csv', index=False)
pd.DataFrame(tracks_data).to_csv('tracks.csv', index=False)
pd.DataFrame(track_features_data).to_csv('track_features.csv', index=False)
pd.DataFrame(collabs_data).to_csv('collaborations.csv', index=False)
pd.DataFrame(streams_data).to_csv('streams.csv', index=False)
pd.DataFrame(royalties_data).to_csv('royalties.csv', index=False)
pd.DataFrame(playlists_data).to_csv('playlists.csv', index=False)
pd.DataFrame(awards_data).to_csv('awards.csv', index=False)
pd.DataFrame(charts_data).to_csv('charts.csv', index=False)

print("Success! All synthetic data generated successfully.")