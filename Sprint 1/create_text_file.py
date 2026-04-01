import pandas as pd

print("Loading the sampled 500 movies...")
# 1. Load the balanced dataset you just created
df = pd.read_excel('Sampled_500_Movies.xlsx')

print("Translating rows into unstructured text...")
# 2. Open a brand new text file to hold the output
with open('Unstructured_500_Movies.txt', 'w', encoding='utf-8') as file:
    
    # 3. Loop through every single movie in the Excel file
    for index, row in df.iterrows():
        
        # Pull the data, using a fallback just in case a field is blank
        title = row.get('primaryTitle', 'Unknown Title')
        year = row.get('startYear', 'Unknown Year')
        genres = row.get('genres', 'Unknown Genres')
        rating = row.get('averageRating', 'No Rating')
        votes = row.get('numVotes', '0')
        cast = row.get('Cast_and_Crew', 'No Cast Data')
        
        # 4. Design the unstructured paragraph format
        paragraph = (
            f"Record {index + 1}: The movie '{title}' was released in {year}. "
            f"It falls under the genres of {genres}. On IMDb, it has an average "
            f"rating of {rating} out of 10, based on {votes} user votes. "
            f"The notable cast and crew associated with this production are: {cast}."
        )
        
        # 5. Write the paragraph to the text file, adding two blank lines between each movie
        file.write(paragraph + "\n\n")

print("✅ Success! Your 500 movies are now compiled into 'Unstructured_500_Movies.txt'.")
