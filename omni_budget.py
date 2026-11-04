# OMNI BUDGET - Cat 19 - Budget planner - Expense-oda next level
import json, pathlib
F = pathlib.Path("omni_budget.json")
def _load():
    if F.exists():
        try: return json.loads(F.read_text())
        except: pass
    return {"budget": 0, "spent": 0}
def _save(d): F.write_text(json.dumps(d, ensure_ascii=False, indent=2))
def handle_budget(msg):
    s = msg.strip(); m = s.lower()
    if m.startswith("budget set "):
        try: amt = float(s[11:].strip()); d=_load(); d["budget"]=amt; _save(d); return f"💰 BUDGET SET: Rs.{amt}"
        except: return "💰 BUDGET: 'budget set 5000' nu number kodu da!"
    if m in ["budget", "budget status"]:
        d=_load(); left=d["budget"]-d["spent"]
        return f"💰 BUDGET:\nBudget: Rs.{d['budget']}\nSpent: Rs.{d['spent']}\nLeft: Rs.{left}"
    return None
