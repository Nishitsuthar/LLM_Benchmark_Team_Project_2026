#!/usr/bin/env python3
"""
Import CSV files to NeonDB (PostgreSQL)
Handles schema creation and data import automatically
"""

import psycopg2
import pandas as pd
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# NeonDB Connection String
# Format: postgresql://user:password@host/database?sslmode=require
# Get this from your Neon dashboard
NEON_CONNECTION_STRING = "postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST.neon.tech/YOUR_DATABASE?sslmode=require"

# CSV files to import (in dependency order)
CSV_FILES = [
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

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_connection_string():
    """Get connection string from environment or prompt user"""
    conn_str = os.environ.get('NEON_CONNECTION_STRING', NEON_CONNECTION_STRING)

    if 'YOUR_USER' in conn_str or 'YOUR_PASSWORD' in conn_str:
        print("=" * 80)
        print("NEON DATABASE CONNECTION")
        print("=" * 80)
        print("\nPlease enter your Neon connection string.")
        print("You can find this in your Neon dashboard under 'Connection Details'")
        print("\nFormat: postgresql://user:password@host/database?sslmode=require\n")
        conn_str = input("Connection String: ").strip()

    return conn_str


def create_schema(cursor):
    """Create database schema"""
    print("\n[1/3] Creating database schema...")

    schema_file = Path(__file__).parent / 'create_schema.sql'

    if not schema_file.exists():
        print("❌ Error: create_schema.sql not found!")
        return False

    with open(schema_file, 'r') as f:
        schema_sql = f.read()

    try:
        cursor.execute(schema_sql)
        print("✓ Schema created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        return False


def import_csv_file(cursor, filename, table_name):
    """Import a single CSV file into a table"""
    filepath = Path(__file__).parent / filename

    if not filepath.exists():
        print(f"  ⚠ Warning: {filename} not found, skipping...")
        return False

    try:
        # Read CSV
        df = pd.read_csv(filepath)

        # Convert DataFrame to list of tuples
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))

        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Insert data
        for idx, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        print(f"  ✓ {filename:30s} → {len(df):>6,} rows imported")
        return True

    except Exception as e:
        print(f"  ❌ Error importing {filename}: {e}")
        return False


def import_all_data(cursor):
    """Import all CSV files"""
    print("\n[2/3] Importing CSV data...")

    table_mapping = {
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

    success_count = 0
    for csv_file in CSV_FILES:
        table_name = table_mapping[csv_file]
        if import_csv_file(cursor, csv_file, table_name):
            success_count += 1

    print(f"\n  Total: {success_count}/{len(CSV_FILES)} files imported successfully")
    return success_count > 0


def verify_import(cursor):
    """Verify data was imported correctly"""
    print("\n[3/3] Verifying import...")

    try:
        cursor.execute("SELECT * FROM summary_stats ORDER BY row_count DESC")
        results = cursor.fetchall()

        print("\nTable Summary:")
        print("-" * 50)
        for table_name, row_count in results:
            print(f"  {table_name:30s} {row_count:>10,} rows")
        print("-" * 50)

        total_rows = sum(row[1] for row in results)
        print(f"  {'TOTAL':30s} {total_rows:>10,} rows")

        return True
    except Exception as e:
        print(f"❌ Error verifying import: {e}")
        return False


def run_sample_queries(cursor):
    """Run some sample queries to demonstrate the data"""
    print("\n" + "=" * 80)
    print("SAMPLE QUERIES")
    print("=" * 80)

    queries = [
        {
            'name': 'Top 10 Artists by Popularity',
            'sql': '''
                SELECT name, primary_genre, country, popularity_score
                FROM artists
                ORDER BY popularity_score DESC
                LIMIT 10
            '''
        },
        {
            'name': 'Most Streamed Tracks',
            'sql': '''
                SELECT t.title, a.name as artist, SUM(s.stream_count) as total_streams
                FROM tracks t
                JOIN artists a ON t.artist_id = a.artist_id
                JOIN streams s ON t.track_id = s.track_id
                GROUP BY t.track_id, t.title, a.name
                ORDER BY total_streams DESC
                LIMIT 10
            '''
        },
        {
            'name': 'Tracks by Genre',
            'sql': '''
                SELECT a.primary_genre, COUNT(t.track_id) as track_count
                FROM tracks t
                JOIN artists a ON t.artist_id = a.artist_id
                GROUP BY a.primary_genre
                ORDER BY track_count DESC
            '''
        }
    ]

    for query in queries:
        print(f"\n{query['name']}:")
        print("-" * 80)
        try:
            cursor.execute(query['sql'])
            results = cursor.fetchall()
            for row in results[:10]:  # Limit to 10 rows
                print("  ", row)
        except Exception as e:
            print(f"  Error: {e}")

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("=" * 80)
    print("NEON DATABASE IMPORT TOOL")
    print("Music Industry Synthetic Data")
    print("=" * 80)

    # Get connection string
    conn_string = get_connection_string()

    # Connect to database
    print("\nConnecting to NeonDB...")
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("✓ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTips:")
        print("  1. Check your connection string is correct")
        print("  2. Ensure your IP is whitelisted in Neon dashboard")
        print("  3. Verify SSL mode is set to 'require'")
        return

    try:
        # Create schema
        if not create_schema(cursor):
            conn.rollback()
            return

        conn.commit()

        # Import data
        if not import_all_data(cursor):
            print("\n⚠ Some files failed to import")

        conn.commit()

        # Verify import
        verify_import(cursor)

        # Run sample queries
        run_sample_queries(cursor)

        print("\n" + "=" * 80)
        print("✓ IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nYour NeonDB database is ready to use!")
        print("\nNext steps:")
        print("  1. Connect to your database using psql or any SQL client")
        print("  2. Run queries to explore the data")
        print("  3. Use the data for development, testing, or analytics")

    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
        print("\nConnection closed.")


if __name__ == '__main__':
    # Check if psycopg2 is installed
    try:
        import psycopg2
    except ImportError:
        print("=" * 80)
        print("ERROR: psycopg2 not installed")
        print("=" * 80)
        print("\nPlease install it with:")
        print("  pip3 install psycopg2-binary pandas")
        print("\nThen run this script again.")
        exit(1)

    main()
