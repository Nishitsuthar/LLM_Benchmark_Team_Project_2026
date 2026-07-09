# Sprint 4: Unified Hard Cases Benchmark

**Duration:** July 2026  
**Team:** 5 members  
**Status:** Planning Phase  
**Goal:** Create benchmark of LLM failure cases from Sprint 1-3

---

## 📁 Sprint 4 Documents

This directory contains complete Sprint 4 planning documentation:

### Planning Documents

1. **[SPRINT4_OBJECTIVES_DRAFT.md](SPRINT4_OBJECTIVES_DRAFT.md)** (MAIN DOCUMENT)
   - Complete Sprint 4 plan (comprehensive, ~30 pages)
   - Detailed objectives, methodology, and deliverables
   - Team structure and timeline
   - Success metrics and evaluation framework
   - Read this for full project understanding

2. **[TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md)** (TEAM REFERENCE)
   - Specific assignments for each of 5 team members
   - Week-by-week deliverables and milestones
   - Communication protocols and escalation paths
   - Individual contribution tracking
   - Use this to coordinate team work

3. **[LLM_SELECTION_DECISION.md](LLM_SELECTION_DECISION.md)** (TECHNICAL DECISION)
   - Detailed analysis of model options
   - Cost-benefit comparison
   - Recommended: Llama-3-8B, Nemotron-550B, GPT-4-Turbo
   - Alternative configurations if budget constrained
   - Use this for model selection meeting

4. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** (PROFESSOR MEETING)
   - One-page summary for professor meetings
   - Key stats, decisions, and questions
   - Elevator pitch and talking points
   - Use this for quick updates

---

## 🎯 Sprint 4 Summary

### What We're Building:
A **Unified Hard Cases Benchmark** of 100-150 Q&A pairs where LLMs consistently fail, extracted from Sprint 1, 2, and 3 results.

### Why This Matters:
- Previous sprints showed what works (80-90% success)
- Sprint 4 focuses on the remaining 10-20% that consistently fails
- Creates benchmark for evaluating future LLM improvements
- Documents failure patterns for research/academic use

### Approach:
- Extract ONLY consistently failing questions from previous sprints
- Test 3 diverse LLMs (small/large/proprietary)
- Use fixed, simple configurations (no optimization)
- Document failure patterns, don't try to solve them

---

## 📊 Benchmark Composition (100-150 Questions)

```
Category                        Questions    Source
────────────────────────────────────────────────────
Structured Data                 30-40        Sprint 2 failures
Financial Docs (TatHybrid)      20-30        Sprint 3 failures
Financial Docs (FinHybrid)      15-20        Sprint 3 failures
Multi-hop Reasoning             20-30        New curation
Edge Cases (optional)           10-20        New creation
────────────────────────────────────────────────────
TOTAL                           100-150
```

---

## 🤖 Selected LLMs (Pending Approval)

| Model | Parameters | Type | Cost | Rationale |
|-------|------------|------|------|-----------|
| Llama-3-8B-Instruct | 8B | Open | $6 | Small baseline |
| Nemotron-3-Ultra-550B | 550B | Open | $30 | Large open-source, Sprint 3 experience |
| GPT-4-Turbo | ~1T+ | Proprietary | $90 | Industry standard, UDA paper comparison |

**Total Budget:** ~$126

---

## 🔬 Evaluation Framework

### 3 Approaches (Fixed Configuration):
1. **Direct LLM** - Full context, no RAG
2. **Simple RAG** - TOP_K=10, CHUNK_SIZE=1500, all-MiniLM-L6-v2
3. **Long Context** - No chunking (only GPT-4/Gemini with 100K+ context)

### 2 Prompt Strategies:
1. **Zero-shot** - Direct instruction
2. **Chain-of-Thought** - Step-by-step reasoning

### Evaluation Metrics:
- **F1 Score** - Token overlap (NqText, FetaTab, PaperText)
- **Exact Match** - Binary correctness (FinHybrid)
- **Numeracy F1** - Number-aware F1 (TatHybrid)
- **Empty Rate** - % questions with no answer

---

## 📅 Timeline (4 Weeks)

