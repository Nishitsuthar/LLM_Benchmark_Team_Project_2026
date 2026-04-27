import pandas as pd
from faker import Faker
import random

fake = Faker()

# Configuration
NUM_LABELS = 5
NUM_ARTISTS = 20
NUM_ALBUMS = 50

# 1. Generate Record Labels
labels_data = []
for i in range(1, NUM_LABELS + 1):
    labels_data.append({
        'label_id': f'LBL_{i}',
        'name': fake.company() + " Records",
        'country': fake.country(),
        'founding_year': random.randint(1950, 2015),
        'royalty_rate_per_stream': round(random.uniform(0.003, 0.008), 5)
    })
df_labels = pd.DataFrame(labels_data)

# 2. Generate Artists
artists_data = []
genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Electronic', 'Country']
for i in range(1, NUM_ARTISTS + 1):
    artists_data.append({
        'artist_id': f'ART_{i}',
        'name': fake.name(),
        'country': fake.country(),
        'primary_genre': random.choice(genres),
        'debut_year': random.randint(1990, 2023),
        'label_id': random.choice(labels_data)['label_id']
    })
df_artists = pd.DataFrame(artists_data)

# 3. Generate Albums
albums_data = []
for i in range(1, NUM_ALBUMS + 1):
    artist = random.choice(artists_data)
    albums_data.append({
        'album_id': f'ALB_{i}',
        'artist_id': artist['artist_id'],
        # Using catch_phrase for indie-sounding album titles
        'title': fake.catch_phrase().title(), 
        'release_year': random.randint(artist['debut_year'], 2024),
        'genre': artist['primary_genre'],
        'total_tracks': random.randint(7, 15)
    })
df_albums = pd.DataFrame(albums_data)

# Export to CSV to act as your "Ground Truth" SQL database
df_labels.to_csv('record_labels.csv', index=False)
df_artists.to_csv('artists.csv', index=False)
df_albums.to_csv('albums.csv', index=False)

print("Base tabular data generated successfully!")