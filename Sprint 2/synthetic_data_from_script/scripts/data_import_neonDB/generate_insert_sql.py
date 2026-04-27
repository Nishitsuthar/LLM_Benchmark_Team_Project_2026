#!/usr/bin/env python3
"""
Generate SQL INSERT statements from CSV files
No dependencies needed except pandas (which you already have)
"""

import pandas as pd
from pathlib import Path

# Path to CSV files
DATA_DIR = Path(__file__).parent.parent.parent / 'Data'

# CSV to table mapping
CSV_TO_TABLE = {
    'record_labels.csv': 'record_labels',
    'artists.csv': 'artists',
    'albums.csv': 'albums',
    'tracks.csv': 'tracks',
    'track_features.csv': 'track_features',
    'collaborations.csv': 'collaborations',
    'streams.csv': 'streams',
    'royalties.csv': 'royalties',
    'playlists.csv': 'playlists',
    'awards.csv': 'awards',
    'charts.csv': 'charts'
}

def escape_sql_value(value):
    """Escape SQL values properly"""
    if pd.isna(value):
        return 'NULL'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    else:
        # Escape single quotes
        value_str = str(value).replace("'", "''")
        return f"'{value_str}'"

def generate_insert_statements(csv_file, table_name, batch_size=100):
    """Generate INSERT statements for a CSV file"""
    filepath = DATA_DIR / csv_file

    if not filepath.exists():
        print(f"⚠ Warning: {csv_file} not found")
        return []

    df = pd.read_csv(filepath)

    # Get column names
    columns = ', '.join(df.columns)

    statements = []
    statements.append(f"\n-- Importing {csv_file} ({len(df)} rows)")

    # Generate batched INSERT statements for better performance
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]

        values_list = []
        for _, row in batch.iterrows():
            values = ', '.join(escape_sql_value(val) for val in row)
            values_list.append(f"({values})")

        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES\n  " + ",\n  ".join(values_list) + ";"
        statements.append(insert_sql)

    print(f"✓ Generated {len(df)} INSERT statements for {csv_file}")
    return statements

def main():
    print("=" * 80)
    print("SQL INSERT STATEMENT GENERATOR")
    print("=" * 80)
    print(f"\nLooking for CSV files in: {DATA_DIR}")

    all_statements = []
    all_statements.append("-- ============================================================================")
    all_statements.append("-- Auto-generated SQL INSERT statements from CSV files")
    all_statements.append("-- Run this AFTER creating the schema")
    all_statements.append("-- ============================================================================")
    all_statements.append("\nBEGIN;")

    total_rows = 0

    for csv_file, table_name in CSV_TO_TABLE.items():
        statements = generate_insert_statements(csv_file, table_name)
        all_statements.extend(statements)

        # Count rows
        filepath = DATA_DIR / csv_file
        if filepath.exists():
            df = pd.read_csv(filepath)
            total_rows += len(df)

    all_statements.append("\nCOMMIT;")
    all_statements.append(f"\n-- Total rows inserted: {total_rows:,}")

    # Write to file
    output_file = Path(__file__).parent / 'insert_data.sql'
    with open(output_file, 'w') as f:
        f.write('\n'.join(all_statements))

    print("\n" + "=" * 80)
    print(f"✓ SQL file generated: {output_file}")
    print(f"✓ Total rows: {total_rows:,}")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Copy insert_data.sql content")
    print("  2. Go to your Neon SQL Editor")
    print("  3. Paste and run the SQL")
    print("=" * 80)

if __name__ == '__main__':
    main()