| Week | Dates | Focus | Key Deliverable |
|------|-------|-------|-----------------|
| 1 | Jul 1-7 | Dataset Extraction | CSV files with hard cases |
| 2 | Jul 8-14 | Framework Setup | Working benchmark system |
| 3 | Jul 15-21 | LLM Evaluation | Result CSVs (all models) |
| 4 | Jul 22-28 | Analysis & Docs | Final report + presentation |

---

## 👥 Team Structure

| Member | Role | Questions | Hours |
|--------|------|-----------|-------|
| Nishit Suthar | Lead + Structured Data | 30-40 | 15-20h |
| Member 2 | TatHybrid Extraction | 20-30 | 12-15h |
| Member 3 | FinHybrid Extraction | 15-20 | 12-15h |
| Member 4 | Multi-hop Reasoning | 20-30 | 12-15h |
| Member 5 | Edge Cases + QA | 10-20 | 10-12h |

**Total Team Effort:** 60-75 hours across 5 members

---

## 📋 Next Steps

### Immediate Actions (This Week):
- [ ] **Team Meeting:** Schedule for July 1, 2 PM
- [ ] **Read Documents:** All members review SPRINT4_OBJECTIVES_DRAFT.md
- [ ] **Model Selection:** Vote on LLM choices
- [ ] **Role Assignment:** Assign team members to roles 2-5
- [ ] **Professor Email:** Send Friday update with plan and budget request

### Week 1 Goals:
- [ ] Extract 10 sample questions per category
- [ ] Create shared question CSV template
- [ ] Set up GitHub repository
- [ ] Validate extraction criteria

---

## 📚 References

### Previous Work:
- [Sprint 1 README](../Sprint%201/README.md) - Data preparation
- [Sprint 2 README](../Sprint%202/README.md) - Format comparison
- [Sprint 3 README](../Sprint%203/README.md) - RAG optimization
- [Sprint 3 Critical Findings](../Sprint%203/UDA-Benchmark/CRITICAL_FINDINGS_REPORT.md) - Quality degradation analysis

### Key Insights to Apply:
- Sprint 2: 20% failed even in individual mode → Extract these
- Sprint 3 Phase 1: Matched GPT-4 (43.5% on TatHybrid)
- Sprint 3 Phase 3C: Optimization degraded quality (43.5% → 37.8%)
- Lesson: More answers ≠ better answers

### External Resources:
- UDA Paper: https://arxiv.org/pdf/2406.15187
- UDA GitHub: https://github.com/qinchuanhui/UDA-Benchmark
- TatQA Paper: https://arxiv.org/abs/2109.07323
- FinQA Paper: https://arxiv.org/abs/2109.00122

---

## ❓ Open Questions (For Team Discussion)

### Model Selection:
- [ ] Approve Llama-3-8B, Nemotron-550B, GPT-4-Turbo?
- [ ] Budget: Is $125 acceptable?
- [ ] Alternative: Replace GPT-4 with Gemini-1.5-Pro ($96 total)?
- [ ] Contact Aleph Alpha for free tokens?

### Scope:
- [ ] Target: 100 questions or 150 questions?
- [ ] Include Sprint 2 failures (20% of 20 = 4 questions) or only Sprint 3?
- [ ] Create edge cases (Member 5) or focus only on real failures?

### Technical:
- [ ] Question CSV format: Which columns required?
- [ ] Long Context: Test on all 3 models or only GPT-4?
- [ ] Code generation: Include as separate experiment?

### Deliverables:
- [ ] Final benchmark format: CSV? JSON? Hugging Face dataset?
- [ ] Open-source after completion?
- [ ] Publication target: Conference? Workshop? arXiv?

---

## 📞 Contact & Communication

### Team Meetings:
- **When:** Every Monday, 2-3 PM
- **Where:** [To be decided]
- **Format:** Rotating facilitator, shared agenda

### Professor Updates:
- **When:** Every Friday by 5 PM
- **Format:** Email with bullet points (5-10 items)
- **Subject:** "Sprint 4 Progress - Week X"

### Daily Communication:
- **Platform:** [Slack/WhatsApp/Discord - To be decided]
- **Purpose:** Quick updates, blockers, questions

### Repository:
- **GitHub:** [URL to be created]
- **Structure:**
  ```
  sprint-4/
  ├── benchmark/          (Questions & data)
  ├── framework/          (Evaluation code)
  ├── results/            (LLM outputs)
  ├── analysis/           (Reports & visualizations)
  └── docs/               (Documentation)
  ```

