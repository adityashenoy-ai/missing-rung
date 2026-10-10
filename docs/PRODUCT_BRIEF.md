# The Missing Rung: product brief

*Owner: Aditya Shenoy · Status: v1 in build · Last updated: 10 Oct 2026*

## 1. Problem

Most "Will AI take my job?" tools score a whole occupation. A career isn't one block of work, though. It's a ladder, and people learn the senior rungs by doing the junior ones.

If AI mostly absorbs the routine tasks juniors used to learn on, three things can be true at once: the occupation looks safe, seniors become more productive, and new entrants have nowhere to start. Current exposure scores can't show this, because they average over the whole ladder.

**Problem statement:** Early-career people and the managers who hire them can't see *which specific rungs* of a role AI is already doing on its own. So they can't decide what to learn, or how to redesign entry-level work, on evidence rather than headlines.

## 2. Who it's for

| Segment | Situation | Job to be done | What they leave with |
|---|---|---|---|
| **Primary: students and freshers** (India first: IT services, consulting, analytics) | Campus hiring is tight, and AI advice is generic | "Tell me which parts of the job I'm aiming for are being handed to AI, so I can build skills that still compound." | A role ladder, the at-risk rungs, and a 90-day proof-of-skill project |
| **Secondary: hiring and engineering managers, L&D, HR** | Entry-level roles still designed for 2019 workflows | "Help me redesign junior roles so people still learn, even when AI does the grunt work." | A rung-by-rung redesign checklist for one role |
| **Tertiary: journalists and researchers** | Need a citable, transparent cut of the data | "Give me a sourced, reproducible number." | Open CSV, method notes, and code |

## 3. Hypothesis (the data is allowed to say no)

> **H1.** Within the same role, tasks typical of junior work show a higher *automation* share of Claude usage (the user hands the task over) than tasks typical of senior work, which skew toward *augmentation* (the user works through it with AI).

- **Supported if** the junior-tier median automation share is clearly above the senior-tier median in most of the roles covered.
- **Not supported if** the gap is small, reversed, or appears in only a few roles. In that case the site reports that result, and the story changes to "AI is reshaping every rung, not only the bottom one."

This is written down *before* looking at the numbers on purpose. A portfolio piece that only ever confirms its own premise isn't evidence of product judgment.

## 4. What v1 is, and what it isn't

