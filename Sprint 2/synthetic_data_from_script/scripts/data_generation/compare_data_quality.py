"""
Data Quality Comparison Tool
Compare outputs from original vs enhanced generators
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

def analyze_csv(filepath):
    """Analyze a CSV file and return statistics"""
    if not Path(filepath).exists():
        return None

    df = pd.read_csv(filepath)

    stats = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': list(df.columns),
        'null_count': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }

    # Detect numeric columns and calculate distributions
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        stats['numeric_columns'] = len(numeric_cols)
        stats['mean_values'] = df[numeric_cols].mean().to_dict()
        stats['std_values'] = df[numeric_cols].std().to_dict()

    # Detect date columns
    date_cols = [col for col in df.columns if 'date' in col.lower() or 'year' in col.lower()]
    stats['date_columns'] = len(date_cols)

    return stats


def compare_files(original_dir='.', enhanced_dir='.'):
    """Compare all CSV files between original and enhanced versions"""

    files_to_compare = [
        'record_labels.csv',
        'artists.csv',
        'albums.csv',
        'tracks.csv',
        'track_features.csv',
        'collaborations.csv',
        'streams.csv',
        'royalties.csv',
        'playlists.csv',
        'awards.csv',
        'charts.csv'
    ]

    print("=" * 80)
    print("DATA QUALITY COMPARISON REPORT")
    print("=" * 80)

    comparison_results = []

    for filename in files_to_compare:
        orig_path = Path(original_dir) / filename
        enh_path = Path(enhanced_dir) / filename

        print(f"\n[{filename}]")
        print("-" * 80)

        if orig_path.exists():
            orig_stats = analyze_csv(orig_path)
            print(f"Original:  {orig_stats['rows']:,} rows × {orig_stats['columns']} cols | "
                  f"{orig_stats['null_count']} nulls | {orig_stats['duplicate_rows']} dupes")
        else:
            orig_stats = None
            print("Original:  FILE NOT FOUND")

        if enh_path.exists():
            enh_stats = analyze_csv(enh_path)
            print(f"Enhanced:  {enh_stats['rows']:,} rows × {enh_stats['columns']} cols | "
                  f"{enh_stats['null_count']} nulls | {enh_stats['duplicate_rows']} dupes")
        else:
            enh_stats = None
            print("Enhanced:  FILE NOT FOUND")

        if orig_stats and enh_stats:
            # Column comparison
            orig_cols = set(orig_stats['column_names'])
            enh_cols = set(enh_stats['column_names'])

            new_cols = enh_cols - orig_cols
            if new_cols:
                print(f"New columns in enhanced: {', '.join(new_cols)}")

            removed_cols = orig_cols - enh_cols
            if removed_cols:
                print(f"Removed columns: {', '.join(removed_cols)}")

            comparison_results.append({
                'file': filename,
                'original_rows': orig_stats['rows'],
                'enhanced_rows': enh_stats['rows'],
                'original_cols': orig_stats['columns'],
                'enhanced_cols': enh_stats['columns'],
                'new_columns': len(new_cols),
                'quality_improvement': '+' if enh_stats['columns'] > orig_stats['columns'] else '='
            })

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if comparison_results:
        summary_df = pd.DataFrame(comparison_results)
        print(summary_df.to_string(index=False))

        print(f"\nTotal new columns across all files: {summary_df['new_columns'].sum()}")
        print(f"Average column increase: {summary_df['new_columns'].mean():.1f} per file")
    else:
        print("No comparisons available. Please generate data first.")

    print("\n" + "=" * 80)


def validate_data_quality(directory='.'):
    """Run comprehensive validation checks"""

    print("\n" + "=" * 80)
    print("DATA QUALITY VALIDATION")
    print("=" * 80)

    # Check for referential integrity
    print("\n[Referential Integrity]")

    try:
        labels = pd.read_csv(Path(directory) / 'record_labels.csv')
        artists = pd.read_csv(Path(directory) / 'artists.csv')
        albums = pd.read_csv(Path(directory) / 'albums.csv')
        tracks = pd.read_csv(Path(directory) / 'tracks.csv')

        # Check label references
        invalid_labels = artists[~artists['label_id'].isin(labels['label_id'])]
        print(f"✓ Artists with invalid label_id: {len(invalid_labels)} (should be 0)")

        # Check artist references in albums
        invalid_artists = albums[~albums['artist_id'].isin(artists['artist_id'])]
        print(f"✓ Albums with invalid artist_id: {len(invalid_artists)} (should be 0)")

        # Check album references in tracks
        invalid_albums = tracks[~tracks['album_id'].isin(albums['album_id'])]
        print(f"✓ Tracks with invalid album_id: {len(invalid_albums)} (should be 0)")

    except FileNotFoundError as e:
        print(f"⚠ Could not validate: {e}")

    # Check temporal consistency
    print("\n[Temporal Consistency]")

    try:
        artist_debut = artists.set_index('artist_id')['debut_year'].to_dict()
        albums['artist_debut'] = albums['artist_id'].map(artist_debut)
        temporal_violations = albums[albums['release_year'] < albums['artist_debut']]
        print(f"✓ Albums released before artist debut: {len(temporal_violations)} (should be 0)")

    except Exception as e:
        print(f"⚠ Could not validate: {e}")

    # Check for duplicates
    print("\n[Uniqueness]")

    for filename, id_col in [
        ('record_labels.csv', 'label_id'),
        ('artists.csv', 'artist_id'),
        ('albums.csv', 'album_id'),
        ('tracks.csv', 'track_id')
    ]:
        try:
            df = pd.read_csv(Path(directory) / filename)
            duplicates = df[id_col].duplicated().sum()
            print(f"✓ {filename:25s} duplicate {id_col}s: {duplicates} (should be 0)")
        except Exception as e:
            print(f"⚠ {filename:25s} could not check: {e}")

    # Distribution analysis
    print("\n[Distribution Analysis]")

    try:
        # Check if popularity scores follow power-law
        if 'popularity_score' in artists.columns:
            pop_scores = artists['popularity_score'].values
            top_20_pct = np.percentile(pop_scores, 80)
            top_20_artists = artists[artists['popularity_score'] >= top_20_pct]
            top_20_avg = top_20_artists['popularity_score'].mean()
            bottom_80_avg = artists[artists['popularity_score'] < top_20_pct]['popularity_score'].mean()

            print(f"✓ Top 20% avg popularity: {top_20_avg:.3f}")
            print(f"✓ Bottom 80% avg popularity: {bottom_80_avg:.3f}")
            print(f"✓ Ratio (should be 2-4x for power-law): {top_20_avg / bottom_80_avg:.2f}x")

    except Exception as e:
        print(f"⚠ Could not analyze distributions: {e}")

    print("\n" + "=" * 80)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Compare and validate synthetic data quality')
    parser.add_argument('--compare', action='store_true', help='Compare original vs enhanced')
    parser.add_argument('--validate', action='store_true', help='Validate data quality')
    parser.add_argument('--dir', default='.', help='Directory containing CSV files')

    args = parser.parse_args()

    if args.compare:
        compare_files(args.dir, args.dir)
    elif args.validate:
        validate_data_quality(args.dir)
    else:
        # Default: run both
        compare_files(args.dir, args.dir)
        validate_data_quality(args.dir)

    print("\n✓ Analysis complete!")
