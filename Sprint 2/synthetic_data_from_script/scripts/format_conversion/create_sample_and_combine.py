#!/usr/bin/env python3
"""
Step 1: Create a balanced sample of the dataset
Maintains referential integrity and distribution balance
Then combines into ONE master CSV file
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Sample size configuration - adjust these to control final file size
SAMPLE_CONFIG = {
    'artists': 0.15,        # 15% of artists (~105 artists)
    'albums': 0.15,         # 15% of albums (from sampled artists)
    'tracks': 0.10,         # 10% of tracks (from sampled albums)
    'streams': 0.05,        # 5% of streams (from sampled tracks)
    'royalties': 0.08,      # 8% of royalties (from sampled tracks)
    'track_features': 1.0,  # 100% for sampled tracks (required)
    'collaborations': 0.15, # 15% of collaborations (from sampled artists)
    'playlists': 0.10,      # 10% of playlists (from sampled tracks)
    'awards': 0.15,         # 15% of awards (from sampled artists)
    'charts': 0.10,         # 10% of chart entries (from sampled tracks)
    'record_labels': 1.0    # 100% of labels (small table)
}

DATA_DIR = Path(__file__).parent.parent.parent / 'Data'
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'dataset_formats'

TABLE_ORDER = [
    'record_labels', 'artists', 'albums', 'tracks', 'track_features',
    'collaborations', 'streams', 'royalties', 'playlists', 'awards', 'charts'
]

# ============================================================================
# SAMPLING FUNCTIONS
# ============================================================================

def load_data():
    """Load all CSV files"""
    print("Loading full dataset...")
    data = {}

    for table in TABLE_ORDER:
        filepath = DATA_DIR / f'{table}.csv'
        if filepath.exists():
            data[table] = pd.read_csv(filepath)
            print(f"  ✓ {table:20s} {len(data[table]):>6,} rows")
        else:
            print(f"  ✗ {table:20s} NOT FOUND")

    return data


def sample_artists_balanced(df, sample_ratio=0.15):
    """Sample artists with balanced distribution across genres and countries"""
    print("\nBalanced sampling artists...")

    # Create popularity tiers
    df['popularity_tier'] = pd.qcut(df['popularity_score'],
                                      q=4,
                                      labels=['Low', 'Medium', 'High', 'Very High'])

    # Stratified sampling
    sampled = df.groupby(['primary_genre', 'country', 'popularity_tier'],
                         group_keys=False).apply(
        lambda x: x.sample(frac=sample_ratio, random_state=42) if len(x) > 1 else x
    )

    sampled = sampled.drop('popularity_tier', axis=1)

    print(f"  Original: {len(df):,} artists")
    print(f"  Sampled:  {len(sampled):,} artists ({len(sampled)/len(df)*100:.1f}%)")

    return sampled


def sample_dependent_table(df, parent_ids, parent_col, sample_ratio):
    """Sample rows that reference parent IDs"""
    filtered = df[df[parent_col].isin(parent_ids)]

    if len(filtered) == 0 or sample_ratio >= 1.0:
        return filtered

    sample_size = max(1, int(len(filtered) * sample_ratio))
    sampled = filtered.sample(n=min(sample_size, len(filtered)), random_state=42)

    return sampled


def create_balanced_sample(data):
    """Create balanced sample maintaining referential integrity"""
    sampled = {}

    print("\n" + "="*80)
    print("CREATING BALANCED SAMPLE")
    print("="*80)

    # 1. Record labels (keep all)
    sampled['record_labels'] = data['record_labels'].copy()
    print(f"\n✓ record_labels: {len(sampled['record_labels']):,} (100%)")

    # 2. Artists (balanced)
    sampled['artists'] = sample_artists_balanced(data['artists'], SAMPLE_CONFIG['artists'])
    sampled_artist_ids = set(sampled['artists']['artist_id'])

    # 3. Albums
    sampled['albums'] = sample_dependent_table(
        data['albums'], sampled_artist_ids, 'artist_id', SAMPLE_CONFIG['albums']
    )
    print(f"✓ albums: {len(sampled['albums']):,} ({len(sampled['albums'])/len(data['albums'])*100:.1f}%)")
    sampled_album_ids = set(sampled['albums']['album_id'])

    # 4. Tracks
    sampled['tracks'] = sample_dependent_table(
        data['tracks'], sampled_album_ids, 'album_id', SAMPLE_CONFIG['tracks']
    )
    print(f"✓ tracks: {len(sampled['tracks']):,} ({len(sampled['tracks'])/len(data['tracks'])*100:.1f}%)")
    sampled_track_ids = set(sampled['tracks']['track_id'])

    # 5. Track features
    sampled['track_features'] = data['track_features'][
        data['track_features']['track_id'].isin(sampled_track_ids)
    ]
    print(f"✓ track_features: {len(sampled['track_features']):,}")

    # 6. Collaborations (must also have valid track_id)
    collab_filtered = data['collaborations'][
        (data['collaborations']['primary_artist_id'].isin(sampled_artist_ids) |
         data['collaborations']['featured_artist_id'].isin(sampled_artist_ids)) &
        data['collaborations']['track_id'].isin(sampled_track_ids)
    ]
    sample_size = max(1, int(len(collab_filtered) * SAMPLE_CONFIG['collaborations']))
    sampled['collaborations'] = collab_filtered.sample(
        n=min(sample_size, len(collab_filtered)), random_state=42
    ) if len(collab_filtered) > 0 else collab_filtered
    collab_pct = (len(sampled['collaborations'])/len(data['collaborations'])*100) if len(data['collaborations']) > 0 else 0
    print(f"✓ collaborations: {len(sampled['collaborations']):,} ({collab_pct:.1f}%)")

    # 7. Streams
    sampled['streams'] = sample_dependent_table(
        data['streams'], sampled_track_ids, 'track_id', SAMPLE_CONFIG['streams']
    )
    print(f"✓ streams: {len(sampled['streams']):,} ({len(sampled['streams'])/len(data['streams'])*100:.1f}%)")

    # 8. Royalties
    sampled['royalties'] = sample_dependent_table(
        data['royalties'], sampled_track_ids, 'track_id', SAMPLE_CONFIG['royalties']
    )
    print(f"✓ royalties: {len(sampled['royalties']):,} ({len(sampled['royalties'])/len(data['royalties'])*100:.1f}%)")

    # 9. Playlists
    sampled['playlists'] = sample_dependent_table(
        data['playlists'], sampled_track_ids, 'track_id', SAMPLE_CONFIG['playlists']
    )
    print(f"✓ playlists: {len(sampled['playlists']):,} ({len(sampled['playlists'])/len(data['playlists'])*100:.1f}%)")

    # 10. Awards (only artist-level awards, no track-specific ones to avoid FK issues)
    awards_filtered = data['awards'][
        data['awards']['artist_id'].isin(sampled_artist_ids) &
        data['awards']['track_id'].isna()
    ]
    sampled['awards'] = sample_dependent_table(
        awards_filtered, sampled_artist_ids, 'artist_id', SAMPLE_CONFIG['awards']
    )
    print(f"✓ awards: {len(sampled['awards']):,} ({len(sampled['awards'])/len(data['awards'])*100:.1f}%)")

    # 11. Charts
    sampled['charts'] = sample_dependent_table(
        data['charts'], sampled_track_ids, 'track_id', SAMPLE_CONFIG['charts']
    )
    print(f"✓ charts: {len(sampled['charts']):,} ({len(sampled['charts'])/len(data['charts'])*100:.1f}%)")

    return sampled


def create_combined_csv(sampled):
    """Combine all sampled tables into ONE master CSV file"""
    print("\n" + "="*80)
    print("CREATING COMBINED CSV (SINGLE SOURCE)")
    print("="*80)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / 'music_dataset_combined.csv'

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, table_name in enumerate(TABLE_ORDER):
            if table_name not in sampled:
                continue

            df = sampled[table_name]

            # Write table separator
            if i > 0:
                f.write("\n")

            f.write(f"### TABLE: {table_name} ###\n")
            df.to_csv(f, index=False)

            print(f"  ✓ {table_name:20s} → {len(df):>6,} rows")

    file_size_kb = output_file.stat().st_size / 1024
    print(f"\n✓ Combined CSV created: {output_file.name} ({file_size_kb:.1f} KB)")

    return output_file


def print_summary(original, sampled):
    """Print sampling summary"""
    print("\n" + "="*80)
    print("SAMPLING SUMMARY")
    print("="*80)

    print("\n{:20s} {:>10s} {:>10s} {:>10s}".format("Table", "Original", "Sampled", "Ratio"))
    print("-" * 55)

    total_orig = 0
    total_samp = 0

    for table in TABLE_ORDER:
        if table not in sampled:
            continue

        orig_count = len(original[table])
        samp_count = len(sampled[table])
        ratio = samp_count / orig_count if orig_count > 0 else 0

        print("{:20s} {:>10,} {:>10,} {:>9.1%}".format(
            table, orig_count, samp_count, ratio
        ))

        total_orig += orig_count
        total_samp += samp_count

    print("-" * 55)
    print("{:20s} {:>10,} {:>10,} {:>9.1%}".format(
        "TOTAL", total_orig, total_samp, total_samp/total_orig
    ))


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("STEP 1: CREATE BALANCED SAMPLE + COMBINED CSV")
    print("="*80)

    # Load data
    data = load_data()

    if not data:
        print("\n❌ No data found!")
        return

    # Create balanced sample
    sampled = create_balanced_sample(data)

    # Create combined CSV (single source)
    combined_file = create_combined_csv(sampled)

    # Print summary
    print_summary(data, sampled)

    print("\n" + "="*80)
    print("✓ STEP 1 COMPLETED!")
    print("="*80)
    print(f"\nOutput: {combined_file}")
    print("\n✓ This combined CSV is the SINGLE SOURCE for all format conversions")
    print("\nNext step: Run convert_to_formats.py")


if __name__ == '__main__':
    main()
