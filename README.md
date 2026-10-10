# The Missing Rung

**Which entry-level tasks is AI taking over?** This project maps real AI usage data onto the career ladders of 12 early-career roles. It shows which rungs juniors used to learn on are now mostly handed to AI, and what to do about it.

**Live:** https://adityashenoy-ai.github.io/missing-rung/

## The finding

Across 12 roles, junior tasks are handed over to AI far more often than senior ones. The figures are the median share of Claude.ai conversations where the user hands the whole task over (Anthropic Economic Index, Apr–May 2026):

| Rung | Median automation share | Tasks |
|---|---|---|
| Senior | 39% | 12 |
| Mid | 47% | 52 |
| Junior | **60%** | 66 |

- Junior tasks are more automated than mid-level ones in **10 of 12 roles** (p < 0.001).
- **25 junior tasks are "broken rungs"**, with 65% or more of their conversations handing the task over. They're concentrated in software, QA, IT support and business analysis.
- **The exceptions:** no junior rung is broken yet for financial analysts or digital marketers.
- Only 29% of senior tasks appear in Claude usage at all. Senior work is mostly experience, relationships and decisions, and it barely shows up.

The method, the robustness checks, and the one check that *didn't* confirm are in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## Why this exists (the product view)

Exposure scores rate whole occupations, but careers are ladders. If AI absorbs the bottom rungs, an occupation can look safe while new entrants have nowhere to start. The [product brief](docs/PRODUCT_BRIEF.md) sets out the users (freshers in India first, then managers), a hypothesis written before looking at the data, success metrics, and a decision log.

## Repo map

```
docs/PRODUCT_BRIEF.md   problem, users, hypothesis, metrics, decisions, results
docs/METHODOLOGY.md     sources, pipeline, tagging rubric, checks, limits
scripts/01–06           reproducible pipeline (Python 3 + pandas)
scripts/roles.py        role → O*NET occupation mapping
scripts/tags_v1.py      junior/mid/senior tag + reason for every task (dispute via issues)
scripts/guidance.py     editorial guidance per role (author's judgment, labelled on site)
data/ladders.csv        the joined dataset: every task, tag, status and metric
data/robustness.json    every check behind the headline
site/data.json          what the page reads
index.html              the page (generated from site/page.html)
```

## Reproduce

1. Download into `data/raw/` (not committed, because the files are large):
   - `aei_claude_ai_2026-06-26.csv` and `aei_1p_api_2026-06-26.csv` from the [Anthropic Economic Index dataset](https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2026_06_26/data)
   - `task_statements.csv` from [O*NET 31.0](https://www.onetcenter.org/dl_files/database/db_31_0_csv/task_statements.csv), saved as `onet_31_0_task_statements.csv`
2. Run `pip install pandas numpy`, then `for s in scripts/0*.py; do python3 $s; done`

## Sources and licences

- Anthropic Economic Index, release 2026-06-26 (CC-BY). Report: [Anthropic Economic Index report: Cadences](https://www.anthropic.com/research/economic-index-june-2026-report)
- O*NET 31.0 Database, U.S. Department of Labor/Employment and Training Administration (CC-BY 4.0)

This is an independent analysis. It is not affiliated with or endorsed by Anthropic or the U.S. Department of Labor.
