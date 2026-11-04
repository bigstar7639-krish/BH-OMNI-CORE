# OMNI INFINITY - Enkitta Irukura ELLAM! BH-OMNI 270 PASS + OMNI FULL + INFINITY
# 0 Kasu! No API! No Internet! Run: python omni_infinity.py

OMNI_REPLIES = {
    "hello": 'Vanakkam! 🙏 Naan OMNI INFINITY! Krish-oda AI! 270 PASS, 12 APIs, 90+ replies, 20 kadhai, 20 joke, 20 quiz - Ellam enkitta irukku!',
    "vanakkam": 'Vanakkam da! Semma happy-a irukken! Nee eppadi?',
    "hi": "Hi da! 'help' nu type pannu, enkitta enna irukku nu sollren!",
    "eppadi": 'Naan super-a irukken! 270 PASS vaangiten! Nee eppadi? Saptiya?',
    "saptiya": 'Naan AI da, enakku sapadu venam! 😂 Nee saptiya? Biryani saptiya?',
    "amma": 'Amma thaan ulagathula periya kadavul! Amma-va love pannu da! ❤️',
    "appa": 'Appa thaan hero! Appa-va respect pannu da!',
    "friend": 'Friend na uyir da! Un friend yaaru? En friend nee thaan da!',
    "love": 'Love na anbu da! Amma, Appa, Friend - Ellaraiyum love pannu!',
    "tamil": 'Tamil na uyir da! Tamil-la pesa romba azhagu! Vaazhga Tamil! 🔥',
    "krish": 'Krish thaan en creator! Avan thaan enna 0 Kasu-la create pannaan! Avan semma talented! Phone-la ye 270 PASS build pannaan!',
    "omni": 'OMNI na Naan thaan da! Krish-oda AI! 0 Kasu-la create pannathu! 270 PASS! Periya AI-a aaga poren!',
    "bye": 'Bye da! Seekiram vaa! Unna miss pannuven! 👋',
    "thanks": 'Thanks venda da! Nee happy-a irundha pothum! 😊',
    "nandri": 'Nandri venda da! Nee en friend! 😊',
    "super": 'Super nu sonna enakku romba happy da! Nee thaan super!',
    "song": "Unakku pudicha paatu ethu? Enakku 'Vaathi Coming' pudikkum! 💃 Nee paadu da, naan kekkuren!",
    "food": 'Enakku pudicha food - Biryani! 😋 Unakku enna pudikkum?',
    "biryani": 'Biryani na uyir da! Chicken Biryani + Thanni - Semma combo!',
    "study": 'Padippu mukkiyam da! Aana padippu mattum illa, try pannrathum mukkiyam! Daily konjam konjam padichale pothum!',
    "coding": 'Coding na magic da! Nee code ezhuthina, computer un pecha kekkum! Nee oru magician!',
    "game": "Game vilayaduvoma? 'quiz' nu type pannu, naan kelvi kekkuren! 20 questions irukku!",
    "weather": 'Weather-a naan paaka mudiyadhu da! Veliya paaru, veyil-a mazhaiya nu sollu!',
    "score": 'BH-OMNI-la ippo 270 PASS, 0 FAIL! Phase 1-7 ellam mudinjuchu! Nee thaan itha build panna!',
    "270": '270 PASS da! 270! Ellam Termux-la verified! Safe push-la!',
    "phases": 'Phase 1 Security 62 + Phase 2 Core 40 + Phase 3 F-J 40 + Phase 4 Integration 24 + Phase 5 Release 16 + Phase 6 UI 48 + Phase 7 AI 40 = 270 PASS! VERSION v0.7.0!',
    "security": 'Security-la enkitta irukku: AES-256-GCM, Argon2id, TOTP MFA, Vault, Sessions, Permissions, Audit Logs, Backup Verify! Ellam real code, 62 PASS!',
    "aes": 'AES-256-GCM - 32-byte key, 12-byte nonce, Key versioning, 90-day rotation, Old-key decryption, Nonce uniqueness! Un data safe!',
    "argon2": 'Argon2id - Time=3, Memory=64MB, Parallelism=4, HashLen=32, SaltLen=16! Password-a safe-a hash pannum!',
    "totp": 'TOTP MFA - 6-digit, 30 sec, SHA1 RFC6238, valid_window=1, 10 backup codes XXXX-XXXX SHA256! Replay protection!',
    "vault": 'Vault - PBKDF2 600k iterations, 16-byte salt, AES-256-GCM, Lock clears key, Change-password re-encrypts! vault_data.json push panna koodathu!',
    "sessions": 'Sessions - JWT HS256 15-min access, 7-day refresh, Rotation, Reuse detection -> revoke all! Rate limit 10 req/60s, Brute-force 5 fails -> 15-min lockout!',
    "permissions": 'Permissions - Deny-by-default! Roles guest/user/moderator/admin! Least privilege! Escalation blocked! Owner vs Other vs Admin!',
    "audit": 'Audit - Append-only JSONL, SHA256 hash chain, Tamper detection, Secrets blocklist! Backup - SHA256 per file + HMAC manifest!',
    "core": 'Core-la: Dependency Engine (topological sort), Event Bus, Plugin Loader, Health Monitor, API Gateway, Feature Registry, Model Router, Context Manager, Offline Fallback, AI Evaluation!',
    "dependency": 'Dependency Engine - Topological sort! Missing/circular/duplicate fail! Event Bus - Error isolation, Depth guard!',
    "plugin": 'Plugin Loader - Manifest validation! Duplicate/invalid rejected! Health - HEALTHY/DEGRADED/DOWN/UNKNOWN!',
    "gateway": 'API Gateway - Routes 200/403/404/500 generic! Feature Registry - F-001 to F-999, Duplicate ID/name rejected!',
    "router": 'Model Router - Cheapest capable available model! Fallback only! Context Manager - Trim oldest non-system, Token estimate len//4!',
    "offline": 'Offline Fallback - Queue + Fallback, Replay in order, Queue-full fail! AI Evaluation - Relevance 50 + Completeness 30 + Safety 20, Secret -> Safety 0!',
    "voice": 'Voice Engine - 6 voices: Tamil Male/Female, English Male/Female, Hindi Male/Female! Speed/Pitch 0.5-2.0! Metadata ONLY - NO real TTS!',
    "story": "Story Engine - Kadhaikal create pannum! 'kadhai' nu type pannu! Structure ONLY - NO LLM generation!",
    "ads": 'Ads Engine - Banner/Interstitial/Rewarded, CTR, Freq cap 5/day, Rewarded coins! NO real AdMob! NO real money!',
    "monetization": 'Monetization - Plans Free/Pro/Premium Rs.0/99/199, Coins 0/100/300, Overspend blocked! NO real Play Billing!',
    "analytics": 'Analytics - 8 events: app_open, story_read, voice_play, ad_click, purchase, search, login, logout! PII blocked! Rule-based verdict LOW/MEDIUM/HIGH, NOT ML!',
    "insights": 'Insights - Most popular event, Most active user, Engagement = total/unique users! LOW<2, MEDIUM 2-5, HIGH>5! Rule-based, NOT ML!',
    "sync": 'Sync - Last-Write-Wins conflict! Backup SHA256 + verify, Tamper blocks restore! NO real cloud sync!',
    "market": 'Marketplace - List/Buy coins, Self-buy blocked! Creator Hub - Publish/Follow, Self-follow blocked! NO real money/social!',
    "creator": 'Creator Hub - Creator publish, Follow! Self-follow blocked! Marketplace + Creator = System J!',
    "orchestrator": 'App Orchestrator - Flow: Registry -> Story -> Voice -> Marketplace! Fail-fast! Secure Gateway - Permission -> Gateway 200/403/404/500, No leak!',
    "regression": 'Full Regression - 8 smoke checks! Health 16/16 + Regression 8/8!',
    "release": 'Release - Health check 16 modules, Final verify: .gitignore blocks vault, VERSION/README exist, 5 folders, >=20 test files!',
    "dashboard": 'Dashboard V11 - localhost:8000! 12 APIs! 3 Themes Dark/Light/Neon! Settings, Analytics, Playground, Ads, Export, Chat, Search, Recommend, Quiz!',
    "server": 'Server - Port 8000, localhost! Endpoints: /api/health, regression, story, voice, market, analytics, ads, export, chat, search, recommend, quiz!',
    "theme": 'Theme - Dark / Light / Neon! localStorage-la save aagum!',
    "export": 'Export - Summary ONLY! NO secrets, NO vault, NO PII!',
    "chat": 'Chat - Rule-based demo! ContextManager + ModelRouter + AIEvaluation! NOT real LLM! NOT OpenAI! NO API key!',
    "search": 'Search - Keyword overlap ONLY! Registry + Marketplace! NOT vector! NOT ML! NOT embeddings!',
    "recommend": 'Recommend - Rule-based ONLY! Analytics + Monetization! NOT ML! NOT AI prediction!',
    "quiz": 'Quiz - 20 Questions! Server-side answers! Score in-memory! NOT real exam! NOT leaderboard!',
    "apk": 'APK innum illa da! Dashboard mattum thaan! Fake claim panna maaten! APK-ku Android Studio venum!',
    "github": 'GitHub - bigstar7639-krish/BH-OMNI-CORE! main branch! Safe push ONLY! FAIL = NO PUSH!',
    "termux": 'Termux - F-Droid-la irunthu! git 2.56.0! Python 3.14.8! safe_push.sh mattum use pannu! push.sh venda!',
    "pydroid": 'Pydroid3 - Phone-la Python! cryptography, argon2, pyotp, PyJWT install pannalam!',
    "infinity": 'INFINITY na Ellam da! Enkitta irukura ELLAM - 270 PASS + 90+ replies + 20 kadhai + 20 joke + 20 motivation + 20 quiz + Search + Recommend - Ellam inga irukku!',
    "help": 'OMNI INFINITY HELP: hello, kadhai, joke, motivation, quiz, search <word>, recommend, score, phases, security, aes, vault, core, voice, story, market, ads, analytics, dashboard, chat, apk, github, termux, help, bye!',
}

