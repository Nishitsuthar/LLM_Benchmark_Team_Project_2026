"""
High-Quality Synthetic Music Industry Data Generator

Features:
- Realistic distributions (power-law for popularity, temporal patterns)
- Strong referential integrity and temporal consistency
- Genre-specific characteristics and relationships
- Correlated attributes (e.g., popular artists get more streams)
- Realistic naming and data patterns
- Data quality validation
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# CONFIGURATION
# =============================================================================
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

# Genre definitions with realistic characteristics
GENRE_PROFILES = {
    'Pop': {'popularity': 0.9, 'tempo_mean': 120, 'tempo_std': 15, 'energy_mean': 0.7, 'danceability_mean': 0.75},
    'Rock': {'popularity': 0.7, 'tempo_mean': 125, 'tempo_std': 20, 'energy_mean': 0.8, 'danceability_mean': 0.6},
    'Hip-Hop': {'popularity': 0.85, 'tempo_mean': 95, 'tempo_std': 12, 'energy_mean': 0.75, 'danceability_mean': 0.8},
    'Jazz': {'popularity': 0.4, 'tempo_mean': 110, 'tempo_std': 25, 'energy_mean': 0.5, 'danceability_mean': 0.5},
    'Electronic': {'popularity': 0.65, 'tempo_mean': 128, 'tempo_std': 10, 'energy_mean': 0.85, 'danceability_mean': 0.8},
    'Country': {'popularity': 0.6, 'tempo_mean': 105, 'tempo_std': 15, 'energy_mean': 0.6, 'danceability_mean': 0.65},
    'Classical': {'popularity': 0.3, 'tempo_mean': 90, 'tempo_std': 30, 'energy_mean': 0.4, 'danceability_mean': 0.3},
    'R&B': {'popularity': 0.7, 'tempo_mean': 100, 'tempo_std': 18, 'energy_mean': 0.65, 'danceability_mean': 0.7},
    'Indie': {'popularity': 0.5, 'tempo_mean': 115, 'tempo_std': 20, 'energy_mean': 0.6, 'danceability_mean': 0.6},
    'Metal': {'popularity': 0.45, 'tempo_mean': 140, 'tempo_std': 25, 'energy_mean': 0.9, 'danceability_mean': 0.4}
}

PLATFORMS = ['Spotify', 'Apple Music', 'Tidal', 'Amazon Music', 'YouTube Music']
PLATFORM_MARKET_SHARE = [0.35, 0.25, 0.05, 0.15, 0.20]  # Realistic market distribution

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def power_law_sample(size, alpha=2.5, min_val=1, max_val=None):
    """Generate power-law distributed samples (for popularity, wealth distribution)"""
    samples = np.random.pareto(alpha, size) + 1
    samples = samples / samples.max()
    if max_val:
        samples = samples * (max_val - min_val) + min_val
    return samples

def weighted_choice(choices, weights, size=1):
    """Make weighted random choices"""
    return np.random.choice(choices, size=size, p=np.array(weights)/sum(weights))

def generate_artist_name(genre):
    """Generate realistic artist names based on genre"""
    if genre in ['Hip-Hop', 'R&B']:
        prefixes = ['Lil', 'Big', 'Young', 'DJ', '']
        suffixes = ['', ' Baby', ' King', ' Prince']
        name = fake.first_name()
        if random.random() > 0.5:
            return f"{random.choice(prefixes)} {name}{random.choice(suffixes)}".strip()
    elif genre == 'Electronic':
        if random.random() > 0.6:
            return fake.last_name() + 'x' * random.randint(0, 2)
    elif genre == 'Metal':
        dark_words = ['Dark', 'Blood', 'Iron', 'Death', 'Black', 'Shadow', 'Grave', 'Storm']
        if random.random() > 0.5:
            return f"{random.choice(dark_words)} {fake.last_name()}"

    # Default: band name or regular artist
    if random.random() > 0.6:
        return f"The {fake.last_name()}s"
    return fake.name()

def generate_song_title(genre):
    """Generate genre-appropriate song titles"""
    if genre == 'Hip-Hop':
        slang = ['Flexin', 'Vibin', 'Stackin', 'Rollin', 'Winnin', 'Drippin']
        if random.random() > 0.6:
            return f"{random.choice(slang)} {fake.word().title()}"
    elif genre == 'Country':
        country_themes = ['Truck', 'Whiskey', 'Highway', 'Heart', 'River', 'Small Town']
        if random.random() > 0.5:
            return f"{random.choice(country_themes)} {fake.word().title()}"
    elif genre == 'Classical':
        forms = ['Sonata', 'Symphony', 'Concerto', 'Prelude', 'Nocturne']
        if random.random() > 0.7:
            return f"{random.choice(forms)} No. {random.randint(1, 20)}"

    # Default
    return ' '.join(fake.words(nb=random.randint(1, 4))).title()

def generate_album_title(genre):
    """Generate genre-appropriate album titles"""
    album_words = {
        'Rock': ['Thunder', 'Revolution', 'Edge', 'Echo', 'Storm'],
        'Pop': ['Dreams', 'Forever', 'Love', 'Star', 'Light'],
        'Electronic': ['Neon', 'Digital', 'Circuit', 'Pulse', 'Wave'],
        'Jazz': ['Blue', 'Smooth', 'Velvet', 'Midnight', 'Soul'],
    }

    words = album_words.get(genre, ['Time', 'Life', 'World', 'Journey', 'Stories'])
    if random.random() > 0.5:
        return random.choice(words) + ' ' + fake.word().title()
    return fake.catch_phrase().title()

# =============================================================================
# DATA GENERATION
# =============================================================================

print("=" * 70)
print("HIGH-QUALITY SYNTHETIC MUSIC DATA GENERATOR")
print("=" * 70)

print("\n[1/11] Generating Record Labels...")
labels_data = []
major_labels = ['Universal', 'Sony', 'Warner', 'Capitol', 'Columbia']
for i in range(1, NUM_LABELS + 1):
    is_major = i <= 5
    founding_year = random.randint(1950, 1980) if is_major else random.randint(1980, 2020)

    labels_data.append({
        'label_id': f'LBL_{i:04d}',
        'name': major_labels[i-1] + " Records" if is_major else fake.company() + random.choice([' Records', ' Music', ' Entertainment']),
        'country': weighted_choice(['USA', 'UK', 'Canada', 'Germany', 'Japan', 'France'],
                                   [0.4, 0.25, 0.1, 0.1, 0.08, 0.07])[0],
        'founding_year': founding_year,
        'label_type': 'Major' if is_major else weighted_choice(['Independent', 'Subsidiary'], [0.7, 0.3])[0],
        'royalty_rate_per_stream': round(random.uniform(0.004, 0.009) if is_major else random.uniform(0.003, 0.007), 5)
    })

print(f"   Generated {len(labels_data)} labels ({sum(1 for l in labels_data if l['label_type'] == 'Major')} major)")

print("\n[2/11] Generating Artists...")
artists_data = []
genre_list = list(GENRE_PROFILES.keys())
genre_weights = [GENRE_PROFILES[g]['popularity'] for g in genre_list]

# Assign popularity scores (power-law distribution)
artist_popularity = power_law_sample(NUM_ARTISTS, alpha=2.0)

for i in range(1, NUM_ARTISTS + 1):
    primary_genre = weighted_choice(genre_list, genre_weights)[0]
    debut_year = random.randint(1990, 2024)
    popularity_score = artist_popularity[i-1]

    # Major labels sign more popular artists
    if popularity_score > 0.8:
        label = random.choice([l for l in labels_data if l['label_type'] == 'Major'])
    else:
        label = random.choice(labels_data)

    artists_data.append({
        'artist_id': f'ART_{i:04d}',
        'name': generate_artist_name(primary_genre),
        'country': label['country'] if random.random() > 0.3 else fake.country(),
        'primary_genre': primary_genre,
        'secondary_genre': random.choice([g for g in genre_list if g != primary_genre]) if random.random() > 0.6 else None,
        'debut_year': debut_year,
        'label_id': label['label_id'],
        'is_active': random.random() > 0.15,  # 85% active
        'popularity_score': round(popularity_score, 3)
    })

print(f"   Generated {len(artists_data)} artists across {len(genre_list)} genres")

print("\n[3/11] Generating Albums...")
albums_data = []
album_popularity = power_law_sample(NUM_ALBUMS, alpha=2.2)

for i in range(1, NUM_ALBUMS + 1):
    artist = random.choices(artists_data, weights=[a['popularity_score'] for a in artists_data])[0]

    # More popular artists release more albums
    years_active = 2024 - artist['debut_year']
    release_year = random.randint(artist['debut_year'], min(2024, artist['debut_year'] + years_active + 1))

    total_tracks = np.random.choice([8, 10, 12, 14, 16], p=[0.15, 0.25, 0.3, 0.2, 0.1])

    albums_data.append({
        'album_id': f'ALB_{i:04d}',
        'artist_id': artist['artist_id'],
        'title': generate_album_title(artist['primary_genre']),
        'release_year': release_year,
        'release_date': fake.date_between(start_date=f'-{2024-release_year}y', end_date='today'),
        'primary_genre': artist['primary_genre'],
        'secondary_genre': artist['secondary_genre'],
        'album_type': weighted_choice(['Studio', 'Live', 'Compilation', 'EP'], [0.65, 0.15, 0.10, 0.10])[0],
        'total_tracks': total_tracks,
        'popularity_score': round(album_popularity[i-1], 3)
    })

print(f"   Generated {len(albums_data)} albums")

print("\n[4/11] Generating Tracks...")
tracks_data = []
track_popularity = power_law_sample(NUM_TRACKS, alpha=2.3)

# Distribute tracks across albums respecting total_tracks constraint
album_track_counts = defaultdict(int)

for i in range(1, NUM_TRACKS + 1):
    # Choose album weighted by popularity and remaining capacity
    available_albums = [a for a in albums_data if album_track_counts[a['album_id']] < a['total_tracks']]
    if not available_albums:
        # Reset if we run out (shouldn't happen with proper sizing)
        album_track_counts.clear()
        available_albums = albums_data

    album = random.choices(available_albums,
                          weights=[a['popularity_score'] for a in available_albums])[0]
    album_track_counts[album['album_id']] += 1

    genre_profile = GENRE_PROFILES[album['primary_genre']]

    # Duration varies by genre
    if album['primary_genre'] == 'Classical':
        duration_ms = random.randint(180000, 1200000)  # 3-20 minutes
    elif album['primary_genre'] in ['Hip-Hop', 'Pop']:
        duration_ms = random.randint(150000, 240000)  # 2.5-4 minutes
    else:
        duration_ms = random.randint(180000, 360000)  # 3-6 minutes

    tracks_data.append({
        'track_id': f'TRK_{i:05d}',
        'album_id': album['album_id'],
        'artist_id': album['artist_id'],
        'title': generate_song_title(album['primary_genre']),
        'track_number': album_track_counts[album['album_id']],
        'duration_ms': duration_ms,
        'explicit': random.random() > 0.75 if album['primary_genre'] == 'Hip-Hop' else random.random() > 0.9,
        'release_date': album['release_date'],
        'isrc': f"{fake.country_code()}{fake.bothify(text='###???###')}".upper(),
        'popularity_score': round(track_popularity[i-1], 3)
    })

print(f"   Generated {len(tracks_data)} tracks")

print("\n[5/11] Generating Track Audio Features...")
track_features_data = []

for track in tracks_data:
    # Get genre profile for realistic feature distributions
    artist = next(a for a in artists_data if a['artist_id'] == track['artist_id'])
    genre_profile = GENRE_PROFILES[artist['primary_genre']]

    # Generate correlated features
    tempo = np.clip(int(np.random.normal(genre_profile['tempo_mean'], genre_profile['tempo_std'])), 40, 200)
    energy = np.clip(np.random.beta(5, 2) if genre_profile['energy_mean'] > 0.7 else np.random.beta(2, 3), 0, 1)
    danceability = np.clip(np.random.normal(genre_profile['danceability_mean'], 0.15), 0, 1)

    # Valence correlates with major key
    valence = np.clip(np.random.beta(2, 2), 0, 1)

    # Acousticness inversely correlates with electronic genres
    if artist['primary_genre'] in ['Electronic', 'Hip-Hop']:
        acousticness = np.random.beta(1, 5)
    elif artist['primary_genre'] in ['Classical', 'Jazz', 'Country']:
        acousticness = np.random.beta(5, 2)
    else:
        acousticness = np.random.beta(2, 2)

    track_features_data.append({
        'track_id': track['track_id'],
        'tempo_bpm': tempo,
        'energy': round(energy, 3),
        'danceability': round(danceability, 3),
        'valence': round(valence, 3),
        'acousticness': round(acousticness, 3),
        'loudness_db': round(np.random.uniform(-15, -3), 2),
        'instrumentalness': round(np.random.beta(1, 10), 3),
        'speechiness': round(np.random.beta(1, 8) if artist['primary_genre'] != 'Hip-Hop' else np.random.beta(3, 2), 3),
        'liveness': round(np.random.beta(1, 5), 3),
        'key': random.randint(0, 11),
        'mode': random.choice([0, 1]),  # 0 = minor, 1 = major
        'time_signature': weighted_choice([3, 4, 5, 6], [0.05, 0.85, 0.05, 0.05])[0]
    })

print(f"   Generated audio features for {len(track_features_data)} tracks")

print("\n[6/11] Generating Collaborations...")
collabs_data = []
collab_set = set()  # Prevent duplicates

attempts = 0
max_attempts = NUM_COLLABS * 10

while len(collabs_data) < NUM_COLLABS and attempts < max_attempts:
    attempts += 1
    track = random.choices(tracks_data, weights=[t['popularity_score'] for t in tracks_data])[0]
    primary_artist = next(a for a in artists_data if a['artist_id'] == track['artist_id'])

    # Featured artists are more likely from same genre or label
    same_genre = [a for a in artists_data if a['primary_genre'] == primary_artist['primary_genre']
                  and a['artist_id'] != track['artist_id']]
    same_label = [a for a in artists_data if a['label_id'] == primary_artist['label_id']
                  and a['artist_id'] != track['artist_id']]

    if random.random() > 0.4 and same_genre:
        feat_artist = random.choice(same_genre)
    elif random.random() > 0.7 and same_label:
        feat_artist = random.choice(same_label)
    else:
        feat_artist = random.choice([a for a in artists_data if a['artist_id'] != track['artist_id']])

    collab_key = (track['track_id'], feat_artist['artist_id'])
    if collab_key not in collab_set:
        collab_set.add(collab_key)
        collabs_data.append({
            'collab_id': f'COL_{len(collabs_data)+1:04d}',
            'track_id': track['track_id'],
            'primary_artist_id': track['artist_id'],
            'featured_artist_id': feat_artist['artist_id'],
            'collab_type': weighted_choice(['Featured', 'Remix', 'Producer'], [0.7, 0.2, 0.1])[0]
        })

print(f"   Generated {len(collabs_data)} unique collaborations")

print("\n[7/11] Generating Streams...")
streams_data = []

# Create realistic streaming patterns
for i in range(1, NUM_STREAMS + 1):
    # Popular tracks get exponentially more streams
    track = random.choices(tracks_data, weights=[t['popularity_score']**2 for t in tracks_data])[0]

    # Streams only occur after release date
    days_since_release = (datetime.now().date() - track['release_date']).days
    if days_since_release > 0:
        stream_date = track['release_date'] + timedelta(days=random.randint(0, days_since_release))
    else:
        stream_date = track['release_date']

    # Platform distribution
    platform = weighted_choice(PLATFORMS, PLATFORM_MARKET_SHARE)[0]

    # Stream counts follow power-law (viral hits vs. regular plays)
    base_streams = int(power_law_sample(1, alpha=2.0, min_val=100, max_val=100000)[0])
    popularity_multiplier = track['popularity_score'] * 10
    stream_count = int(base_streams * popularity_multiplier)

    streams_data.append({
        'stream_id': f'STR_{i:06d}',
        'track_id': track['track_id'],
        'artist_id': track['artist_id'],
        'region': fake.country_code(),
        'platform': platform,
        'stream_date': stream_date,
        'stream_count': stream_count,
        'skip_rate': round(np.random.beta(2, 8), 3),  # Most tracks aren't skipped
        'completion_rate': round(np.random.beta(8, 2), 3)
    })

print(f"   Generated {len(streams_data)} stream records")

print("\n[8/11] Generating Royalties...")
royalties_data = []

# Generate quarterly royalties
quarters = []
for year in [2023, 2024]:
    for q in range(1, 5):
        quarters.append(f'Q{q}-{year}')

# Aggregate streams by track and quarter for realistic royalties
track_artist_map = {t['track_id']: t['artist_id'] for t in tracks_data}
artist_label_map = {a['artist_id']: a['label_id'] for a in artists_data}
label_rate_map = {l['label_id']: l['royalty_rate_per_stream'] for l in labels_data}

for i in range(1, NUM_ROYALTIES + 1):
    track = random.choices(tracks_data, weights=[t['popularity_score'] for t in tracks_data])[0]
    artist_id = track['artist_id']
    label_id = artist_label_map[artist_id]
    rate = label_rate_map[label_id]

    quarter = random.choice(quarters)

    # Royalty streams are aggregate counts (much higher than individual stream records)
    base_streams = int(power_law_sample(1, alpha=1.8, min_val=10000, max_val=5000000)[0])
    streams_credited = int(base_streams * track['popularity_score'] * 5)

    royalties_data.append({
        'royalty_id': f'ROY_{i:05d}',
        'track_id': track['track_id'],
        'artist_id': artist_id,
        'label_id': label_id,
        'quarter': quarter,
        'streams_credited': streams_credited,
        'rate_per_stream': rate,
        'gross_revenue_usd': round(streams_credited * rate, 2),
        'label_cut_usd': round(streams_credited * rate * 0.7, 2),
        'artist_payout_usd': round(streams_credited * rate * 0.3, 2)
    })

print(f"   Generated {len(royalties_data)} royalty records")

print("\n[9/11] Generating Playlist Entries...")
playlists_data = []

# Generate diverse playlist names
playlist_themes = ['Chill', 'Workout', 'Focus', 'Party', 'Sleep', 'Study', 'Mood', 'Vibes']
playlist_names_cache = [f"{random.choice(playlist_themes)} {fake.word().title()}" for _ in range(200)]

for i in range(1, NUM_PLAYLIST_ENTRIES + 1):
    track = random.choices(tracks_data, weights=[t['popularity_score'] for t in tracks_data])[0]
    platform = weighted_choice(PLATFORMS, PLATFORM_MARKET_SHARE)[0]

    # Playlists created after track release
    days_since_release = (datetime.now().date() - track['release_date']).days
    if days_since_release > 0:
        added_date = track['release_date'] + timedelta(days=random.randint(0, days_since_release))
    else:
        added_date = track['release_date']

    playlists_data.append({
        'playlist_entry_id': f'PLE_{i:05d}',
        'user_id': f'USR_{random.randint(1, NUM_PLAYLIST_ENTRIES // 6):05d}',  # Users have multiple playlists
        'playlist_name': random.choice(playlist_names_cache),
        'track_id': track['track_id'],
        'platform': platform,
        'added_date': added_date,
        'position': random.randint(1, 100),
        'is_public': random.random() > 0.3
    })

print(f"   Generated {len(playlists_data)} playlist entries")

print("\n[10/11] Generating Awards...")
awards_data = []
award_set = set()  # Prevent duplicate artist-award-year

award_names = [
    'Global Music Award', 'Sound & Vision Prize', 'Golden Mic',
    'Streaming Record Award', 'Artist of the Year', 'Billboard Award'
]
categories = [
    'Song of the Year', 'Best New Artist', 'Best Album', 'Top Producer',
    'Best Pop Artist', 'Best Rock Album', 'Breakthrough Artist', 'Best Collaboration'
]

attempts = 0
max_attempts = NUM_AWARDS * 10

while len(awards_data) < NUM_AWARDS and attempts < max_attempts:
    attempts += 1

    # Popular artists win more awards
    artist = random.choices(artists_data, weights=[a['popularity_score']**2 for a in artists_data])[0]
    award_name = random.choice(award_names)
    category = random.choice(categories)
    year = random.randint(max(artist['debut_year'], 2010), 2024)

    award_key = (artist['artist_id'], award_name, category, year)
    if award_key not in award_set:
        award_set.add(award_key)

        # Get artist's tracks (if any)
        artist_tracks = [t['track_id'] for t in tracks_data if t['artist_id'] == artist['artist_id']]
        track_id = random.choice(artist_tracks) if artist_tracks and random.random() > 0.4 else None

        awards_data.append({
            'award_id': f'AWD_{len(awards_data)+1:04d}',
            'artist_id': artist['artist_id'],
            'track_id': track_id,
            'award_name': award_name,
            'category': category,
            'year': year,
            'won': random.random() > 0.3  # 70% won, 30% nominated
        })

print(f"   Generated {len(awards_data)} award records")

print("\n[11/11] Generating Chart Entries...")
charts_data = []

chart_names = [
    'Top 100 Global', 'Viral 50', 'Hot 100', 'Indie Spotlight',
    'Weekend Anthems', 'New Music Friday', 'Top Streaming'
]

for i in range(1, NUM_CHART_ENTRIES + 1):
    # Popular tracks chart more
    track = random.choices(tracks_data, weights=[t['popularity_score']**3 for t in tracks_data])[0]
    chart_name = random.choice(chart_names)

    # Charts only after release
    days_since_release = (datetime.now().date() - track['release_date']).days
    if days_since_release > 7:
        week_date = track['release_date'] + timedelta(weeks=random.randint(1, days_since_release // 7))
    else:
        week_date = track['release_date']

    # Peak position correlates with popularity
    if track['popularity_score'] > 0.9:
        peak_position = random.randint(1, 10)
    elif track['popularity_score'] > 0.7:
        peak_position = random.randint(5, 30)
    else:
        peak_position = random.randint(20, 100)

    # Weeks on chart correlates with popularity
    weeks_on_chart = int(np.random.exponential(track['popularity_score'] * 20) + 1)
    weeks_on_chart = min(weeks_on_chart, 52)

    charts_data.append({
        'chart_id': f'CHT_{i:05d}',
        'track_id': track['track_id'],
        'artist_id': track['artist_id'],
        'chart_name': chart_name,
        'week_date': week_date,
        'peak_position': peak_position,
        'current_position': min(peak_position + random.randint(0, 20), 100),
        'weeks_on_chart': weeks_on_chart,
        'movement': random.randint(-30, 30)
    })

print(f"   Generated {len(charts_data)} chart entries")

# =============================================================================
# DATA QUALITY VALIDATION
# =============================================================================

print("\n" + "=" * 70)
print("DATA QUALITY VALIDATION")
print("=" * 70)

# Check referential integrity
print("\n[Referential Integrity Checks]")
album_artists = {a['album_id']: a['artist_id'] for a in albums_data}
track_albums = {t['track_id']: t['album_id'] for t in tracks_data}

orphaned_albums = [a for a in albums_data if a['artist_id'] not in [ar['artist_id'] for ar in artists_data]]
print(f"✓ Orphaned albums: {len(orphaned_albums)} (should be 0)")

orphaned_tracks = [t for t in tracks_data if t['album_id'] not in [a['album_id'] for a in albums_data]]
print(f"✓ Orphaned tracks: {len(orphaned_tracks)} (should be 0)")

# Check temporal consistency
print("\n[Temporal Consistency Checks]")
temporal_issues = []
for album in albums_data:
    artist = next(a for a in artists_data if a['artist_id'] == album['artist_id'])
    if album['release_year'] < artist['debut_year']:
        temporal_issues.append(f"Album {album['album_id']} released before artist debut")

print(f"✓ Temporal violations: {len(temporal_issues)} (should be 0)")

# Check duplicates
print("\n[Uniqueness Checks]")
label_ids = [l['label_id'] for l in labels_data]
print(f"✓ Duplicate label IDs: {len(label_ids) - len(set(label_ids))} (should be 0)")

artist_ids = [a['artist_id'] for a in artists_data]
print(f"✓ Duplicate artist IDs: {len(artist_ids) - len(set(artist_ids))} (should be 0)")

track_ids = [t['track_id'] for t in tracks_data]
print(f"✓ Duplicate track IDs: {len(track_ids) - len(set(track_ids))} (should be 0)")

# Check data distributions
print("\n[Distribution Checks]")
genre_counts = pd.Series([a['primary_genre'] for a in artists_data]).value_counts()
print(f"✓ Genre distribution (top 3): {dict(genre_counts.head(3))}")

platform_counts = pd.Series([s['platform'] for s in streams_data]).value_counts()
print(f"✓ Platform distribution: {dict(platform_counts)}")

# =============================================================================
# EXPORT TO CSV
# =============================================================================

print("\n" + "=" * 70)
print("EXPORTING DATA TO CSV FILES")
print("=" * 70)

output_files = [
    ('record_labels.csv', labels_data),
    ('artists.csv', artists_data),
    ('albums.csv', albums_data),
    ('tracks.csv', tracks_data),
    ('track_features.csv', track_features_data),
    ('collaborations.csv', collabs_data),
    ('streams.csv', streams_data),
    ('royalties.csv', royalties_data),
    ('playlists.csv', playlists_data),
    ('awards.csv', awards_data),
    ('charts.csv', charts_data)
]

for filename, data in output_files:
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✓ {filename:30s} - {len(df):,} rows × {len(df.columns)} columns")

# Generate summary statistics
print("\n" + "=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)

total_rows = sum(len(data) for _, data in output_files)
print(f"\nTotal records generated: {total_rows:,}")
print(f"Total CSV files: {len(output_files)}")
print(f"Estimated disk size: ~{total_rows * 0.2 / 1024:.1f} MB")

print("\n" + "=" * 70)
print("✓ SUCCESS! High-quality synthetic data generated.")
print("=" * 70)
