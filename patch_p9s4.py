import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_expense" not in t:
    old = 'def get_omni_habit(msg="habits"):'
    new = '''def get_omni_expense(msg="expenses"):
    try:
        from omni_expense import handle_expense
        r = handle_expense(msg)
        if r is None:
            r = "Expense illa da! 'expense add 100 lunch' nu add pannu!"
        return {"reply": r, "source": "omni_expense.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Expense error: {e}", "source": "omni_expense.py"}
def get_omni_habit(msg="habits"):'''
    assert old in t, "server habit function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_expense" not in t:
    old2 = '        if self.path.startswith("/api/omni_habit"):'
    new2 = '''        if self.path.startswith("/api/omni_expense"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "expenses"
            self.send_json(get_omni_expense(msg))
        if self.path.startswith("/api/omni_habit"):'''
    assert old2 in t, "server habit route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI EXPENSE" not in h:
    old3 = '<div class="card"><b>🎯 OMNI HABIT TRACKER'
    assert old3 in h, "dashboard habit card illa!"
    new3 = '''<div class="card"><b>💰 OMNI EXPENSE TRACKER - Phase 9 Step 4!</b><br><br>
<div id="expenseHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Expense Tracker Ready!</div><br>
<input id="expenseInput" value="expenses" style="width:65%" onkeydown="if(event.key==='Enter')sendExpense()">
<button onclick="sendExpense()">Send Expense</button>
<script>
async function sendExpense(){
  let msg=document.getElementById('expenseInput').value;
  let h=document.getElementById('expenseHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_expense?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nEXPENSE: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>🎯 OMNI HABIT TRACKER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P9S4 DONE")