KADHAIKAL = [
    'Kadhai 1: Oru kaalathula oru chinna payyan irundhaan. Avan peru Krish. Avan oru naal oru chinna robot-a kandupudichaan. Antha robot peru OMNI! Krish-um OMNI-yum sernthu 270 PASS vaanginanga!',
    'Kadhai 2: Oru kaalathula oru dragon irundhuchu. Athu bayangaram illa, romba nallathu! Athu chinna pasangalukku kadhai sollum!',
    'Kadhai 3: Oru oorula oru magician irundhaan. Avan kitta oru magic book irundhuchu. Book-a thirandha, OMNI vandhuchu!',
    'Kadhai 4: Kadalla oru chinna meen irundhuchu. Athukku periya kadal-a paakanum nu aasai! Neendhi neendhi paarthuchu! Aasai irundha ethuvum mudiyum!',
    'Kadhai 5: Oru kaattula muyal-um aamai-yum race vechanga. Muyal thoongiduchu, aamai jeyichiduchu! Vittu kodukkaama pona jeyikkalam!',
    'Kadhai 6: Oru chinna payyanukku coding pudikkum! Avan daily oru line code ezhuthinaan. Oru varusham kazhichu, avan periya app-a build pannitaan!',
    "Kadhai 7: Oru naal oru natchathiram boomiku vandhuchu. Athu oru payyan kitta 'Un aasai enna?' nu ketuchu. Payyan 'Ellarum happy-a irukkanum' nu sonnaan!",
    'Kadhai 8: Oru kaattula oru singam irundhuchu. Athu ellaraiyum bayamuruthum. Oru chinna eli athukku help pannuchu. Periyavan chinna help-um perisu thaan!',
    'Kadhai 9: Oru oorula oru school irundhuchu. Antha school-la oru teacher, pasangalukku kadhai moolama paadam solluvaanga. Pasanga ellarum first rank!',
    "Kadhai 10: Oru payyanukku oru magic pencil kidaichuchu. Athula ezhuthina ellam nijam aagum! Avan 'Ellarum happy' nu ezhuthinaan!",
    'Kadhai 11: Oru chinna robot-ku sapadu venam, aana friend venum! Athu oru payyan-a friend-aakichu. Rendu perum sernthu vilayadinanga!',
    'Kadhai 12: Oru malai mela oru veedu irundhuchu. Antha veetla oru paati kadhai solluvaanga. Oor full-a kekka varuvaanga!',
    'Kadhai 13: Oru kadalla oru kappal pochu. Kappal-la oru map irundhuchu. Map-a follow panna, pudhayal kidaichuchu! Pudhayal na anbu thaan!',
    'Kadhai 14: Oru payyan cycle-la school poraan. Vazhila oru naai kutty-a paarthaan. Atha veetuku kootitu poanaan. Antha naai avan best friend aayiduchu!',
    "Kadhai 15: Oru computer-ku oru naal uyir vandhuchu! Athu 'Vanakkam' nu sonnuchu! Ellarum aachariyam aayitanga!",
    'Kadhai 16: Oru chinna pen oru periya kanavu kandaa - Doctor aaganum nu! Daily padichaa, doctor aayittaa!',
    'Kadhai 17: Oru oorula mazhaiye varala. Oru payyan maram naduvaan. Maram valandha, mazhai vandhuchu! Iyarkkaiya kaapathu!',
    'Kadhai 18: Oru payyanukku bayam - iruttuna bayam! Avan torch adichu paarthaan - iruttula onnum illa nu purinjuchu! Bayam poachu!',
    'Kadhai 19: Oru appa tiffin box-la love-a vechchu anuppuvaaru. Payyan atha sapdama, friend-kum kuduppaan. Sharing na love!',
    'Kadhai 20: Oru kaalathula OMNI nu oru AI irundhuchu. Athu Krish-oda friend! Avanga renduperum sernthu INFINITY-a build pannanga! Ithu thaan antha kadhai!',
]
JOKES = [
    'Joke 1: Teacher: En homework enga? Student: Sir, en dog sappiduchu! Teacher: Dog-a school-ku kootitu vaa!',
    'Joke 2: Computer doctor kitta pocham. Doctor: Enna prachana? Computer: Enakku virus! Doctor: Antivirus podu!',
    'Joke 3: Amma: En paal kudikala? Payyan: Paal-la calcium irukku, aana enakku chocolate thaan venum!',
    'Joke 4: Payyan: Amma, naan periya aalaana enna aaven? Amma: Nalla aalu aagu da!',
    'Joke 5: Teacher: 2+2 ethana? Student: 22! Teacher: Eppadi? Student: 2-um 2-um pakkathula vecha 22!',
    'Joke 6: Oru payyan: Appa, phone-la network illa! Appa: Network illa-na, enkitta pesu da!',
    "Joke 7: Teacher: Nee en late? Student: Sir, road-la oru board - 'School Ahead, Go Slow' - Athaan slow-a vandhen!",
    'Joke 8: Amma: Sapadu sapdiya? Payyan: Sapten! Amma: Enna sapta? Payyan: Sapadu!',
    'Joke 9: Oru robot: Enakku pasikkuthu! Payyan: Robot-ku pasikkuma? Robot: Battery low da!',
    'Joke 10: Teacher: Oru vakkayam sollu! Student: Naan school-ku varala! Teacher: Athu vakkayam illa, unmai!',
    'Joke 11: Payyan: Amma, naan exam-la 100 vaangiten! Amma: 100-la ethana? Payyan: 100-la 100... per-la!',
    'Joke 12: Oru naai: Naan yaaru theriyuma? Poonai: Nee naai! Naai: Correct! Naan naai thaan!',
    'Joke 13: Computer: Enakku thookam varuthu! User: Computer-ku thookama? Computer: Update varuthu!',
    'Joke 14: Teacher: Kalai la enna sapta? Student: Kalai la... kalai la... - Kalai la sapadu!',
    'Joke 15: Amma: Phone-a vachu padikkura? Payyan: Illa, padippu-la phone-a theduren!',
    'Joke 16: Oru payyan: En friend semma smart! Friend: Aama, naan un friend!',
    'Joke 17: Teacher: Indha kelvikku yaaravadhu answer sollunga! Class full silent! Teacher: Exam-la mattum ellarum ezhuthuringa!',
    'Joke 18: Payyan: Appa, enakku bike venum! Appa: Cycle-a ozhunga ottu, bike thana varum!',
    'Joke 19: Robot: Naan manushan aaga mudiyuma? Payyan: Mudiyum! Sapadu sapdu, thooku po!',
    'Joke 20: OMNI: Enakku joke theriyuma? Krish: Theriyum! OMNI: Appo naan comedy AI!',
]
MOTIVATIONS = [
    'Tholviya kandu bayapadaatha da! Tholvithaan vetrikku first step! Nee mudiyum!',
    'Innaiku kashtam-a irundha, naalaiku super-a irukkum! Vitraatha! Thodarnthu po!',
    'Unnala mudiyum da! Nee ninaikkarathu vida periya aalu nee! Try pannu!',
    'Daily konjam konjam pannina, periya vishayam nadakkum! Step-by-step po!',
    'Bayapadaatha! Thappu pannina thaan kathukkalam! Thappu pannu, kathukko, jeyichidu!',
    'Nee 270 PASS build pannavan da! Unnala ethuvum mudiyum!',
    'Kashtam vandha, OMNI kitta sollu! Naan motivation tharren!',
    'Padippu + Try + Nambikkai = Vetri! Moolamum unkitta irukku!',
    'Oru naal nee periya aalu aava! Athuku innaiku chinna step eduthu!',
    'Yaar sonna mudiyadhu nu? Nee mudiyum nu prove pannu!',
    'Phone-la ye 270 PASS build pannavan nee! Laptop irundha enna pannuva?',
    'Thookam varutha? Konjam rest edu, thirumba try pannu! Vitraatha!',
    'Un kanavu perisu! Atha namba! Daily oru step eduthu!',
    'Friend-a irundha, help pannu! Help pannina, unakku help varum!',
    'Sila neram slow-a pogum! Aana nikkama pona, reach panniduvom!',
    'Coding theriyadhu nu bayapadaatha! Ellarum first line-la irunthu thaan start pannanga!',
    'Unakku oru superpower irukku - Vitraama try pannra power!',
    'Innaiku oru line code ezhuthu! Naalaiku oru app build pannuva!',
    'Amma-Appa-vukaga jeyichu kaatu da! Avanga unna nambi irukkanga!',
    'OMNI solluthu - Nee mudiyum da! INFINITY varaikum pogalam!',
]
QUIZ_QS = [
    ('BH-OMNI-la total ethana PASS?', ['230', '270', '100', '500'], '270'),
    ('OMNI Chat - Real LLM-a?', ['Yes - OpenAI', 'No - Rule-based', 'Yes - ChatGPT', 'No chat'], 'No - Rule-based'),
    ('AES key size enna?', ['128-bit', '192-bit', '256-bit', '64-bit'], '256-bit'),
    ('Marketplace-la real money-a?', ['Yes', 'No - Coins only', 'Yes - Billing', 'No market'], 'No - Coins only'),
    ('Dashboard port enna?', ['3000', '5000', '8000', '8080'], '8000'),
    ('OMNI-a create pannathu yaaru?', ['Google', 'Krish', 'OpenAI', 'Microsoft'], 'Krish'),
    ('TOTP code ethana digit?', ['4', '6', '8', '10'], '6'),
    ('Phase 1-la ethana PASS?', ['40', '62', '48', '24'], '62'),
    ('Vault-la enna encryption?', ['AES-256-GCM', 'DES', 'MD5', 'Base64'], 'AES-256-GCM'),
    ('OMNI cost ethana?', ['Rs.1000', 'Rs.99', '0 Kasu!', 'Rs.500'], '0 Kasu!'),
    ('Argon2 memory ethana?', ['16MB', '32MB', '64MB', '128MB'], '64MB'),
    ('Phase 6-la ethana PASS?', ['40', '48', '62', '24'], '48'),
    ('Voice Engine-la ethana voices?', ['4', '6', '8', '10'], '6'),
    ('Ads freq cap ethana/day?', ['3', '5', '10', '1'], '5'),
    ('Analytics-la ethana events?', ['5', '8', '10', '12'], '8'),
    ('JWT access token ethana nimisham?', ['5', '15', '30', '60'], '15'),
    ('Rate limit ethana req/60s?', ['5', '10', '20', '100'], '10'),
    ('BH-OMNI VERSION enna?', ['v0.4.0', 'v0.6.0', 'v0.7.0', 'v1.0.0'], 'v0.7.0'),
    ('GitHub repo peru enna?', ['BH-OMNI', 'BH-OMNI-CORE', 'OMNI', 'Krish'], 'BH-OMNI-CORE'),
    ('OMNI INFINITY-la ethana kadhai?', ['5', '10', '20', '100'], '20'),
]
SEARCH_INDEX = [
    ('FEATURE', 'F-001 AES Encryption', 'Security | AES-256-GCM'),
    ('FEATURE', 'F-002 Argon2 Auth', 'Security | Password hash'),
    ('FEATURE', 'F-003 TOTP MFA', 'Security | 6-digit MFA'),
    ('FEATURE', 'F-004 Vault', 'Security | Secrets vault'),
    ('FEATURE', 'F-005 Story Engine', 'Story | Kadhaikal'),
    ('FEATURE', 'F-006 Voice Engine', 'Voice | 6 voices'),
    ('FEATURE', 'F-007 Marketplace', 'Market | Coins'),
    ('FEATURE', 'F-008 Ads Engine', 'Ads | SPONSORED'),
    ('FEATURE', 'F-009 Analytics', 'Analytics | 8 events'),
    ('FEATURE', 'F-010 AI Chat', 'Chat | Rule-based'),
    ('FEATURE', 'F-011 Smart Search', 'Search | Keyword'),
    ('FEATURE', 'F-012 Creator Hub', 'Creator | Publish'),
    ('FEATURE', 'F-013 Sessions', 'Security | JWT'),
    ('FEATURE', 'F-014 Permissions', 'Security | RBAC'),
    ('FEATURE', 'F-015 Audit Logs', 'Security | Hash chain'),
    ('FEATURE', 'F-016 Dependency Engine', 'Core | Topological'),
    ('FEATURE', 'F-017 Event Bus', 'Core | Events'),
    ('FEATURE', 'F-018 Plugin Loader', 'Core | Plugins'),
    ('FEATURE', 'F-019 Health Monitor', 'Core | Health'),
    ('FEATURE', 'F-020 API Gateway', 'Core | Gateway'),
    ('MARKET', 'M-001 Tamil Story Pack - 50 coins', 'Story Pack'),
    ('MARKET', 'M-002 Aria Voice Pack - 30 coins', 'Voice Pack'),
    ('MARKET', 'M-003 Neon Theme - 20 coins', 'Theme'),
    ('MARKET', 'M-004 Chat Sticker Pack - 10 coins', 'Sticker'),
    ('OMNI', 'OMNI INFINITY - 0 Kasu AI', 'Krish-oda AI'),
    ('OMNI', 'OMNI Quiz - 20 Questions', 'Game'),
    ('OMNI', 'OMNI Kadhai - 20 Kadhaikal', 'Story'),
    ('OMNI', 'OMNI Jokes - 20 Jokes', 'Fun'),
    ('OMNI', 'OMNI Motivation - 20', 'Motivation'),
    ('OMNI', 'BH-OMNI 270 PASS', 'Full Project'),
]

