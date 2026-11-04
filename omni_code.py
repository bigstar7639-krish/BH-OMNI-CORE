# OMNI CODE HELPER - Phase 19 Step 1 - SAME PROJECT
# Category 23 - Explain + template only
TIPS = {
    "python": "Python: print('Vanakkam') - simple, readable. Indent matters!",
    "list": "List: a = [1,2,3] - a.append(4) panna add aagum.",
    "dict": "Dict: d = {'name':'Krish'} - d['name'] nu access pannalam.",
    "loop": "Loop: for i in range(5): print(i) - 0 to 4 print aagum.",
    "function": "Function: def hello(): return 'Hi' - def use panni create pannu.",
    "git": "Git: git status, git add ., git commit -m 'msg', git push",
}

def handle_code(msg):
    m = msg.strip().lower()
    if m.startswith("code "):
        topic = msg.strip()[5:].strip().lower()
        if topic in TIPS:
            return f"💻 CODE HELPER - {topic}:\n{TIPS[topic]}"
        return f"💻 CODE HELPER: '{topic}' - ippo topics: {', '.join(TIPS.keys())}"
    if m in ["code", "code list", "code topics"]:
        return "💻 OMNI CODE TOPICS:\n" + "\n".join(f"- {k}" for k in TIPS.keys())
    return None
