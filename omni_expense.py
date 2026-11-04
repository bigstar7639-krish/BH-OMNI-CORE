# OMNI EXPENSE TRACKER - Phase 9 Step 3 - SAME PROJECT
# Category 19 - Finance
from omni_memory import _load, _save

def get_expenses():
    d = _load()
    return d.get("expenses", [])

def handle_expense(msg):
    m = msg.strip().lower()
    if m.startswith("expense add "):
        rest = msg.strip()[12:].strip()
        if not rest:
            return "Expense sollu da! Ex: expense add 100 lunch"
        parts = rest.split(None, 1)
        try:
            amt = float(parts[0])
        except:
            return "Amount number-la sollu da! Ex: expense add 100 lunch"
        item = parts[1] if len(parts) > 1 else "general"
        d = _load()
        ex = d.get("expenses", [])
        ex.append({"amount": amt, "item": item})
        d["expenses"] = ex
        _save(d)
        return f"✅ Expense added: Rs.{amt} - {item}"
    if m in ["expenses", "expense", "expense list"]:
        ex = get_expenses()
        if not ex:
            return "Expense illa da! 'expense add 100 lunch' nu add pannu!"
        total = sum(e.get("amount", 0) for e in ex)
        out = f"💰 OMNI EXPENSES - Total: Rs.{total}\n"
        for i, e in enumerate(ex[-10:]):
            out += f"{i+1}. Rs.{e.get('amount')} - {e.get('item')}\n"
        return out
    if m == "expense total":
        total = sum(e.get("amount", 0) for e in get_expenses())
        return f"💰 Total Expense: Rs.{total}"
    return None
