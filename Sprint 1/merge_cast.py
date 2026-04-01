import pandas as pd

# --- UPDATE THESE 3 FILE NAMES TO MATCH YOURS ---
MOVIES_FILE = 'title.basics.1995-2015.csv'  
PRINCIPALS_FILE = 'title.principals.csv'
NAMES_FILE = 'name.basics.csv'
# ------------------------------------------------

print("1/5: Loading your 30k filtered movies...")
movies_df = pd.read_csv(MOVIES_FILE, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')

# Convert the movie IDs to a 'set' for lightning-fast lookups
valid_tconsts = set(movies_df['tconst'])

print("2/5: Filtering the cast database (Processing in chunks to save RAM)...")
principals_chunks = []
# Read 100,000 rows at a time
for chunk in pd.read_csv(PRINCIPALS_FILE, usecols=['tconst', 'nconst', 'category'], sep='\t', engine='c', quoting=3, on_bad_lines='skip', chunksize=100000):
    # Keep only the rows that match your movies, then add them to our safe list
    filtered_chunk = chunk[chunk['tconst'].isin(valid_tconsts)]
    principals_chunks.append(filtered_chunk)

# Combine all the safe chunks together
filtered_principals = pd.concat(principals_chunks, ignore_index=True)
valid_nconsts = set(filtered_principals['nconst'])

print("3/5: Finding the human names (Processing in chunks to save RAM)...")
names_chunks = []
# Read 100,000 rows at a time
for chunk in pd.read_csv(NAMES_FILE, usecols=['nconst', 'primaryName'], sep='\t', engine='c', quoting=3, on_bad_lines='skip', chunksize=100000):
    filtered_chunk = chunk[chunk['nconst'].isin(valid_nconsts)]
    names_chunks.append(filtered_chunk)

filtered_names = pd.concat(names_chunks, ignore_index=True)

print("4/5: Stitching everything together...")
cast_with_names = pd.merge(filtered_principals, filtered_names, on='nconst', how='left')

# Format it nicely so it reads like: "Keanu Reeves (actor)"
cast_with_names['person_info'] = cast_with_names['primaryName'].astype(str) + " (" + cast_with_names['category'].astype(str) + ")"

# Group all cast members by movie ID, separated by commas
grouped_cast = cast_with_names.groupby('tconst')['person_info'].apply(lambda x: ', '.join(x)).reset_index()
grouped_cast.rename(columns={'person_info': 'Cast_and_Crew'}, inplace=True)

final_df = pd.merge(movies_df, grouped_cast, on='tconst', how='left')
final_df['Cast_and_Crew'] = final_df['Cast_and_Crew'].fillna('No Cast Data')

print("5/5: Saving to Excel...")
final_df.to_excel('Final_Movies_With_Cast.xlsx', index=False)

print("✅ Done! Open 'Final_Movies_With_Cast.xlsx' to see your results.")