---

## 🎯 Success Criteria

### What Success Looks Like:
✅ 100-150 hard case questions extracted and validated  
✅ 3 LLMs tested with fixed, simple configurations  
✅ Clear failure patterns documented  
✅ Budget stays under $150  
✅ Reproducible framework for future use  
✅ All 5 team members contribute roughly equally  
✅ Final report and presentation ready for delivery

### What Success Does NOT Require:
❌ Solving all the hard cases (they're supposed to be hard!)  
❌ Optimizing systems (professor explicitly said NO)  
❌ Testing 10 different models (3 is enough)  
❌ Perfect accuracy scores (document failures)  
❌ Advanced RAG techniques (keep it simple)

---

## 🚀 Getting Started

### For Team Members:
1. Read [SPRINT4_OBJECTIVES_DRAFT.md](SPRINT4_OBJECTIVES_DRAFT.md) fully
2. Review [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md) for your role
3. Check [LLM_SELECTION_DECISION.md](LLM_SELECTION_DECISION.md) for technical details
4. Attend Monday team meeting to finalize assignments

### For Professor Review:
1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for high-level overview
2. Check budget and timeline feasibility
3. Provide feedback on model selection
4. Approve or request changes to scope

### For External Readers:
1. See Sprint 1-3 README files for background
2. Review [SPRINT4_OBJECTIVES_DRAFT.md](SPRINT4_OBJECTIVES_DRAFT.md) for methodology
3. Check back after July 31 for final results

---

## 📊 Expected Deliverables (End of Sprint 4)

1. **Benchmark Dataset**
   - `benchmark_v1/` directory with 100-150 Q&A pairs
   - CSV format with ground truth and metadata
   - Source documents (PDFs, CSVs)

2. **Evaluation Framework**
   - Python scripts for 3 approaches (Direct, RAG, Long Context)
   - Automated evaluation pipeline (F1, EM, Numeracy F1)
   - Cost tracking and logging

3. **Results**
   - Result CSVs for all LLM evaluations
   - Per-question scores and failure classifications
   - Summary comparison tables

4. **Analysis**
   - `SPRINT4_ANALYSIS_REPORT.md` (15-20 pages)
   - Failure taxonomy and patterns
   - Cost-benefit analysis
   - Recommendations for future work

5. **Presentation**
   - 15-20 slides (bullet points, visuals)
   - Follows professor's feedback (less text, more charts)
   - Ready for team presentation

6. **Documentation**
   - README for running the benchmark
   - Installation and setup guide
   - Reproducibility instructions

---

## 💡 Key Lessons from Sprint 3 (To Apply)

### What Worked:
✅ Systematic phase-by-phase approach  
✅ Comprehensive documentation  
✅ Per-question evaluation (not just aggregates)  
✅ Cost tracking  
✅ Critical thinking about results

### What to Improve:
⚠️ Don't optimize when professor wants benchmarking  
⚠️ Start with failure analysis, not success metrics  
⚠️ Simpler is better (fixed config prevents scope creep)  
⚠️ More answers ≠ better answers (measure quality!)

### Critical Discovery:
> "What about the actual results which matters more?" - You, July 1 2026

This question saved Sprint 3 from claiming success based only on empty response reduction. Sprint 4 applies this lesson: measure quality first.

---

## 📝 Version History

- **v1.0** (July 2, 2026) - Initial planning documents created
  - SPRINT4_OBJECTIVES_DRAFT.md - Full plan
  - TEAM_ASSIGNMENTS.md - Team structure
  - LLM_SELECTION_DECISION.md - Model analysis
  - QUICK_REFERENCE.md - Summary card
  - README.md - This file

**Status:** Draft pending team and professor approval  
**Next Update:** After team meeting and professor feedback

---

## 📧 Questions or Feedback?

**Team Lead:** Nishit Suthar (I772947)  
**Project:** LLM Benchmark Team Project 2026  
**Course:** [Course Name/Number]  
**Institution:** [University Name]

For questions about Sprint 4 planning, contact the team lead or bring to Monday team meeting.

---

**Let's build a benchmark that shows what LLMs can't do yet! 🚀**
