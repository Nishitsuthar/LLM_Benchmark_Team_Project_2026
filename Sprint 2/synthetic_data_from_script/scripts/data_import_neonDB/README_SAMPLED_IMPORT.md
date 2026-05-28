# Import Sampled Data to NeonDB

## 📋 Purpose

Import the **sampled dataset (678 records)** to NeonDB so you can regenerate ground truth answers for your 30 benchmark questions.

---

## 🚀 Quick Start

### Step 1: Run Import Script

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 2/synthetic_data_from_script/scripts/data_import_neonDB"

python3 import_sampled_to_neon.py
```

The script will:
1. Load `dataset_formats/music_dataset_combined.csv`
2. Drop existing tables (if any)
3. Create fresh schema
4. Import all 678 records
5. Verify import succeeded

---

## 🔧 What You Need

1. **NeonDB Connection String**
   - Get from Neon dashboard → Connection Details
   - Format: `postgresql://user:password@host/database?sslmode=require`

2. **Schema File**
   - The script needs `create_schema.sql` in the same directory
   - This should already exist from your previous work

---

## 📊 What Gets Imported

| Table | Records | Notes |
|-------|---------|-------|
| record_labels | 50 | All labels |
| artists | 294 | Balanced sample |
| albums | 104 | From sampled artists |
| tracks | 44 | From sampled albums |
| track_features | 44 | All features for sampled tracks |
| collaborations | 81 | From sampled artists |
| streams | 3 | From sampled tracks |
| royalties | 1 | From sampled tracks |
| playlists | 2 | From sampled tracks |
| awards | 54 | From sampled artists |
| charts | 1 | From sampled tracks |
| **TOTAL** | **678** | **2.1% of original** |

---

## ⚠️ Important Notes

- **Existing data will be DELETED** - The script drops all tables first
- **Use the sampled data** - Not the full dataset (to match your format files)
- **Single source** - Imports from `music_dataset_combined.csv`

---

## ✅ After Import

Once import succeeds, you need to:

### 1. Re-run All 30 SQL Queries

Open your NeonDB and execute each query from `llm_benchmark_questions.csv`:

```sql
-- Example: Q001
SELECT a.name, a.popularity_score, COUNT(DISTINCT al.album_id) as album_count
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
WHERE a.popularity_score = (SELECT MAX(popularity_score) FROM artists)
GROUP BY a.artist_id, a.name, a.popularity_score;
```

### 2. Record New Answers

Copy results and update the `answer` column in `llm_benchmark_questions.csv`

### 3. Then Test with GPT!

Upload format files to GPT and compare with your new ground truth.

---

## 🐛 Troubleshooting

### "create_schema.sql not found"
```bash
# Make sure the schema file exists
ls scripts/data_import_neonDB/create_schema.sql
```

### "Connection failed"
- Check connection string format
- Verify IP is whitelisted in Neon dashboard
- Ensure SSL mode is 'require'

### "Combined CSV not found"
```bash
# Make sure you ran the sampling pipeline first
ls dataset_formats/music_dataset_combined.csv
```

---

## 🎯 Full Workflow

```
1. ✅ Create sampled data (DONE)
   → run_pipeline.py generated 678-record sample

2. 📍 Import to NeonDB (YOU ARE HERE)
   → import_sampled_to_neon.py

3. ⏳ Regenerate ground truth (NEXT)
   → Run 30 SQL queries manually
   → Update llm_benchmark_questions.csv

4. 🚀 Test with GPT (FINAL)
   → Upload format files
   → Compare with ground truth
```

---

**Ready to import? Run the script and provide your NeonDB connection string when prompted!**
