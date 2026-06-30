#!/bin/bash
# Skill: sprint3-cleanup
# Description: Clean up Sprint 3 temporary and redundant files
# Usage: /sprint3-cleanup [--aggressive|--safe]

You are helping the user clean up Sprint 3 directory by removing temporary session files and organizing the structure.

## Your Task:

### Phase 1: Analysis
1. Scan for temporary files in experiments/:
   - Files named: *READY_TO_RUN*.md, *START_HERE*.md, *FIXES_APPLIED*.md, *ISSUE_FIXED*.md
   - Files in: documentation/archived/ folders
   - Session handoff files: *HANDOFF*.md, *SESSION*.md

2. Identify redundant files:
   - Multiple result reports that are superseded by FINAL_RESULTS_PHASE3C.md
   - Duplicate guides/instructions
   - Empty README files

3. Create a cleanup report showing:
   - Files to delete (with rationale)
   - Files to archive (with destination)
   - Files to keep (essential)
   - Estimated space savings

### Phase 2: Execution (based on user approval)

**If user passed --safe or no argument:**
- Archive files to appropriate locations
- Create cleanup summary document
- Preserve all data, just reorganize

**If user passed --aggressive:**
- Delete temporary session files
- Delete redundant intermediate results
- Keep only: final results, presentation materials, essential docs
- Archive historical data

### Phase 3: Verification
- Show before/after structure
- List what was removed/archived
- Verify no essential files were touched
- Create CLEANUP_SUMMARY.md

## Files to ALWAYS Keep:
- Sprint 3/README.md
- Sprint 3/SPRINT3_EXPERIMENT_PLAN.md
- Sprint 3/PHASE1_BASELINE_RESULTS.md
- UDA-Benchmark/FINAL_RESULTS_PHASE3C.md
- UDA-Benchmark/PHASE3B_ABANDONED.md
- UDA-Benchmark/PRESENTATION_*.md
- UDA-Benchmark/VISUAL_INDEX.md
- All notebooks in experiments/.../3_prompts/notebooks/ (Phase 3C finals)
- All CSV results in experiments/.../3_prompts/results/ (Phase 3C finals)
- All presentation_visuals/*.png

## Files to DELETE (safe):
- experiments/**/READY_TO_RUN.md
- experiments/**/START_HERE.md
- experiments/**/FIXES_APPLIED.md
- experiments/**/QUICK_START.md
- experiments/**/ISSUE_FIXED.md
- experiments/**/REORGANIZATION_COMPLETE.md
- experiments/2_optimization/documentation/archived/*.md (all files)

## Files to REVIEW:
- Multiple PHASE3C_*.md files (keep only essential)
- Multiple optimization reports (consolidate or archive)
- Phase 3A pdfplumber results (already abandoned)

Present a plan to the user before executing any deletions.
