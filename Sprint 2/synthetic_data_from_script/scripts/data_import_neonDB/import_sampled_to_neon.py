#!/usr/bin/env python3
"""
Import Sampled CSV Data to NeonDB
Imports the sampled dataset (678 records) to regenerate ground truth
"""

import psycopg2
import pandas as pd
import os
from pathlib import Path
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

# NeonDB Connection String
# Get this from your Neon dashboard
NEON_CONNECTION_STRING = "postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST.neon.tech/YOUR_DATABASE?sslmode=require"

# Path to combined CSV
COMBINED_CSV = Path(__file__).parent.parent.parent / 'dataset_formats' / 'music_dataset_combined.csv'

# Table order (for proper foreign key handling)
TABLE_ORDER = [
    'record_labels',
    'artists',
    'albums',
    'tracks',
    'track_features',
    'collaborations',
    'streams',
    'royalties',
    'playlists',
    'awards',
    'charts'
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


def load_combined_csv():
    """Load and parse the combined CSV into separate table DataFrames"""
    print("\nLoading combined CSV...")

    if not COMBINED_CSV.exists():
        print(f"❌ File not found: {COMBINED_CSV}")
        return None

    data = {}
    current_table = None
    table_lines = []

    with open(COMBINED_CSV, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('### TABLE:'):
                # Save previous table
                if current_table and table_lines:
                    from io import StringIO
                    csv_content = ''.join(table_lines)
                    # Read CSV, treating empty strings as actual empty strings
                    data[current_table] = pd.read_csv(StringIO(csv_content), keep_default_na=True)
                    print(f"  ✓ {current_table:20s} {len(data[current_table]):>6,} rows")

                # Extract new table name
                match = re.search(r'### TABLE: (\w+) ###', line)
                if match:
                    current_table = match.group(1)
                    table_lines = []
            else:
                if current_table:
                    table_lines.append(line)

        # Save last table
        if current_table and table_lines:
            from io import StringIO
            csv_content = ''.join(table_lines)
            data[current_table] = pd.read_csv(StringIO(csv_content), keep_default_na=True)
            print(f"  ✓ {current_table:20s} {len(data[current_table]):>6,} rows")

    total_records = sum(len(df) for df in data.values())
    print(f"\n✓ Total records: {total_records:,}")

    return data


def drop_existing_tables(cursor):
    """Drop existing tables if they exist"""
    print("\n[1/4] Dropping existing tables (if any)...")

    # Drop in reverse order due to foreign keys
    tables_reverse = list(reversed(TABLE_ORDER))

    for table in tables_reverse:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            print(f"  ✓ Dropped {table}")
        except Exception as e:
            print(f"  ⚠ Could not drop {table}: {e}")


def create_schema(cursor):
    """Create database schema"""
    print("\n[2/4] Creating database schema...")

    schema_file = Path(__file__).parent / 'create_schema.sql'

    if not schema_file.exists():
        print("❌ Error: create_schema.sql not found!")
        print(f"   Looking for: {schema_file}")
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


def import_table_data(cursor, table_name, df):
    """Import a single table's data"""
    if df is None or len(df) == 0:
        print(f"  ⚠ {table_name}: No data to import")
        return 0

    try:
        # Make a copy to avoid modifying original
        df = df.copy()

        # Convert DataFrame to list of tuples
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))

        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Insert data - convert NaN to None for SQL NULL
        inserted = 0
        for idx, row in df.iterrows():
            # Convert row to list, replacing NaN with None
            row_values = [None if pd.isna(val) else val for val in row]
            cursor.execute(insert_query, tuple(row_values))
            inserted += 1

        print(f"  ✓ {table_name:20s} {inserted:>6,} rows imported")
        return inserted

    except Exception as e:
        print(f"  ❌ Error importing {table_name}: {e}")
        return 0


def import_all_data(cursor, data):
    """Import all tables"""
    print("\n[3/4] Importing sampled data...")

    total_imported = 0

    for table_name in TABLE_ORDER:
        if table_name in data:
            imported = import_table_data(cursor, table_name, data[table_name])
            total_imported += imported

    print(f"\n✓ Total rows imported: {total_imported:,}")
    return total_imported > 0


def verify_import(cursor):
    """Verify data was imported correctly"""
    print("\n[4/4] Verifying import...")

    try:
        # Count rows in each table
        print("\nTable Summary:")
        print("-" * 50)

        total_rows = 0
        for table_name in TABLE_ORDER:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name:30s} {count:>6,} rows")
            total_rows += count

        print("-" * 50)
        print(f"  {'TOTAL':30s} {total_rows:>6,} rows")

        return True
    except Exception as e:
        print(f"❌ Error verifying import: {e}")
        return False


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("=" * 80)
    print("IMPORT SAMPLED DATA TO NEONDB")
    print("For Ground Truth Regeneration")
    print("=" * 80)

    # Load combined CSV
    data = load_combined_csv()

    if not data:
        return

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
        # Drop existing tables
        drop_existing_tables(cursor)
        conn.commit()

        # Create schema
        if not create_schema(cursor):
            conn.rollback()
            return

        conn.commit()

        # Import data
        if not import_all_data(cursor, data):
            print("\n⚠ Some tables failed to import")

        conn.commit()

        # Verify import
        verify_import(cursor)

        print("\n" + "=" * 80)
        print("✓ IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nYour NeonDB now contains the SAMPLED dataset (678 records)")
        print("\nNext steps:")
        print("  1. Run all 30 SQL queries from llm_benchmark_questions.csv")
        print("  2. Update the 'answer' column with new ground truth")
        print("  3. Then you can test with GPT and compare results!")

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