**In scope**
- About 12 roles chosen for early-career relevance in India, each mapped to a U.S. O*NET occupation (the dataset's task taxonomy).
- Each of the role's O*NET tasks tagged Junior, Mid or Senior using a published rubric. The tags are in a CSV that anyone can dispute.
- For each task: share of Claude usage, automation vs augmentation split, and AI autonomy, all taken from the Anthropic Economic Index (CC-BY) and labelled with their source.
- A **broken rung** flag: a junior task where automation is the dominant use pattern (rule in METHODOLOGY.md).
- Two guidance views: *For you* (early career) and *For your team* (managers).

**Not in scope**
- Predicting job losses or salary effects. The data shows how people *use Claude*, not what employers do.
- Measuring the whole economy. Claude users aren't representative of all workers, and the site says so at the top, not in a footnote.
- Personalised advice or anything that collects user data. It's a static site with no tracking beyond page analytics.

## 5. Key product decisions

| Decision | Options considered | Choice and why |
|---|---|---|
| Unit of analysis | Occupation · task · skill | **Task.** It's the finest grain the source publishes and the only level where "junior vs senior" means something. |
| Seniority labels | Model-only · expert survey · rubric plus human review | **Rubric plus review, published as CSV.** It can be audited and disputed. A model-only label would be a black box, and a survey is out of scope for v1. |
| Primary metric | Usage share · automation share · AI autonomy | **Automation share** as the headline, with autonomy as a second signal. Usage share alone shows *popularity*, not *displacement*. |
| Small samples | Show everything · hide · show with a warning | **Show only cells the source published, and grey out low-usage tasks.** The source already withholds cells below its privacy thresholds. A missing value means "not published", never zero. |
| Data source | Claude.ai only · API only · both | **Both, shown side by side.** API traffic is where businesses automate tasks at scale. Claude.ai shows individual workers. When they disagree, that's a finding, not noise. |
| Hosting | App with a backend · static | **Static GitHub Pages plus a reproducible Python build.** No running costs, and anyone can rebuild the numbers. |

## 6. Success metrics

| Type | Metric | v1 target (first 30 days) |
|---|---|---|
| North star | Visitors who open a role **and** reach its "what to do" section | ≥ 35% of role views |
| Reach | Unique visitors · LinkedIn and X shares | 3k visitors · 50 shares |
| Trust | Disputes or corrections filed on the tagging CSV (GitHub issues) | ≥ 5. Engagement with the method is the goal, not zero issues |
| Usefulness | Managers downloading or printing the redesign checklist | ≥ 100 |
| Guardrail | Corrections to a factual claim | 0 left unfixed for more than 48 hours |

## 7. Risks

| Risk | Mitigation |
|---|---|
| Readers treat Claude usage as the whole labour market | A "What this data is" banner at the top of every role, plus the source on every number |
| My seniority tags are wrong or biased | Public rubric, one-line rationale per tag, CSV open to pull requests |
| Using U.S. O*NET occupations for Indian roles | Name the mapping explicitly ("closest O*NET occupation") and avoid India-specific claims the data can't support |
| Results go stale | The build script pins the release date. Re-running it on the next release updates the site |
| The hypothesis fails | Publish that result anyway (see §3) |

## 8. Roadmap

- **v1 (this build):** about 12 roles, static site, method notes, open data.
- **v1.1:** compare releases over time (did a rung break between 2025 and 2026?), using earlier releases of the same dataset.
- **v2:** "Bring your own role": paste a job description, match it to O*NET tasks and see its ladder.

## 9. Results and decisions made during the build

**H1 is supported.** The median automation share is 60% for junior tasks, 47% for mid and 39% for senior. Junior is above mid in 10 of 12 roles (p < 0.001). The result survives each month on its own, a stricter sample-size cutoff, usage weighting, and a keyword tagger that uses no judgment. Details are in METHODOLOGY.md.

**What the data changed:**

| Discovery | Decision |
|---|---|
| About 95% of API usage is automation on almost every task, so it can't tell rungs apart | API data is shown only as "built into apps" (share of API usage), never as status |
| Many 95–100% automation values sit on tasks with near-zero usage | Added a thin-data rule: a task needs at least 0.01% of usage to count toward any headline or broken flag |
| The O*NET file bundled with the dataset is an older version (2,603 of 3,307 IDs matched) | Switched to O*NET 31.0: 3,304 of 3,307 matched, with identical wording |
| India's data is published per task only as a usage share, and India over-indexes about 1.2× evenly across all rungs | The India view is a per-task comparison, not a claim about juniors |
| The check I set in advance (years of education) did not rank my tiers | Published it as "did not confirm" on the site instead of dropping it |
| Senior tasks seldom appear in Claude usage (29% vs 59%) | Made it a headline finding and said the junior vs senior gap rests on fewer tasks |
| Recruiter and customer support have fewer than 6 tasks with data | Dropped both, and named them on the site with the reason |

**Open items before launch:** the author reviews the 402 seniority tags (drafted by AI from the rubric), and a peer reads the role guidance.

## Sources
- Anthropic Economic Index dataset (CC-BY): https://huggingface.co/datasets/Anthropic/EconomicIndex
- Anthropic Economic Index reports: https://www.anthropic.com/economic-index
- O*NET task statements (U.S. Department of Labor), as bundled in the dataset's 2025-02-10 release
- Stanford Digital Economy Lab, early-career employment update (Aug 2026): https://digitaleconomy.stanford.edu/news/canariesaug26/
