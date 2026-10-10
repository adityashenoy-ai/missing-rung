"""Step 4: robustness checks for H1, written to data/robustness.json."""
import json, pathlib, re
import pandas as pd, numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = pd.read_csv(ROOT/"data/ladders.csv", dtype={"task_id": str})
L = pd.read_csv(ROOT/"data/interim/aei_tasks_long.csv", dtype={"task_id": str})
L["task_id"] = L.task_id.str.replace(r"\.0$", "", regex=True)
allc = D[(D.tier!="X") & D.automation_pct.notna()]
cov = allc[allc.status != "thin"]      # headline set: tasks with >=0.01% of Claude.ai usage
out = {}
def tier_meds(df, col="tier", val="automation_pct"):
    return {k: round(float(v),1) for k,v in df.groupby(col)[val].median().items()}
out["main"] = tier_meds(cov)
out["all_tasks_incl_thin"] = tier_meds(allc)
out["usage_ge_0.02"] = tier_meds(allc[allc.usage_pct>=0.02])
# 1. each month separately
for m in ["2026-04-01","2026-05-01"]:
    a = L[(L.source=="claude_ai")&(L.date_start==m)&(L.metric_id=="collaboration_bucket_automation_pct")].set_index("task_id").value
    x = D[(D.tier!="X")&(D.status!="thin")].assign(a=lambda d: d.task_id.map(a)).dropna(subset=["a"])
    out[f"month_{m[:7]}"] = tier_meds(x, val="a")
# 2. mechanical keyword tagger, independent of my judgement
SEN = r"^(supervise|direct|assign|approve|negotiate|recruit|hire|train subordinates|manage|establish|determine (system )?performance standards|develop or specify standards|recommend (investments|purchase)|advise|represent|initiate, review, or approve|propose, review, or approve|select|evaluate or recommend|develop and manage|coordinate recruitment)"
JUN = r"^(enter|record|document|compile|maintain|update|prepare|process|code|operate|check|match|transfer|test|perform .*tests|conduct trial|correct|write|key|install|answer|respond|collect|draw|back up|renew|create graphs|clean|reconcile|debit|classify|calculate|receive|organize|edit)"
def mech(t):
    t = t.lower()
    return "S" if re.search(SEN, t) else "J" if re.search(JUN, t) else "M"
x = cov.assign(mtier=cov.task.map(mech))
out["keyword_tagger"] = tier_meds(x, col="mtier")
out["keyword_tagger_agreement_pct"] = round(float((x.mtier==x.tier).mean()*100),1)
# 3. usage-weighted means
out["usage_weighted_mean"] = {k: round(float(np.average(g.automation_pct, weights=g.usage_pct.clip(lower=0.005))),1) for k,g in cov.groupby("tier")}
# 4. coverage: share of tasks in each tier that appear in Claude.ai usage at all
base = D[D.tier!="X"]
out["coverage_pct"] = {k: round(float(g.automation_pct.notna().mean()*100),1) for k,g in base.groupby("tier")}
out["coverage_ge_0.01_pct"] = {k: round(float((g.status.notna() & (g.status!="thin")).mean()*100),1) for k,g in base.groupby("tier")}
# permutation test (within-role label shuffle), J vs M and J vs S
rng = np.random.default_rng(7)
for other in ["M","S"]:
    js = cov[cov.tier.isin(["J",other])].copy()
    obs = js[js.tier=="J"].automation_pct.median() - js[js.tier==other].automation_pct.median()
    null = []
    for _ in range(5000):
        perm = js.groupby("role").tier.transform(lambda s: rng.permutation(s.values))
        null.append(js[perm=="J"].automation_pct.median() - js[perm==other].automation_pct.median())
    out[f"perm_J_vs_{other}"] = {"gap_pts": round(float(obs),1), "p_one_sided": round(float((np.array(null) >= obs).mean()),4)}
# India: India's share of its own usage vs global share, by tier
ii = cov.dropna(subset=["india_usage_pct"])
out["india_index_by_tier"] = {k: round(float(g.india_usage_pct.sum()/g.usage_pct.sum()),2) for k,g in ii.groupby("tier")}
out["n_tasks"] = {k: int(v) for k,v in cov.tier.value_counts().items()}
# 5. junior vs mid per role
t = cov.groupby(["role","tier"]).automation_pct.median().unstack()
out["roles_J_gt_S"] = f"{int((t.J>t.S).sum())} of {int((t.J-t.S).notna().sum())}"
out["roles_J_gt_M"] = f"{int((t.J>t.M).sum())} of {int((t.J-t.M).notna().sum())}"
# 6. education-years validation (pre-registered; reported whatever the result)
out["edu_years_median"] = tier_meds(cov, val="edu_years")
out["autonomy_median"] = tier_meds(cov, val="autonomy")
json.dump(out, open(ROOT/"data/robustness.json","w"), indent=1); print(json.dumps(out, indent=1))
