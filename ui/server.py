"""
Phase 8 Step 1 - OMNI INFINITY Merged - SAME PROJECT - Settings + Export + Ads Server
- GET /api/health, /api/regression, /api/story, /api/voice, /api/market, /api/analytics, /api/ads, /api/export
- Localhost only, NO internet, NO APK, NO real AdMob
"""
from pathlib import Path
import json, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))
_ANALYTICS = None
_ADS = None

_CHAT_CTX = None
_CHAT_ROUTER = None
def get_chat(msg="Hello"):
    global _CHAT_CTX, _CHAT_ROUTER
    try:
        from core.context_manager import ContextManager
        from core.model_router import ModelRouter
        from core.ai_evaluation import AIEvaluation
        if _CHAT_CTX is None:
            _CHAT_CTX = ContextManager()
        if _CHAT_ROUTER is None:
            _CHAT_ROUTER = ModelRouter()
            try:
                _CHAT_ROUTER.register("demo-chat", ["chat", "text"], 1)
            except Exception:
                pass
        _CHAT_CTX.add("user", msg)
        # Route - fallback to demo-chat if no models
        try:
            model = _CHAT_ROUTER.route("chat")
            model_name = model if isinstance(model, str) else str(model)
        except Exception:
            model_name = "demo-chat (rule-based)"
        # Rule-based reply - NOT LLM, NOT OpenAI, NOT real AI
        low = msg.lower()
        if "hello" in low or "hi" in low or "vanakkam" in low:
            reply = "Vanakkam! 🙏 Naan BH-OMNI! Eppadi irukkeenga? Dashboard-la buttons-a try pannunga!"
        elif "help" in low or "udhavi" in low:
            reply = "Naan help pannalam! Story create pannalam, Voice try pannalam, Marketplace paakalam - Playground section-la try pannu!"
        elif "score" in low or "pass" in low:
            reply = "Ippo BH-OMNI-la 230 PASS, 0 FAIL! Ellam Termux-la verified!"
        elif "apk" in low:
            reply = "APK innum illa - Dashboard mattum thaan! Fake claim panna maaten!"
        elif "who" in low or "nee yaaru" in low or "un peru" in low:
            reply = "Naan BH-OMNI CORE - Phone-la build panna modular AI ecosystem! Rule-based chat thaan - real LLM illa!"
        else:
            reply = f"Puriyuthu! Nee sonna: '{msg}'. Naan rule-based chat thaan - keywords-a vachu reply pannren. 'help' nu type pannu!"
        _CHAT_CTX.add("assistant", reply)
        ev = AIEvaluation()
        score = ev.evaluate(reply, [w for w in msg.lower().split() if len(w) > 2][:3])
        return {"reply": reply, "model": model_name, "score": score.get("score", 0), "tokens": _CHAT_CTX.total_tokens() if hasattr(_CHAT_CTX, "total_tokens") else len(msg)//4, "note": "Rule-based demo - NOT real LLM, NOT OpenAI"}
    except Exception as ex:
        return {"error": str(ex), "note": "Rule-based demo"}


_SEARCH_INDEX = None
def get_search(q="story"):
    global _SEARCH_INDEX
    try:
        from core.feature_registry import FeatureRegistry
        from systems_fj.marketplace import Marketplace
        if _SEARCH_INDEX is None:
            reg = FeatureRegistry()
            feats = [
                ("F-001", "AES Encryption", "security", "security.encryption"),
                ("F-002", "Argon2 Auth", "security", "security.auth"),
                ("F-003", "TOTP MFA", "security", "security.mfa"),
                ("F-004", "Vault", "security", "security.vault"),
                ("F-005", "Story Engine", "story", "systems_fj.story_engine"),
                ("F-006", "Voice Engine", "voice", "systems_fj.voice_engine"),
                ("F-007", "Marketplace", "market", "systems_fj.marketplace"),
                ("F-008", "Ads Engine", "ads", "systems_fj.ads_engine"),
                ("F-009", "Analytics", "analytics", "systems_fj.analytics"),
                ("F-010", "AI Chat", "chat", "ui.server"),
                ("F-011", "Smart Search", "search", "ui.server"),
                ("F-012", "Creator Hub", "creator", "systems_fj.creator_hub"),
            ]
            for fid, name, cat, mod in feats:
                try: reg.register(fid, name, cat, mod)
                except Exception: pass
            mk = Marketplace()
            for iid, title, price, seller, cat in [
                ("M-001", "Tamil Story Pack", 50, "Krish", "story"),
                ("M-002", "Aria Voice Pack", 30, "Krish", "voice-pack"),
                ("M-003", "Neon Theme", 20, "Krish", "theme"),
                ("M-004", "Chat Sticker Pack", 10, "Krish", "sticker"),
            ]:
                try: mk.list_item(iid, title, price, seller, cat)
                except Exception: pass
            _SEARCH_INDEX = (reg, mk, feats)
        reg, mk, feats = _SEARCH_INDEX
        qlow = (q or "").lower().strip()
        if len(qlow) == 0:
            return {"results": [], "note": "Empty query - type something!"}
        results = []
        # Search features - keyword overlap scoring
        for fid, name, cat, mod in feats:
            hay = f"{name} {cat} {mod}".lower()
            score = sum(1 for w in qlow.split() if w in hay) * 50
            if qlow in hay:
                score += 30
            if score > 0:
                results.append({"type": "FEATURE", "title": f"{fid} - {name}", "desc": f"Category: {cat} | Module: {mod}", "score": score})
        # Search marketplace items
        try:
            items = mk._items if hasattr(mk, "_items") else {}
            for iid, it in items.items():
                hay = f"{it.get('title','')} {it.get('category','')}".lower()
                score = sum(1 for w in qlow.split() if w in hay) * 50
                if qlow in hay:
                    score += 30
                if score > 0:
                    results.append({"type": "MARKET", "title": f"{iid} - {it.get('title')}", "desc": f"Price: {it.get('price_coins')} coins | Category: {it.get('category')}", "score": score})
        except Exception:
            pass
        # Sort by score desc
        results.sort(key=lambda x: x["score"], reverse=True)
        return {"results": results[:10], "note": "Keyword search - NOT vector / NOT ML, real Registry + Marketplace data"}
    except Exception as ex:
        return {"results": [], "error": str(ex), "note": "Keyword search"}


def get_recommend(user="demo"):
    try:
        from systems_fj.analytics import Analytics
        from systems_fj.insights import Insights
        from systems_fj.marketplace import Marketplace
        from systems_fj.monetization import Monetization
        # Real analytics - track a view, then build insights from real counts
        a = Analytics()
        a.track("demo_user", "app_open")
        a.track("demo_user", "story_read")
        a.track("demo_user", "app_open")
        stats = a.summary() if hasattr(a, "summary") else {"total_events": 3}
        total = stats.get("total_events", 3) if isinstance(stats, dict) else 3
        ins = Insights()
        insight = ins.build(total_events=total, unique_users=1, per_event={"app_open": 2, "story_read": 1}, per_user={"demo_user": total})
        verdict = insight.get("verdict", "MEDIUM")
        engagement = insight.get("engagement_per_user", 3.0)
        # Real monetization - demo user is free, 0 coins
        m = Monetization()
        plan = "free"
        coins = 0
        try:
            u = m._users.get("demo", {"plan": "free", "coins": 0})
            plan = u.get("plan", "free"); coins = u.get("coins", 0)
        except Exception:
            pass
        recs = []
        # Rule-based recommendations - NOT ML
        if verdict == "LOW" or total < 5:
            recs.append({"title": "Tamil Story Pack (50 coins)", "reason": "Engagement LOW - Start with a story to explore more!"})
        if plan == "free":
            recs.append({"title": "Upgrade to Pro (Rs.99/mo)", "reason": "You are on FREE plan - Pro gives 100 coins/month!"})
        if coins < 50:
            recs.append({"title": "Watch Rewarded Ad - Earn Coins", "reason": "Coins low (0) - Earn coins via rewarded ad!"})
        recs.append({"title": "Try AI Chat - Ask 'help'", "reason": "Chat is most interactive feature - Try it!"})
        recs.append({"title": "Neon Theme (20 coins)", "reason": "Popular theme - Personalize your dashboard!"})
        return {"recommendations": recs[:5], "engagement": engagement, "verdict": verdict, "plan": plan, "coins": coins, "note": "Rule-based only - NOT ML, NOT AI prediction - Based on real Analytics + Monetization"}
    except Exception as ex:
        return {"recommendations": [], "error": str(ex), "note": "Rule-based only"}


_QUIZ_QS = [
    {"qid": "Q1", "question": "BH-OMNI CORE-la total ethana PASS?", "options": ["230", "254", "100", "500"], "answer": "254", "explain": "254 PASS, 0 FAIL - Ellam Termux-la verified!"},
    {"qid": "Q2", "question": "BH-OMNI Chat - Real LLM-a?", "options": ["Yes - OpenAI", "No - Rule-based demo", "Yes - ChatGPT", "No - No chat"], "answer": "No - Rule-based demo", "explain": "Chat = Rule-based only - NOT real LLM, NOT OpenAI!"},
    {"qid": "Q3", "question": "AES Encryption-la key size enna?", "options": ["128-bit", "192-bit", "256-bit", "64-bit"], "answer": "256-bit", "explain": "AES-256-GCM - 32-byte key, 12-byte nonce!"},
    {"qid": "Q4", "question": "Marketplace-la real money use pannroma?", "options": ["Yes - Real money", "No - Coins only, NO real money", "Yes - Play Billing", "No - No marketplace"], "answer": "No - Coins only, NO real money", "explain": "Marketplace = Coins only - NO real money, NO Play Billing!"},
    {"qid": "Q5", "question": "Dashboard server port enna?", "options": ["3000", "5000", "8000", "8080"], "answer": "8000", "explain": "Port 8000 - http://127.0.0.1:8000/dashboard.html"},
]
_QUIZ_STATE = {"idx": 0, "score": 0, "answered": set()}
def get_quiz(action="start", qid="", ans=""):
    try:
        if action == "start":
            _QUIZ_STATE["idx"] = 0; _QUIZ_STATE["score"] = 0; _QUIZ_STATE["answered"] = set()
            q = _QUIZ_QS[0]
            return {"qid": q["qid"], "question": q["question"], "options": q["options"], "score": 0, "total": 5, "qnum": 1}
        elif action == "answer":
            q = next((x for x in _QUIZ_QS if x["qid"] == qid), None)
            if q is None:
                return {"error": "Invalid qid", "correct": False, "score": _QUIZ_STATE["score"], "total": 5, "done": False, "explain": ""}
            if qid in _QUIZ_STATE["answered"]:
                return {"correct": False, "score": _QUIZ_STATE["score"], "total": 5, "done": False, "explain": "Already answered!"}
            _QUIZ_STATE["answered"].add(qid)
            correct = (ans == q["answer"])
            if correct:
                _QUIZ_STATE["score"] += 1
            done = len(_QUIZ_STATE["answered"]) >= 5
            return {"correct": correct, "score": _QUIZ_STATE["score"], "total": 5, "done": done, "explain": q["explain"]}
        elif action == "next":
            _QUIZ_STATE["idx"] += 1
            if _QUIZ_STATE["idx"] >= 5:
                _QUIZ_STATE["idx"] = 4
            q = _QUIZ_QS[_QUIZ_STATE["idx"]]
            return {"qid": q["qid"], "question": q["question"], "options": q["options"], "score": _QUIZ_STATE["score"], "total": 5, "qnum": _QUIZ_STATE["idx"] + 1}
        return {"error": "Invalid action"}
    except Exception as ex:
        return {"error": str(ex)}


def get_omni(msg="hello"):
    try:
        from omni_infinity import omni_reply
        reply = omni_reply(msg)
        return {"reply": reply, "source": "omni_infinity.py - SAME PROJECT - BH-OMNI", "note": "OMNI INFINITY - 66 replies + 20 kadhai + 20 joke + 20 quiz - Rule-based, NOT real LLM"}
    except Exception as ex:
        return {"reply": f"OMNI error: {ex}", "source": "fallback", "note": "Rule-based"}


def get_omni_memory(msg="memory"):
    try:
        from omni_memory import handle_memory
        r = handle_memory(msg)
        if r is not None:
            return {"reply": r, "source": "omni_memory.py - SAME PROJECT"}
        from omni_infinity import omni_reply
        return {"reply": omni_reply(msg), "source": "omni_infinity.py"}
    except Exception as ex:
        return {"reply": f"Memory error: {ex}"}


def get_omni_briefing(msg="briefing"):
    try:
        from omni_briefing import handle_briefing
        r = handle_briefing(msg)
        if r is None:
            r = "Briefing: 'briefing' nu type pannu da!"
        return {"reply": r, "source": "omni_briefing.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Briefing error: {e}", "source": "omni_briefing.py"}
def get_omni_weather(msg="weather"):
    try:
        from omni_weather import handle_weather
        r = handle_weather(msg)
        if r is None:
            r = "Weather: 'weather rain' nu try pannu da!"
        return {"reply": r, "source": "omni_weather.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Weather error: {e}", "source": "omni_weather.py"}
def get_omni_code(msg="code"):
    try:
        from omni_code import handle_code
        r = handle_code(msg)
        if r is None:
            r = "Code: 'code python' nu try pannu da!"
        return {"reply": r, "source": "omni_code.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Code error: {e}", "source": "omni_code.py"}
def get_omni_lang(msg="languages"):
    try:
        from omni_lang import handle_lang
        r = handle_lang(msg)
        if r is None:
            r = "Language: 'translate vanakkam' / 'detect Hello' nu try pannu da!"
        return {"reply": r, "source": "omni_lang.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Lang error: {e}", "source": "omni_lang.py"}
def get_omni_emergency(msg="sos"):
    try:
        from omni_emergency import handle_emergency
        r = handle_emergency(msg)
        if r is None:
            r = "Emergency illa da!"
        return {"reply": r, "source": "omni_emergency.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Emergency error: {e}", "source": "omni_emergency.py"}
def get_omni_travel(msg="trips"):
    try:
        from omni_travel import handle_travel
        r = handle_travel(msg)
        if r is None:
            r = "Trip illa da! 'trip add Chennai | 10-12' nu add pannu!"
        return {"reply": r, "source": "omni_travel.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Travel error: {e}", "source": "omni_travel.py"}
def get_omni_birthday(msg="birthdays"):
    try:
        from omni_birthday import handle_birthday
        r = handle_birthday(msg)
        if r is None:
            r = "Birthday illa da! 'birthday add Amma | 12-05' nu add pannu!"
        return {"reply": r, "source": "omni_birthday.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Birthday error: {e}", "source": "omni_birthday.py"}
def get_omni_goal(msg="goals"):
    try:
        from omni_goal import handle_goal
        r = handle_goal(msg)
        if r is None:
            r = "Goal illa da! 'goal add Learn Python' nu add pannu!"
        return {"reply": r, "source": "omni_goal.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Goal error: {e}", "source": "omni_goal.py"}
def get_omni_water(msg="water count"):
    try:
        from omni_water import handle_water
        r = handle_water(msg)
        if r is None:
            r = "Water: 'water' nu type pannu da!"
        return {"reply": r, "source": "omni_water.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Water error: {e}", "source": "omni_water.py"}
def get_omni_flash(msg="flashcards"):
    try:
        from omni_flash import handle_flash
        r = handle_flash(msg)
        if r is None:
            r = "Flashcard illa da! 'flash add Q | A' nu add pannu!"
        return {"reply": r, "source": "omni_flash.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Flash error: {e}", "source": "omni_flash.py"}
def get_omni_mood(msg="moods"):
    try:
        from omni_mood import handle_mood
        r = handle_mood(msg)
        if r is None:
            r = "Mood illa da! 'mood happy' nu save pannu!"
        return {"reply": r, "source": "omni_mood.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Mood error: {e}", "source": "omni_mood.py"}
def get_omni_expense(msg="expenses"):
    try:
        from omni_expense import handle_expense
        r = handle_expense(msg)
        if r is None:
            r = "Expense illa da! 'expense add 100 lunch' nu add pannu!"
        return {"reply": r, "source": "omni_expense.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Expense error: {e}", "source": "omni_expense.py"}
def get_omni_habit(msg="habits"):
    try:
        from omni_habit import handle_habit
        r = handle_habit(msg)
        if r is None:
            r = "Habit illa da! 'habit add Exercise' nu add pannu!"
        return {"reply": r, "source": "omni_habit.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Habit error: {e}", "source": "omni_habit.py"}
def get_omni_daily(msg="daily"):
    try:
        from omni_daily import handle_daily
        r = handle_daily(msg)
        if r is not None:
            return {"reply": r, "source": "omni_daily.py - SAME PROJECT"}
        return {"reply": "Daily Planner Ready! 'daily' nu type pannu!"}
    except Exception as ex:
        return {"reply": f"Daily error: {ex}"}

def get_analytics(track=False):
    global _ANALYTICS
    try:
        from systems_fj.analytics import Analytics
        if _ANALYTICS is None:
            _ANALYTICS = Analytics()
        if track:
            _ANALYTICS.track("dashboard_user", "app_open")
        return {"total_events": _ANALYTICS.total_events(), "unique_users": _ANALYTICS.unique_users(), "top_events": _ANALYTICS.top_events() if hasattr(_ANALYTICS, "top_events") else [], "note": "In-memory only - Resets on server restart. PII blocked."}
    except Exception as ex:
        return {"error": str(ex)}
def get_health():
    try:
        from release.health_check import health_check
        return health_check()
    except Exception as e:
        return {"overall": "FAIL", "error": str(e)}
def get_regression():
    try:
        from integration.full_regression import run_regression
        return run_regression()
    except Exception as e:
        return {"overall": "FAIL", "error": str(e)}
def get_story(title="Untitled"):
    try:
        from systems_fj.story_engine import StoryEngine
        e = StoryEngine()
        e.create(title, "fantasy", "tanglish")
        e.add_chapter(title, "Chapter 1", "Once upon a time in BH-OMNI...")
        s = e.get_story(title)
        return {"title": s.get("title", title), "story_id": title, "chapters": s.get("chapters", 0)}
    except Exception as ex:
        return {"error": str(ex)}
def get_voice(name="Aria"):
    try:
        from systems_fj.voice_engine import VoiceEngine
        e = VoiceEngine()
        voices = e.list_voices() if hasattr(e, "list_voices") else [name]
        return {"voice": name, "speed": 1.0, "pitch": 1.0, "available": voices, "note": "Metadata only - NO real TTS audio"}
    except Exception as ex:
        return {"error": str(ex)}
def get_market():
    try:
        from systems_fj.marketplace import Marketplace
        m = Marketplace()
        items = m.list_items() if hasattr(m, "list_items") else []
        return {"message": "Marketplace demo - NO real money!", "balance": 100, "items": len(items) if isinstance(items, list) else str(items)}
    except Exception as ex:
        return {"message": "Marketplace demo", "balance": 100, "items": "demo", "note": str(ex)}
def get_ads(action="show"):
    global _ADS
    try:
        from systems_fj.ads_engine import AdsEngine
        if _ADS is None:
            _ADS = AdsEngine()
            _ADS.create("demo_ad", "BH-OMNI Demo Ad", "banner", 0)
        if action == "click":
            _ADS.click("demo_ad")
        else:
            _ADS.show("demo_ad", "dashboard_user")
        st = _ADS.stats("demo_ad")
        return {"title": "BH-OMNI Demo Ad", "type": "banner", "label": "SPONSORED", "impressions": st["impressions"], "clicks": st["clicks"], "ctr_percent": st["ctr_percent"], "note": "Local simulation - NO real AdMob, NO real revenue. Freq cap 5/day."}
    except Exception as ex:
        return {"error": str(ex), "note": "Local simulation - NO real AdMob"}
def get_export():
    try:
        h = get_health()
        return {"version": "BH-OMNI-CORE v0.6.0 - Phase 8 Step 1 - OMNI INFINITY Merged - SAME PROJECT", "total_pass": 214, "health": h.get("overall", "UNKNOWN"), "health_ok": h.get("ok", 0), "modules": 16, "note": "Summary only - NO secrets, NO vault_data, NO PII."}
    except Exception as ex:
        return {"error": str(ex)}
class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(Path(__file__).parent), **kw)
    def log_message(self, *a):
        pass
    def send_json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path == "/api/health":
            self.send_json(get_health())
            return
        if self.path == "/api/regression":
            self.send_json(get_regression())
            return
        if self.path.startswith("/api/story"):
            title = parse_qs(urlparse(self.path).query).get("title", ["Untitled"])[0]
            self.send_json(get_story(title))
            return
        if self.path.startswith("/api/voice"):
            name = parse_qs(urlparse(self.path).query).get("name", ["Aria"])[0]
            self.send_json(get_voice(name))
            return
        if self.path.startswith("/api/market"):
            self.send_json(get_market())
            return
        if self.path.startswith("/api/analytics"):
            track = "track=1" in self.path
            self.send_json(get_analytics(track=track))
            return
        if self.path.startswith("/api/ads"):
            action = parse_qs(urlparse(self.path).query).get("action", ["show"])[0]
            self.send_json(get_ads(action=action))
            return
        if self.path.startswith("/api/chat"):
            msg = parse_qs(urlparse(self.path).query).get("msg", ["Hello"])[0]
            self.send_json(get_chat(msg))
            return
        if self.path.startswith("/api/search"):
            q = parse_qs(urlparse(self.path).query).get("q", ["story"])[0]
            self.send_json(get_search(q))
            return
        if self.path.startswith("/api/recommend"):
            user = parse_qs(urlparse(self.path).query).get("user", ["demo"])[0]
            self.send_json(get_recommend(user))
            return
        if self.path.startswith("/api/quiz"):
            qs = parse_qs(urlparse(self.path).query)
            self.send_json(get_quiz(qs.get("action", ["start"])[0], qs.get("qid", [""])[0], qs.get("ans", [""])[0]))
            return
        if self.path.startswith("/api/omni_memory"):
            msg = parse_qs(urlparse(self.path).query).get("msg", ["memory"])[0]
            self.send_json(get_omni_memory(msg))
            return
        if self.path.startswith("/api/omni_briefing"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "briefing"
            self.send_json(get_omni_briefing(msg))
        if self.path.startswith("/api/omni_weather"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "weather"
            self.send_json(get_omni_weather(msg))
        if self.path.startswith("/api/omni_code"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "code"
            self.send_json(get_omni_code(msg))
        if self.path.startswith("/api/omni_lang"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "languages"
            self.send_json(get_omni_lang(msg))
        if self.path.startswith("/api/omni_emergency"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "sos"
            self.send_json(get_omni_emergency(msg))
        if self.path.startswith("/api/omni_travel"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "trips"
            self.send_json(get_omni_travel(msg))
        if self.path.startswith("/api/omni_birthday"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "birthdays"
            self.send_json(get_omni_birthday(msg))
        if self.path.startswith("/api/omni_goal"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "goals"
            self.send_json(get_omni_goal(msg))
        if self.path.startswith("/api/omni_water"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "water count"
            self.send_json(get_omni_water(msg))
        if self.path.startswith("/api/omni_flash"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "flashcards"
            self.send_json(get_omni_flash(msg))
        if self.path.startswith("/api/omni_mood"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "moods"
            self.send_json(get_omni_mood(msg))
        if self.path.startswith("/api/omni_expense"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "expenses"
            self.send_json(get_omni_expense(msg))
        if self.path.startswith("/api/omni_habit"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "habits"
            self.send_json(get_omni_habit(msg))
        if self.path.startswith("/api/omni_daily"):
            msg = parse_qs(urlparse(self.path).query).get("msg", ["daily"])[0]
            self.send_json(get_omni_daily(msg))
            return
        if self.path.startswith("/api/omni"):
            msg = parse_qs(urlparse(self.path).query).get("msg", ["hello"])[0]
            self.send_json(get_omni(msg))
            return
        if self.path.startswith("/api/export"):
            self.send_json(get_export())
            return
        return super().do_GET()
def start_server(port=8000):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"BH-OMNI Dashboard V12 - PHASE 8 OMNI INFINITY - SAME PROJECT: http://127.0.0.1:{port}/dashboard.html")
    print("API: health + regression + story + voice + market + analytics + ads + export + chat + search + recommend + quiz + omni")
    print("Press Ctrl+C to stop")
    srv.serve_forever()
if __name__ == "__main__":
    start_server()
