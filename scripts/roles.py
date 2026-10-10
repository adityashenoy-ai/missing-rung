"""Role → O*NET occupation mapping. A product decision: roles are named the way early-career
people in India search for jobs; each maps to the closest O*NET 31.0 occupation(s)."""
ROLES = [
  {"id":"software-engineer","name":"Software engineer","onet":["15-1252.00","15-1251.00"]},
  {"id":"qa-engineer","name":"QA / test engineer","onet":["15-1253.00"]},
  {"id":"web-developer","name":"Web developer","onet":["15-1254.00"]},
  {"id":"it-support","name":"IT support engineer","onet":["15-1232.00"]},
  {"id":"data-analyst","name":"Data analyst","onet":["15-2051.01","15-2051.00"]},
  {"id":"business-analyst","name":"Business / systems analyst","onet":["15-1211.00"]},
  {"id":"financial-analyst","name":"Financial analyst","onet":["13-2051.00"]},
  {"id":"accountant","name":"Accountant","onet":["13-2011.00","43-3031.00"]},
  {"id":"digital-marketer","name":"Digital marketer","onet":["13-1161.01","13-1161.00"]},
  {"id":"technical-writer","name":"Technical / content writer","onet":["27-3042.00"]},
  {"id":"ux-designer","name":"UI / UX designer","onet":["15-1255.00","27-1024.00"]},
  {"id":"project-manager","name":"Project / product manager","onet":["13-1082.00","15-1299.09"]},
]
EXCLUDED = [
  {"name":"Recruiter / HR","onet":"13-1071.00","reason":"Only 5 of 26 tasks have published Claude usage"},
  {"name":"Customer support","onet":"43-4051.00","reason":"Fewer than 5 tasks have published Claude usage"},
]
