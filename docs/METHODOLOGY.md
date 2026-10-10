# Method

Every number on the site comes from two public sources and the scripts in `scripts/`. Nothing is estimated by hand.

## Sources

| Source | What it gives | Licence |
|---|---|---|
| [Anthropic Economic Index](https://huggingface.co/datasets/Anthropic/EconomicIndex), release 2026-06-26: `aei_claude_ai_2026-06-26.csv`, `aei_1p_api_2026-06-26.csv` | Claude usage per O*NET task for Apr and May 2026. Includes share of usage, automation vs augmentation, collaboration patterns, AI autonomy, time estimates, and India's usage share | CC-BY |
| [O*NET 31.0 Task Statements](https://www.onetcenter.org/database.html), U.S. Department of Labor/ETA | Task ID → occupation (O*NET-SOC code and title) | CC-BY 4.0 |

**Why O*NET 31.0 and not the task file bundled with the dataset?** The task list in the dataset's 2025 releases is an older O*NET version. It matched only 2,603 of the 3,307 task IDs in the 2026 data, and 9% of those matches had different wording. O*NET 31.0 matches 3,304 of 3,307 IDs, and every match has identical wording. `scripts/02_task_metrics.py` keeps the join auditable.

## Pipeline

| Step | Script | Output |
|---|---|---|
| 1 | `01_extract.py` | Keeps only task-level (`category_name = onet`, `hierarchy_level = 0`) rows: global metrics plus India's `pct` → `data/interim/aei_tasks_long.csv` |
| 2 | `02_task_metrics.py` | One row per O*NET task. Averages Apr and May where both are published (they correlate at 0.92 for automation share) → `data/interim/task_metrics.csv` |
| 3 | `03_build.py` | Joins roles and seniority tags, assigns status → `data/ladders.csv` |
| 4 | `04_robustness.py` | Checks the hypothesis several ways → `data/robustness.json` |
| 5 | `05_site_data.py` | → `site/data.json`, the only file the page reads |
| 6 | `06_wrap_page.py` | Wraps `site/page.html` into `index.html` |

Re-running all six steps on a future release refreshes the site.

## Roles

12 roles named the way early-career people in India search for jobs, each mapped to the closest O*NET occupation(s). The mapping is in `scripts/roles.py`. Two roles were dropped for thin data: Recruiter/HR (only 5 of 26 tasks published) and Customer support (fewer than 5).

## Seniority tags

Every task in the 12 roles (402 in total) is tagged from its wording only, **before looking at any usage numbers**. The tags are in `scripts/tags_v1.py`, and each has a reason code.

- **J (Junior rung):** executes defined work. It produces, fixes, tests, documents, enters or collects data, answers standard queries, and follows procedures.
- **M (Mid rung):** owns a piece of work. It analyses, designs within constraints, diagnoses non-routine problems, recommends, and coordinates.
- **S (Senior rung):** sets direction or standards, decides or approves, owns budgets, negotiates, supervises, hires, mentors, and advises clients on high-stakes matters.
- **X (Excluded):** not representative of the role as practised in India, such as visiting beta-test sites or green-finance specialisation. These 8 tasks stay in the data but don't appear on the ladder.

The first pass of tags was drafted by Claude (AI) from this rubric and is open to review and dispute. Please file disagreements as GitHub issues, citing the task ID.

## Metrics and status

- **Automation share** is `collaboration_bucket_automation_pct` from Claude.ai: the share of a task's conversations where the user hands the task over (directive, or a feedback loop of fixing AI errors). The rest is augmentation: iterating together, validating, or learning.
- **Status:** *broken* when automation is 65% or more (roughly the top quarter of all 2,691 tasks published for May, where the 75th percentile is 64.3%); *cracking* at 50–65%; *holding* below 50%.
- **Thin data:** a task with less than 0.01% of Claude.ai usage (the published value rounds to 0.00) is flagged and left out of every headline number, because its percentages rest on few conversations.
- **API data** is not used for status. On almost every task about 95% of API usage is automation, because that is what a pipeline does. The site shows a task's share of API usage as "built into apps" instead.
- **India** uses the only India metric published per task, `pct` (the task's share of India's usage). It is compared with the global share as a ratio.

## Hypothesis and results (headline set: 130 tasks with enough data)

H1: within a role, junior tasks show a higher automation share than senior tasks.

| Check | Junior | Mid | Senior |
|---|---|---|---|
| Median automation share (headline) | 60.1% | 47.3% | 39.3% |
| April only / May only | 59.8 / 60.4 | 48.3 / 49.9 | 40.2 / 38.8 |
| Including thin-data tasks | 62.1 | 50.3 | 40.3 |
| Usage ≥ 0.02% only | 59.3 | 49.4 | 39.3 |
| Usage-weighted mean | 61.7 | 45.1 | 44.2 |
| Keyword tagger instead of my tags (66% agreement) | 59.0 | 51.9 | 39.3 |

- Junior > mid in **10 of 12** roles. The pooled gap is 12.8 points (p < 0.001, 5,000 within-role label shuffles).
- Junior > senior in **6 of 7** roles that have senior data. The gap is 20.8 points (p = 0.0004).
- **What didn't confirm:** the check I set in advance used the dataset's estimate of years of education a task needs, and it does not rank my tiers (13.7 / 13.9 / 13.0 years). That estimate measures schooling, not on-the-job experience, but the tags still rest on judgment.
- **Coverage gap:** only 29% of senior tasks appear in Claude usage at all, against 59% of junior tasks (17% vs 37% with enough data). Senior work is less often brought to Claude, which is itself part of the story.

## Limits

- Claude usage is not the labour market. It shows what people bring to one AI system, and they may bring it the tasks they find easiest to hand over.
- O*NET describes U.S. occupations, and Indian job titles bundle tasks differently.
- Two months of data. The site describes a pattern in how AI is used, not a trend over time.
