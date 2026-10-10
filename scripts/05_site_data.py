"""Step 5: assemble site/data.json — the only file the web page reads."""
import json, pathlib, sys
import pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from roles import ROLES, EXCLUDED
from guidance import G
D = pd.read_csv(ROOT/"data/ladders.csv", dtype={"task_id": str})
R = json.load(open(ROOT/"data/robustness.json"))
def clean(v):
    return None if pd.isna(v) else (round(float(v), 2) if isinstance(v, float) else v)
roles = []
for r in ROLES:
    g = D[(D.role == r["id"]) & (D.tier != "X")]
    tasks = [{k: clean(x[k]) for k in ["task_id","onet_soc","occupation","task","task_type","tier","reason","status",
              "automation_pct","augmentation_pct","directive_pct","feedback_loop_pct","task_iteration_pct","learning_pct",
              "validation_pct","autonomy","human_hours","with_ai_minutes","usage_pct","india_usage_pct","api_usage_pct","months"]}
             for _, x in g.iterrows()]
    head = g[g.status.isin(["broken","cracking","holding"])]
    med = head.groupby("tier").automation_pct.median()
    roles.append({**r, "occupations": sorted(g.occupation.unique().tolist()),
        "n_tasks": int(len(g)), "n_with_data": int(len(head)),
        "n_broken_junior": int(((head.tier=="J")&(head.status=="broken")).sum()),
        "median_by_tier": {k: round(float(v),1) for k, v in med.items()},
        "guidance": G[r["id"]], "tasks": tasks})
H = D[(D.tier!="X") & D.status.isin(["broken","cracking","holding"])]
out = {
  "meta": {
    "built": "2026-10-10",
    "period": "April–May 2026 (average of the months published)",
    "source": "Anthropic Economic Index, release 2026-06-26 (CC-BY)",
    "source_url": "https://huggingface.co/datasets/Anthropic/EconomicIndex",
    "report_url": "https://www.anthropic.com/research/economic-index-june-2026-report",
    "onet": "O*NET 31.0 Task Statements, U.S. Department of Labor/ETA (CC-BY 4.0)",
    "onet_url": "https://www.onetcenter.org/database.html",
    "thresholds": {"broken": 65, "cracking": 50, "min_usage_pct": 0.01},
  },
  "headline": {"median_by_tier": R["main"], "n_tasks": R["n_tasks"], "roles_J_gt_M": R["roles_J_gt_M"],
               "roles_J_gt_S": R["roles_J_gt_S"], "perm_J_vs_M": R["perm_J_vs_M"], "perm_J_vs_S": R["perm_J_vs_S"],
               "broken_junior_total": int(((H.tier=="J")&(H.status=="broken")).sum()),
               "coverage_pct": R["coverage_pct"]},
  "robustness": R, "roles": roles, "excluded": EXCLUDED,
}
(ROOT/"site").mkdir(exist_ok=True)
json.dump(out, open(ROOT/"site/data.json","w"), ensure_ascii=False, separators=(",",":"))
print("ok", len(roles), "roles;", out["headline"])