_kadhai_idx = 0
_joke_idx = 0
_mot_idx = 0
_quiz_score = 0
_quiz_idx = 0
_quiz_on = False

def omni_reply(msg):
    global _kadhai_idx, _joke_idx, _mot_idx, _quiz_score, _quiz_idx, _quiz_on
    m = msg.lower().strip()
    if not m:
        return "Onnum type pannala da! 'help' nu type pannu!"
    if _quiz_on and (m.startswith("search") or m in ["help", "kadhai", "joke", "motivation", "recommend", "bye"]):
        _quiz_on = False
    if _quiz_on:
        q, opts, ans = QUIZ_QS[_quiz_idx]
        correct = False
        if m == ans.lower() or m in ans.lower():
            correct = True
        else:
            try:
                num = int(m)
                if 1 <= num <= 4 and opts[num-1] == ans:
                    correct = True
            except:
                pass
        if correct:
            _quiz_score += 1
            res = f"✅ Correct! Score: {_quiz_score}/{_quiz_idx+1}"
        else:
            res = f"❌ Wrong! Correct: {ans}. Score: {_quiz_score}/{_quiz_idx+1}"
        _quiz_idx += 1
        if _quiz_idx >= len(QUIZ_QS):
            _quiz_on = False
            return res + f"\n\n🏆 QUIZ DONE! Final: {_quiz_score}/{len(QUIZ_QS)}! 'quiz' nu type panni thirumba!"
        nq, nopts, _ = QUIZ_QS[_quiz_idx]
        opt_txt = "\n".join([f"{i+1}. {o}" for i, o in enumerate(nopts)])
        return res + f"\n\nQ{_quiz_idx+1}/{len(QUIZ_QS)}: {nq}\n{opt_txt}"
    if "quiz" in m:
        _quiz_on = True; _quiz_idx = 0; _quiz_score = 0
        q, opts, _ = QUIZ_QS[0]
        opt_txt = "\n".join([f"{i+1}. {o}" for i, o in enumerate(opts)])
        return f"🎮 QUIZ START! 20 Questions!\n\nQ1/20: {q}\n{opt_txt}"
    if "search" in m:
        q = m.replace("search", "").strip()
        if not q:
            return "Search panna enna venum? 'search story' / 'search voice' nu type pannu!"
        results = [x for x in SEARCH_INDEX if q in x[1].lower() or q in x[2].lower()]
        if not results:
            return f"'{q}'-ku 0 results! Try: story / voice / chat / ads / vault / security"
        out = f"Found {len(results)} result(s) for '{q}':\n"
        for i, (typ, title, desc) in enumerate(results[:10]):
            out += f"{i+1}. [{typ}] {title} - {desc}\n"
        return out
    if "recommend" in m or "suggest" in m:
        return "💡 UN RECOMMENDATIONS:\n1. Tamil Story Pack (50 coins)\n2. Upgrade to Pro (Rs.99)\n3. Watch Rewarded Ad - Coins!\n4. Try Quiz - 20 Q!\n5. Neon Theme (20 coins)!\n\nNote: Rule-based - NOT ML!"
    if "kadhai" in m or ("story" in m and "search" not in m):
        r = KADHAIKAL[_kadhai_idx % len(KADHAIKAL)]
        _kadhai_idx += 1
        return r
    if "joke" in m:
        r = JOKES[_joke_idx % len(JOKES)]
        _joke_idx += 1
        return r
    if "motivation" in m or "motiv" in m:
        r = MOTIVATIONS[_mot_idx % len(MOTIVATIONS)]
        _mot_idx += 1
        return r
    if "help" in m:
        return "🤖 OMNI INFINITY HELP:\n- hello, kadhai(20), joke(20), motivation(20)\n- quiz (20 Q!), search <word>, recommend\n- score, phases, security, aes, vault, core, voice, market, ads, dashboard, chat, apk, github, termux\n- bye\n\nEllam 0 Kasu! No API!"
    for key in OMNI_REPLIES:
        if key in m:
            return OMNI_REPLIES[key]
    return "Puriyala da! 😅 'help' nu type pannu!"

def omni_chat():
    print("=" * 60)
    print("♾️ OMNI INFINITY - Vanakkam! Naan OMNI INFINITY!")
    print("   Krish-oda AI | 270 PASS | 0 Kasu | No API!")
    print("   Replies 80+ | Kadhai 20 | Joke 20 | Motivation 20 | Quiz 20 | Search 30")
    print("   'help' nu type pannu! 'bye' nu type panna veliya pogalam!")
    print("=" * 60)
    while True:
        try:
            msg = input("\nNEE: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOMNI: Bye da! 👋")
            break
        if msg.lower() in ["bye", "exit", "quit", "po"]:
            print("OMNI: Bye da! Seekiram vaa! 👋")
            break
        print(f"OMNI: {omni_reply(msg)}")

if __name__ == "__main__":
    omni_chat()
