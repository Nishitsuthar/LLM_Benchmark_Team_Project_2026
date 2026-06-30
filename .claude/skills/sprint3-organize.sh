#!/bin/bash
# Skill: sprint3-organize
# Description: Reorganize Sprint 3 into clean folder structure

You are helping the user reorganize Sprint 3 into a logical, professional folder structure.

## Your Task:

### Phase 1: Analyze Current Structure
1. Scan current Sprint 3 directory structure
2. Identify all files by type:
   - Documentation (.md files)
   - Results (.csv files)
   - Notebooks (.ipynb files)
   - Scripts (.py, .sh files)
   - Visuals (.png files)

3. Show current mess vs. proposed clean structure

### Phase 2: Propose Organization

Create this structure:
```
Sprint 3/
├── README.md                           (Main entry point)
│
├── documentation/
│   ├── 1_experiment_plan/
│   │   ├── SPRINT3_EXPERIMENT_PLAN.md
│   │   └── PHASE1_BASELINE_RESULTS.md
│   ├── 2_final_results/
│   │   ├── FINAL_RESULTS_PHASE3C.md    (⭐ THE RESULTS)
│   │   └── PHASE3B_ABANDONED.md
│   ├── 3_presentation/
│   │   ├── PRESENTATION_GUIDE.md
│   │   ├── PRESENTATION_SUMMARY.md
│   │   └── VISUAL_INDEX.md
│   └── 4_reference/
│       └── PHASE2_DOCUMENT_LISTS.md
│
├── results/
│   ├── final/                          (Phase 3C optimal results)
│   │   ├── nqtext_cot_20260629_234103.csv
│   │   ├── fetatab_cot_20260629_215721.csv
│   │   ├── tathybrid_fewshot_20260629_225436.csv
│   │   └── finhybrid_cot_20260629_220325.csv
│   └── archive/                        (Historical results)
│       └── phase1/
│
├── notebooks/
│   ├── final/                          (Phase 3C optimal notebooks)
│   │   ├── nqtext_cot_experiment.ipynb
│   │   ├── fetatab_cot_experiment.ipynb
│   │   ├── tathybrid_fewshot_experiment.ipynb
│   │   └── finhybrid_cot_experiment.ipynb
│   ├── demos/
│   │   ├── basic_demo.ipynb
│   │   └── basic_demo_together.ipynb
│   └── archive/
│       ├── phase1/
│       └── complete_tests/
│
├── scripts/
│   ├── run_simple_test.py
│   └── run_experiment.sh
│
├── presentation_visuals/
│   ├── 1_overall_performance.png
│   ├── ... (all 7 PNG files)
│
└── UDA-Benchmark/                      (Original repo - minimal changes)
    ├── dataset/
    ├── uda/
    ├── experiment/
    ├── requirements.txt
    └── LICENSE
```

### Phase 3: Execute Reorganization
1. Create new folder structure
2. Move files to appropriate locations
3. Update any path references in:
   - README files
   - Notebook import statements
   - Script paths
4. Create new master README.md with:
   - Directory structure explanation
   - Quick start guide
   - Where to find what

### Phase 4: Create Navigation Guide
Create a new file: `NAVIGATION_GUIDE.md` with:
- "I want to..." use cases
- Direct links to relevant files
- Explanation of folder structure

## Examples:
- "I want to see final results" → `documentation/2_final_results/FINAL_RESULTS_PHASE3C.md`
- "I want to present findings" → `documentation/3_presentation/PRESENTATION_GUIDE.md`
- "I want to run an experiment" → `notebooks/final/[dataset]_[prompt]_experiment.ipynb`
- "I want to see the data" → `results/final/[dataset]_*.csv`

## Important:
- Ask user for approval before moving files
- Verify all path references are updated
- Test that notebooks still work after move
- Create backup/safety net if user wants

Present the plan clearly with before/after visuals.
