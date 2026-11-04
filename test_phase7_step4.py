# BH-OMNI CORE - Phase 7 Step 4 - Quiz Game - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v10_quiz_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["MINI QUIZ", "startQuiz()", "quizBox", "quizOptions", "/api/quiz"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v10_quiz_ui: PASS - Quiz card + start + options")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_quiz_ui: FAIL - {e}")
        return "FAIL"

def test_v10_server_quiz():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/quiz", "get_quiz", "_QUIZ_QS"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v10_server_quiz: PASS - /api/quiz + 5 questions server-side")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_server_quiz: FAIL - {e}")
        return "FAIL"

def test_v10_quiz_start():
    try:
        from ui.server import get_quiz
        r = get_quiz("start")
        assert r["qid"] == "Q1" and len(r["options"]) == 4 and r["score"] == 0 and r["total"] == 5
        assert "answer" not in r, "Answer leaked!"
        print(f"TEST v10_quiz_start: PASS - Q1: {r['question'][:40]}... Answer NOT leaked!")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_quiz_start: FAIL - {e}")
        return "FAIL"

def test_v10_quiz_correct():
    try:
        from ui.server import get_quiz
        get_quiz("start")
        r = get_quiz("answer", "Q1", "254")
        assert r["correct"] == True and r["score"] == 1, f"Should be correct: {r}"
        assert "254 PASS" in r["explain"]
        print(f"TEST v10_quiz_correct: PASS - Correct answer -> Score=1, Explain OK")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_quiz_correct: FAIL - {e}")
        return "FAIL"

def test_v10_quiz_wrong():
    try:
        from ui.server import get_quiz
        get_quiz("start")
        r = get_quiz("answer", "Q1", "100")
        assert r["correct"] == False and r["score"] == 0, f"Should be wrong: {r}"
        print("TEST v10_quiz_wrong: PASS - Wrong answer -> Score=0")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_quiz_wrong: FAIL - {e}")
        return "FAIL"

def test_v10_quiz_double_answer():
    try:
        from ui.server import get_quiz
        get_quiz("start")
        get_quiz("answer", "Q1", "254")
        r = get_quiz("answer", "Q1", "254")
        assert r["score"] == 1, f"Double answer should NOT add score: {r}"
        print("TEST v10_quiz_double_answer: PASS - Double answer blocked, Score stays 1")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_quiz_double_answer: FAIL - {e}")
        return "FAIL"

def test_v10_quiz_full_game():
    try:
        from ui.server import get_quiz
        get_quiz("start")
        answers = [("Q1","254"),("Q2","No - Rule-based demo"),("Q3","256-bit"),("Q4","No - Coins only, NO real money"),("Q5","8000")]
        for qid, ans in answers:
            r = get_quiz("answer", qid, ans)
        assert r["score"] == 5 and r["done"] == True, f"Full game should be 5/5 done: {r}"
        print("TEST v10_quiz_full_game: PASS - Full game 5/5, Done=True")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_quiz_full_game: FAIL - {e}")
        return "FAIL"

def test_v10_old_still_ok():
    try:
        from ui.server import get_recommend, get_search, get_chat, get_health
        assert len(get_recommend("demo")["recommendations"]) >= 3
        assert len(get_search("story")["results"]) >= 1
        assert "Vanakkam" in get_chat("hello")["reply"]
        assert get_health()["overall"] == "PASS"
        print("TEST v10_old_still_ok: PASS - Recommend + Search + Chat + Health still work")
        return "PASS"
    except Exception as e:
        print(f"TEST v10_old_still_ok: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v10_quiz_ui, test_v10_server_quiz, test_v10_quiz_start, test_v10_quiz_correct, test_v10_quiz_wrong, test_v10_quiz_double_answer, test_v10_quiz_full_game, test_v10_old_still_ok]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 7 STEP 4 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase7_4_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
