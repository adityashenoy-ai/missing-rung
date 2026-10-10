"""Step 2: one row per O*NET task with Apr–May 2026 averaged metrics.
Inputs: data/interim/aei_tasks_long.csv (step 1), data/raw/onet_31_0_task_statements.csv
(O*NET 31.0, U.S. DOL/ETA, CC-BY 4.0). Averaging rule: mean of the months in which the
source published the cell; `months` records how many (1 or 2). Unpublished cells stay blank."""
import pandas as pd, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
L = pd.read_csv(ROOT/"data/interim/aei_tasks_long.csv", dtype={"task_id": str})
L["task_id"] = L.task_id.str.replace(r"\.0$", "", regex=True)
agg = L.groupby(["source","task_id","metric_id"]).value.agg(["mean","count"]).reset_index()
W = agg.pivot_table(index="task_id", columns=["source","metric_id"], values="mean")
W.columns = [f"{s}__{m}" for s, m in W.columns]
months = agg[(agg.source=="claude_ai")&(agg.metric_id=="collaboration_bucket_automation_pct")].set_index("task_id")["count"]
W["claude_ai__months"] = months
O = pd.read_csv(ROOT/"data/raw/onet_31_0_task_statements.csv", dtype=str)
O = O.rename(columns={"O*NET-SOC Code":"onet_soc","Title":"occupation","Task ID":"task_id","Task":"task","Task Type":"task_type"})
out = O[["onet_soc","occupation","task_id","task","task_type"]].merge(W, left_on="task_id", right_index=True, how="left")
out.to_csv(ROOT/"data/interim/task_metrics.csv", index=False)
print(out.shape, out["claude_ai__collaboration_bucket_automation_pct"].notna().sum())
