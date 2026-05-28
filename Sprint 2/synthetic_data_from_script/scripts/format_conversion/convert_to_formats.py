#!/usr/bin/env python3
"""
Step 2: Convert the SINGLE combined CSV into multiple formats (JSON, HTML, XML)
Source: music_dataset_combined.csv (created by create_sample_and_combine.py)
"""

import pandas as pd
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = Path(__file__).parent.parent.parent / 'dataset_formats'
COMBINED_CSV = OUTPUT_DIR / 'music_dataset_combined.csv'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_combined_csv():
    """Load the combined CSV and split it back into table dictionaries"""
    print("Loading combined CSV...")

    if not COMBINED_CSV.exists():
        print(f"❌ Combined CSV not found: {COMBINED_CSV}")
        print("Please run create_sample_and_combine.py first!")
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
                    data[current_table] = pd.read_csv(StringIO(csv_content))
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
            data[current_table] = pd.read_csv(StringIO(csv_content))
            print(f"  ✓ {current_table:20s} {len(data[current_table]):>6,} rows")

    total_records = sum(len(df) for df in data.values())
    print(f"\nTotal records: {total_records:,}")

    return data


# ============================================================================
# JSON CONVERSION
# ============================================================================

def convert_to_json(data):
    """Convert to JSON format"""
    print("\n" + "="*80)
    print("Converting to JSON...")
    print("="*80)

    json_data = {
        "database": "music_industry",
        "description": "Balanced sample of music industry dataset",
        "tables": {}
    }

    for table_name, df in data.items():
        json_data["tables"][table_name] = df.to_dict(orient='records')
        print(f"  ✓ {table_name:20s} {len(df):>6,} records")

    output_file = OUTPUT_DIR / 'music_dataset.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, default=str)

    file_size_kb = output_file.stat().st_size / 1024
    print(f"\n✓ JSON: {output_file.name} ({file_size_kb:.1f} KB)")

    return output_file


# ============================================================================
# HTML CONVERSION
# ============================================================================

def convert_to_html(data):
    """Convert to HTML format"""
    print("\n" + "="*80)
    print("Converting to HTML...")
    print("="*80)

    html_parts = []

    # HTML header
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Industry Dataset - Balanced Sample</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .subtitle {
            margin-top: 10px;
            opacity: 0.9;
        }
        h2 {
            color: #667eea;
            margin-top: 40px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 40px;
            font-size: 0.9em;
        }
        th {
            background-color: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
        }
        tr:hover {
            background-color: #f8f9ff;
        }
        .table-info {
            background-color: #fff;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
            font-weight: 600;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎵 Music Industry Dataset</h1>
        <div class="subtitle">Balanced sample for LLM Benchmarking</div>
    </div>
""")

    # Convert each table
    for table_name, df in data.items():
        html_parts.append(f'\n    <h2>{table_name.replace("_", " ").title()}</h2>')
        html_parts.append(f'    <div class="table-info">{len(df):,} records</div>')
        html_parts.append('    <table>')
        html_parts.append('        <thead><tr>')

        for col in df.columns:
            html_parts.append(f'            <th>{col}</th>')

        html_parts.append('        </tr></thead>')
        html_parts.append('        <tbody>')

        for _, row in df.iterrows():
            html_parts.append('        <tr>')
            for val in row:
                display_val = '' if pd.isna(val) else str(val)
                html_parts.append(f'            <td>{display_val}</td>')
            html_parts.append('        </tr>')

        html_parts.append('        </tbody>')
        html_parts.append('    </table>')

        print(f"  ✓ {table_name:20s} {len(df):>6,} records")

    html_parts.append('\n</body>\n</html>')

    output_file = OUTPUT_DIR / 'music_dataset.html'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))

    file_size_kb = output_file.stat().st_size / 1024
    print(f"\n✓ HTML: {output_file.name} ({file_size_kb:.1f} KB)")

    return output_file


# ============================================================================
# XML CONVERSION
# ============================================================================

def convert_to_xml(data):
    """Convert to XML format"""
    print("\n" + "="*80)
    print("Converting to XML...")
    print("="*80)

    root = ET.Element('database')
    root.set('name', 'music_industry')
    root.set('type', 'balanced_sample')

    for table_name, df in data.items():
        table_elem = ET.SubElement(root, table_name)
        table_elem.set('record_count', str(len(df)))

        singular = table_name.rstrip('s') if table_name.endswith('s') else table_name

        for _, row in df.iterrows():
            record_elem = ET.SubElement(table_elem, singular)

            for col in df.columns:
                col_elem = ET.SubElement(record_elem, col)
                val = row[col]
                col_elem.text = '' if pd.isna(val) else str(val)

        print(f"  ✓ {table_name:20s} {len(df):>6,} records")

    xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

    output_file = OUTPUT_DIR / 'music_dataset.xml'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_string)

    file_size_kb = output_file.stat().st_size / 1024
    print(f"\n✓ XML: {output_file.name} ({file_size_kb:.1f} KB)")

    return output_file


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("STEP 2: FORMAT CONVERSION")
    print("Converting combined CSV to JSON, HTML, XML")
    print("="*80)

    data = load_combined_csv()

    if not data:
        return

    files = {}
    files['JSON'] = convert_to_json(data)
    files['HTML'] = convert_to_html(data)
    files['XML'] = convert_to_xml(data)

    print("\n" + "="*80)
    print("STEP 2 COMPLETED!")
    print("="*80)

    print(f"\nAll files in: {OUTPUT_DIR}")
    print("\nGenerated formats:")
    for name, filepath in files.items():
        size_kb = filepath.stat().st_size / 1024
        print(f"  • {filepath.name:30s} {size_kb:>8.1f} KB")


if __name__ == '__main__':
    main()
