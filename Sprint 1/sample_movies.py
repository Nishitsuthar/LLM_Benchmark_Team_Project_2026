import pandas as pd

print("Loading the massive dataset...")
# 1. Load your newly created dataset from the last step
df = pd.read_excel('Final_Movies_With_Cast.xlsx')

# 2. Filter for exactly 20 years (1996 to 2015) to get exactly 500 movies
df_filtered = df[(df['startYear'] >= 1996) & (df['startYear'] <= 2015)]

# 3. Create an empty list to hold our final sampled rows
sampled_movies = []

print("Running the Stratified Random Sampler...")
# 4. Loop through each year one by one
for year in range(1996, 2016):
    
    # Grab all movies for this specific year
    year_data = df_filtered[df_filtered['startYear'] == year]
    
    # Split them into your 3 rating categories
    # Note: We use < 8.0 for medium so we don't accidentally count an 8.0 twice!
    top_movies = year_data[year_data['averageRating'] >= 8.0]
    med_movies = year_data[(year_data['averageRating'] >= 5.0) & (year_data['averageRating'] < 8.0)]
    low_movies = year_data[year_data['averageRating'] < 5.0]
    
    # Randomly sample them (8 Top, 9 Medium, 8 Low = 25 total per year)
    # The "min()" function is a safety net: if a year only has 6 low-rated movies, 
    # it will just take those 6 instead of crashing.
    # random_state=42 ensures you get the exact same "random" movies if you run the script twice.
    top_sample = top_movies.sample(n=min(17, len(top_movies)), random_state=42)
    med_sample = med_movies.sample(n=min(16, len(med_movies)), random_state=42)
    low_sample = low_movies.sample(n=min(17, len(low_movies)), random_state=42)
    
    # Add this year's 25 movies to our master list
    sampled_movies.extend([top_sample, med_sample, low_sample])

# 5. Combine all the pieces back together into one final dataset
final_500_df = pd.concat(sampled_movies, ignore_index=True)

print("Saving final dataset...")
# 6. Save the final sample to a brand new file
final_500_df.to_excel('Sampled_500_Movies.xlsx', index=False)

print(f"✅ Success! You now have a perfectly balanced dataset of {len(final_500_df)} movies.")
