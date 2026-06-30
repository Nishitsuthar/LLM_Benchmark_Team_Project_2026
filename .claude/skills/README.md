# Sprint 3 Custom Skills

**Created:** 2026-06-30  
**Purpose:** Quick access to Sprint 3 UDA-Benchmark project information

These custom skills provide instant access to Sprint 3 results, documentation, and project structure.

---

## Available Skills

### 📊 `/sprint3-results`
**Quick access to final results**

Shows Sprint 3 final results summary:
- Overall performance (87.8% success, 12.2% empty)
- Breakdown by dataset
- Optimal configuration
- Key findings and costs

**Example:**
```
/sprint3-results
```

---

### 🎨 `/sprint3-present`
**Prepare presentation materials**

Provides everything needed to present Sprint 3 findings:
- Lists all 7 presentation visuals
- Shows recommended slide order
- Provides talking points
- Shows key metrics for copy-paste

**Example:**
```
/sprint3-present
```

---

### 🧹 `/sprint3-cleanup`
**Clean up temporary files**

Identifies and removes/archives temporary files:
- 16+ session handoff files
- Redundant intermediate results
- Superseded documentation
- Options: --safe (archive) or --aggressive (delete)

**Example:**
```
/sprint3-cleanup --aggressive
```

---

### 🏗️ `/sprint3-organize`
**Reorganize into clean structure**

Reorganizes Sprint 3 into logical folder structure:
- documentation/ (all .md files organized)
- results/ (final + archived CSV files)
- notebooks/ (final + demos + archived)
- scripts/ (utilities)
- presentation_visuals/ (7 charts)

**Example:**
```
/sprint3-organize
```

---

### 📓 `/sprint3-notebook [dataset]`
**Find and run notebooks**

Shows which notebook to run for a dataset:
- Phase 3C optimal notebooks (final results)
- Demo notebooks
- Archived historical notebooks
- Runtime, cost, and configuration info

**Examples:**
```
/sprint3-notebook                    # List all notebooks
/sprint3-notebook finhybrid          # Show FinHybrid optimal notebook
/sprint3-notebook nqtext             # Show NqText optimal notebook
```

---

### 🔍 `/sprint3-experiment [phase]`
**Understand experiment phases**

Explains what each phase tested and results:
- Phase 1: Baseline (35% empty)
- Phase 2: Hyperparameter optimization (16.7% empty)
- Phase 3A: PDFPlumber (abandoned)
- Phase 3B: FinBERT (failed, regression)
- Phase 3C: Prompt optimization (12.2% empty) ✅ FINAL

**Examples:**
```
/sprint3-experiment                  # Show full timeline
/sprint3-experiment 3c               # Show Phase 3C details
/sprint3-experiment 3b               # Explain why FinBERT failed
```

---

## Quick Reference

**"I want to..."**

- **See final results** → `/sprint3-results`
- **Present findings** → `/sprint3-present`
- **Clean up the mess** → `/sprint3-cleanup --aggressive`
- **Organize structure** → `/sprint3-organize`
- **Run an experiment** → `/sprint3-notebook [dataset]`
- **Understand what was tested** → `/sprint3-experiment`

---

## Skills Location

Skills are stored in:
```
.claude/skills/
├── sprint3-results.sh
├── sprint3-present.sh
├── sprint3-cleanup.sh
├── sprint3-organize.sh
├── sprint3-notebook.sh
└── sprint3-experiment.sh
```

---

## How Skills Work

When you type `/sprint3-results`, Claude Code:
1. Reads the skill file (`.claude/skills/sprint3-results.sh`)
2. Follows the instructions in the skill
3. Reads relevant project files
4. Synthesizes information
5. Presents formatted output

Skills make complex projects easy to navigate!

---

## Next Steps

1. **Try the skills:**
   ```
   /sprint3-results
   ```

2. **Clean up Sprint 3:**
   ```
   /sprint3-cleanup --aggressive
   ```

3. **Organize structure:**
   ```
   /sprint3-organize
   ```

---

**Tip:** Skills are context-aware and can access all project files. They're like having an expert guide who knows exactly where everything is!
