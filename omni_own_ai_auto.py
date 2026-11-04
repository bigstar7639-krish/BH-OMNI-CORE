# OMNI OWN AI v4 - Phase 33 Step 1 - SAME PROJECT
# 100% OWN - Auto-learn from correction
# Format: correct <question> | <correct answer> = thappu answer-a thiruthum
from omni_own_ai import teach, ask_own
def correct(question, correct_answer):
    r = teach(question, correct_answer)
    return f"✅ CORRECTED + RE-LEARNED!\n{r}\nInime idha dhaan solluven da!"
def handle_auto(msg):
    s = msg.strip()
    ml = s.lower()
    if ml.startswith("correct "):
        rest = s[8:].strip()
        if " | " in rest:
            q, a = rest.split(" | ", 1)
            return correct(q.strip(), a.strip())
        return "🧠 CORRECT: 'correct vanakkam | Vanakkam da!' - ippadi | potu solli kodu da!"
    return None
