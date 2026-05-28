# PHASE 1: INDIVIDUAL QUESTION MODE TESTING
# Test each of the 20 questions separately (one at a time)

## Test Matrix
- **Formats**: CSV, HTML, JSON, XML
- **Mode**: Individual (one question at a time)
- **Model**: Gemini 3.1 Pro Extended
- **Approach**: Zero-shot, baseline (no special prompting)

---

## INDIVIDUAL QUESTION PROMPTS

For each format, ask questions ONE AT A TIME with this structure:

```
I have a music industry dataset in [FORMAT] format attached.

Please analyze the data and answer this question:

[QUESTION TEXT]

Provide:
1. Your answer
2. Brief explanation of your approach
```

---

## CSV FORMAT PROMPTS (20 individual tests)

### Q001 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Which artist has the highest popularity score and how many albums have they released?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q002 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

What is the average track duration in minutes across all tracks?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q003 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Which music genre has the most artists and how many?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q004 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

What percentage of artists are currently active?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q005 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

How many tracks have explicit content?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q006 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Which record label has signed the most artists?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q007 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

What is the average number of tracks per album for each genre?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q008 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Which artists have won at least one award and how many awards have they won in total?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q009 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

What is the distribution of album types (Single, EP, Album) by record label type (Major, Independent)?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q010 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Which tracks have the highest energy and danceability scores combined?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q011 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

What is the average popularity score for artists from each country?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q012 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Which artists have tracks in multiple albums and how many albums do they have?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q013 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

What is the average speechiness score for explicit vs non-explicit tracks?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q014 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Calculate the "musical diversity score" for each artist based on the variance of their track features (energy, danceability, valence). Which artist has the highest diversity?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q015 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Identify "overperforming" artists: those whose award count is disproportionately high relative to their album count and popularity score.

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q016 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Create a "track mood profile" by categorizing tracks based on valence and energy into quadrants (Happy/High Energy, Happy/Low Energy, Sad/High Energy, Sad/Low Energy). What is the distribution?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q017 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Calculate the "genre dominance score" for each genre based on artist count, album count, and average popularity. Which genre is most dominant?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q018 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Identify "prolific years" for the music industry by counting albums released per year and calculating the year-over-year growth rate.

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q019 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Calculate the "acoustic-electronic spectrum" for each genre by averaging acousticness and instrumentalness. Which genres are most acoustic vs electronic?

Provide:
1. Your answer
2. Brief explanation of your approach
```

### Q020 - CSV Individual
```
I have a music industry dataset in CSV format attached (music_dataset_combined.csv).

Please analyze the data and answer this question:

Identify "hidden gem" tracks: high audio quality features (low speechiness, high instrumentalness) from less popular artists (popularity < 0.5) that have not been heavily streamed.

Provide:
1. Your answer
2. Brief explanation of your approach
```

---

## HTML FORMAT PROMPTS (20 individual tests)

Replace "CSV format" with "HTML format" and "music_dataset_combined.csv" with "music_dataset.html"

Use same question structure for Q001-Q020.

---

## JSON FORMAT PROMPTS (20 individual tests)

Replace "CSV format" with "JSON format" and "music_dataset_combined.csv" with "music_dataset.json"

Use same question structure for Q001-Q020.

---

## XML FORMAT PROMPTS (20 individual tests)

Replace "CSV format" with "XML format" and "music_dataset_combined.csv" with "music_dataset.xml"

Use same question structure for Q001-Q020.

---

## TESTING INSTRUCTIONS

1. **Start with ONE format** (e.g., CSV)
2. **Ask Q001**, record answer
3. **Ask Q002**, record answer
4. Continue through Q020
5. **Repeat for other formats** (HTML, JSON, XML)

## EXPECTED RESULTS TRACKING

Create a spreadsheet or document with:
- Columns: Question ID | Format | Gemini Answer | Ground Truth | Correct? | Notes
- Track which specific questions improve/worsen with individual mode

---

## HYPOTHESIS TO TEST

Individual mode may perform better because:
- Model focuses on one question at a time
- Less context confusion
- More careful analysis per question
- Fewer accumulating errors

OR it may perform worse because:
- Can't leverage cross-question insights
- Reloads data for each question (slower)
- No learning from previous questions

Let's find out!
