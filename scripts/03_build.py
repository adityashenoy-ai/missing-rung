"""Step 3: join seniority tags to task metrics, test H1, and write site data.
Every number written here comes from the Anthropic Economic Index release 2026-06-26 (CC-BY),
Apr–May 2026, global, joined to O*NET 31.0 task statements (CC-BY 4.0)."""
import json, pathlib, sys
import pandas as pd, numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from roles import ROLES, EXCLUDED
from tags_v1 import T

BROKEN, CRACKING = 65.0, 50.0   # automation-share thresholds (Claude.ai); see METHODOLOGY.md
LOW_USAGE = 0.01               # tasks below this share of Claude.ai usage (%) are flagged low-volume

M = pd.read_csv(ROOT/"data/interim/task_metrics.csv", dtype={"task_id": str})
C = "claude_ai__"; A = "1p_api__"
rows = []
for r in ROLES:
    for soc in r["onet"]:
        for _, x in M[M.onet_soc == soc].iterrows():
            tier, reason = T[x.task_id].split()
            auto = x.get(C+"collaboration_bucket_automation_pct")
            status = None
            if pd.notna(auto) and pd.notna(x.get(C+"pct")) and x.get(C+"pct") < LOW_USAGE:
                status = "thin"
            elif pd.notna(auto):
                status = "broken" if auto >= BROKEN else "cracking" if auto >= CRACKING else "holding"
            rows.append(dict(role=r["id"], onet_soc=soc, occupation=x.occupation, task_id=x.task_id, task=x.task,
                task_type=x.task_type, tier=tier, reason=reason, status=status,
                automation_pct=auto, augmentation_pct=x.get(C+"collaboration_bucket_augmentation_pct"),
                directive_pct=x.get(C+"collaboration_directive_pct"), feedback_loop_pct=x.get(C+"collaboration_feedback_loop_pct"),
                task_iteration_pct=x.get(C+"collaboration_task_iteration_pct"), learning_pct=x.get(C+"collaboration_learning_pct"),
                validation_pct=x.get(C+"collaboration_validation_pct"),
                autonomy=x.get(C+"ai_autonomy_mean"), edu_years=x.get(C+"human_education_years_mean"),
                human_hours=x.get(C+"human_only_time_mean"), with_ai_minutes=x.get(C+"human_with_ai_time_mean"),
                usage_pct=x.get(C+"pct"), india_usage_pct=x.get(C+"india_pct"), api_usage_pct=x.get(A+"pct"),
                months=x.get(C+"months")))
D = pd.DataFrame(rows)
D["low_volume"] = D.usage_pct.notna() & (D.usage_pct < LOW_USAGE)
D.to_csv(ROOT/"data/ladders.csv", index=False)

cov = D[(D.tier != "X") & D.automation_pct.notna() & (D.status != "thin")]
print("tasks", len(D), "excluded X", (D.tier=="X").sum(), "with automation data", len(cov))
print("\n== H1: median automation share by tier, per role ==")
t = cov.groupby(["role","tier"]).automation_pct.median().unstack().round(1)
t["n_J"] = cov[cov.tier=="J"].groupby("role").size(); t["n_S"] = cov[cov.tier=="S"].groupby("role").size()
t["J-S"] = (t.J - t.S).round(1); print(t.to_string())
print("\nroles where J > S:", (t["J-S"] > 0).sum(), "of", t["J-S"].notna().sum())
print("pooled median by tier:", cov.groupby("tier").automation_pct.median().round(1).to_dict())
print("pooled mean by tier:", cov.groupby("tier").automation_pct.mean().round(1).to_dict())
print("\n== Validation: required human education years by tier (AEI estimate) ==")
print(cov.groupby("tier").edu_years.median().round(2).to_dict())
print("autonomy by tier:", cov.groupby("tier").autonomy.median().round(2).to_dict())
# permutation test on pooled J vs S medians, within-role shuffle
rng = np.random.default_rng(7); js = cov[cov.tier.isin(["J","S"])].copy()
obs = js[js.tier=="J"].automation_pct.median() - js[js.tier=="S"].automation_pct.median()
null = []
for _ in range(5000):
    js["perm"] = js.groupby("role").tier.transform(lambda s: rng.permutation(s.values))
    null.append(js[js.perm=="J"].automation_pct.median() - js[js.perm=="S"].automation_pct.median())
print(f"\nJ−S pooled median gap {obs:.1f} pts; permutation p (one-sided) = {(np.array(null) >= obs).mean():.4f}")
print("\nstatus counts among junior tasks:", cov[cov.tier=="J"].status.value_counts().to_dict())
