# OMNI MEMORY - Phase 8 Step 2 - SAME PROJECT
import json
from pathlib import Path
MEM_FILE = Path(__file__).parent / "omni_memory.json"
def _load():
    try:
        if MEM_FILE.exists():
            return json.loads(MEM_FILE.read_text())
    except: pass
    return {"name":"","fav":"","notes":[],"todos":[],"quiz_best":0,"chat_count":0}
def _save(d):
    MEM_FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2))
def handle_memory(msg):
    m=msg.strip(); low=m.lower(); d=_load()
    if low.startswith("en peru "):
        d["name"]=m[8:].strip()[:30]; _save(d)
        return f"OK da! Un peru {d['name']} nu nyabagam vechutten! ❤️"
    if low.startswith("note "):
        d["notes"].append(m[5:].strip()[:200]); _save(d)
        return f"Note save panniten! Total: {len(d['notes'])}"
    if low=="notes":
        if not d["notes"]: return "Notes illa da!"
        return "📝 UN NOTES:\n"+"\n".join([f"{i+1}. {n}" for i,n in enumerate(d["notes"])])
    if low.startswith("todo "):
        d["todos"].append({"task":m[5:].strip()[:200],"done":False}); _save(d)
        return f"Todo add panniten! Total: {len(d['todos'])}"
    if low=="todos":
        if not d["todos"]: return "Todo illa da!"
        return "✅ UN TODOS:\n"+"\n".join([f"{i+1}. {'✅' if t['done'] else '⬜'} {t['task']}" for i,t in enumerate(d["todos"])])
    if low.startswith("done "):
        try:
            idx=int(m[5:].strip())-1
            d["todos"][idx]["done"]=True; _save(d)
            return f"Super! Todo {idx+1} mudinjuchu! ✅"
        except: return "Number-a sollu da! 'done 1' mathiri!"
    if low=="memory":
        done=sum(1 for t in d["todos"] if t["done"])
        return f"🧠 OMNI MEMORY:\nPeru: {d['name'] or 'Friend'}\nNotes: {len(d['notes'])}\nTodos: {done}/{len(d['todos'])} mudinjuchu\nChat: {d['chat_count']}"
    return None
