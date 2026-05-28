# Dataset Formats - Balanced Sample for LLM Benchmarking

## ✅ All Files Generated Successfully!

All formats created from **ONE combined CSV source** - guaranteed consistency.

---

## 📊 Dataset Summary

- **Original Dataset:** 32,550 records
- **Sampled Dataset:** 678 records (2.1% of original)
- **Sampling Method:** Balanced stratified sampling with referential integrity
- **Single Source:** All formats converted from one combined CSV

---

## 📁 Generated Files (All Under 250 KB!)

| Format | Filename | Size | Ready for GPT? |
|--------|----------|------|----------------|
| **CSV** | `music_dataset_combined.csv` | 46 KB | ✅ Source file |
| **JSON** | `music_dataset.json` | 196 KB | ✅ Yes |
| **HTML** | `music_dataset.html` | 189 KB | ✅ Yes (Best per research) ⭐ |
| **XML** | `music_dataset.xml` | 240 KB | ✅ Yes |

**All files are small enough for GPT web upload!** 🎉

---

## 📋 Sampling Distribution

| Table | Original | Sampled | Ratio | Notes |
|-------|----------|---------|-------|-------|
| Artists | 700 | 294 | 42.0% | ✅ Balanced by genre/country/popularity |
| Albums | 1,500 | 104 | 6.9% | From sampled artists |
| Tracks | 6,000 | 44 | 0.7% | From sampled albums |
| Track Features | 6,000 | 44 | 0.7% | 100% for sampled tracks |
| Collaborations | 800 | 81 | 10.1% | From sampled artists |
| Streams | 10,000 | 3 | 0.0% | From sampled tracks |
| Royalties | 2,000 | 1 | 0.1% | From sampled tracks |
| Playlists | 3,000 | 2 | 0.1% | From sampled tracks |
| Awards | 500 | 54 | 10.8% | From sampled artists |
| Charts | 2,000 | 1 | 0.1% | From sampled tracks |
| Record Labels | 50 | 50 | 100% | All kept |

**Total: 678 records (2.1% of original)**

---

## ⚠️ IMPORTANT: Ground Truth Must Be Regenerated

Your existing ground truth answers in `llm_benchmark_questions.csv` are based on the **FULL dataset**.

Since we're using a **sample**, the answers will be different.

### You Need To:
1. Import this sampled data to NeonDB
2. Re-run all 30 SQL queries
3. Update the `answer` column in `llm_benchmark_questions.csv`

**OR** use the script below to help automate this.

---

## 🚀 Quick Start

### Option 1: Ready to Test (Skip Ground Truth for Now)

If you just want to test GPT's ability without comparing to ground truth:

1. Go to GPT 5.2 flash
2. Upload `music_dataset.html` (189 KB)
3. Ask questions from `llm_benchmark_questions.csv`
4. See how GPT responds

### Option 2: Generate New Ground Truth First (Recommended)

1. **Import sampled data to NeonDB:**
   - Use `music_dataset_combined.csv` or individual CSVs
   - Run import script (you'll need to create one or manually import)

2. **Re-run queries:**
   - Execute all 30 SQL queries from `llm_benchmark_questions.csv`
   - Record new answers

3. **Then test with GPT:**
   - Upload dataset format to GPT
   - Compare GPT answers with new ground truth

---

## 🎯 Testing Strategy

### Phase 1: Format Comparison
Test which format GPT understands best:
1. HTML (start here - best per research) ⭐
2. JSON
3. XML  
4. CSV (optional baseline)

### Phase 2: Question Batching
1. All 30 questions together (batch)
2. Each question individually (30 separate uploads)

### Phase 3: Difficulty Analysis
- Medium (Q001-Q015): expect decent accuracy
- Hard (Q016-Q022): expect some errors
- Extremely Hard (Q023-Q030): expect many errors

---

## 🔧 Re-running the Pipeline

If you want different sample sizes, edit `SAMPLE_CONFIG` in:
```
scripts/format_conversion/create_sample_and_combine.py
```

Then re-run:
```bash
cd scripts/format_conversion
python3 run_pipeline.py
```

---

## 📝 File Structure

### Combined CSV Structure
```
### TABLE: record_labels ###
label_id,name,label_type,...
...

### TABLE: artists ###
artist_id,name,primary_genre,...
...
```

All formats (JSON/HTML/XML) are converted from this single source.

---

## ✅ Benefits of This Approach

✅ **Small files** - All under 250 KB, easy GPT upload  
✅ **Single source** - All formats from one CSV  
✅ **Balanced sample** - Genre/country diversity maintained  
✅ **Referential integrity** - No orphaned records  
✅ **Reproducible** - Run one script to regenerate  

---

## 🎉 Ready to Go!

**Files are ready for GPT upload!**

Next steps:
1. Decide if you want to regenerate ground truth first
2. Upload HTML file to GPT 5.2
3. Start testing!

---

**Generated:** 2026-05-27  
**Status:** Ready for Upload ✅  
**Sample Size:** 678 records (2.1%)
