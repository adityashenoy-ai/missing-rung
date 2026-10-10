"""Step 1: slim the raw Anthropic Economic Index (release 2026-06-26) files to the
task-level rows this project uses. Source: https://huggingface.co/datasets/Anthropic/EconomicIndex (CC-BY)."""
import pandas as pd, pathlib
RAW = pathlib.Path(__file__).resolve().parents[1] / "data/raw"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data/interim"
METRICS = ["pct","collaboration_bucket_automation_pct","collaboration_bucket_augmentation_pct",
  "collaboration_directive_pct","collaboration_feedback_loop_pct","collaboration_task_iteration_pct",
  "collaboration_learning_pct","collaboration_validation_pct","collaboration_none_pct",
  "ai_autonomy_mean","human_education_years_mean","human_only_time_mean","human_with_ai_time_mean",
  "use_case_work_pct","human_only_ability_pct"]
frames = []
for src, fn in [("claude_ai","aei_claude_ai_2026-06-26.csv"),("1p_api","aei_1p_api_2026-06-26.csv")]:
    d = pd.read_csv(RAW/fn, dtype={"node_external_id":str})
    d = d[(d.category_name=="onet")&(d.hierarchy_level==0)]
    g = d[(d.geo_id=="GLOBAL")&(d.metric_id.isin(METRICS))]
    i = d[(d.geo_id=="IND")&(d.metric_id=="pct")].assign(metric_id="india_pct")
    frames.append(pd.concat([g,i]).assign(source=src))
out = pd.concat(frames)[["source","date_start","metric_id","node_external_id","node_name","value"]]
out = out.rename(columns={"node_external_id":"task_id","node_name":"task_text"})
out.to_csv(OUT/"aei_tasks_long.csv", index=False)
print(len(out), out.task_id.nunique())
