# OMNI MEGA FULL - Phase 36 - En kitta irundha FULL content!
# Jokes + Kadhai + Motivation + Quiz + Tips - Ellaam ore file-la!
MEGA_JOKES = [
    "Teacher: Yen late? Student: Alarm-a naane off panniten miss!",
    "Krish: En phone hang aayiduchu! Phone: Nee dhaan enna hang pannura!",
    "Amma: Saptiya? Krish: Sapten! Amma: Poi solladha, plate-la sapadu irukku!",
    "Coding pannum podhu bug varadhu normal - bug illana dhaan bayapadanum!",
    "WiFi slow-na, manasu slow aayidum!",
    "Exam-ku night full-a padicha, morning full-a marandhuvom!",
    "Battery 1% - appo dhaan mukkiyamana velai varum!",
    "Alarm vaikum podhu brave, morning-la coward!",
    "Biriyani paatha manasu, diet-a marandhuvom!",
    "Rain varum podhu dhaan bike-la poganum-nu thonum!",
]
MEGA_KADHAI = [
    "Oru chinna payyan, periya kanavu kanden. Daily chinna step eduthan, oru naal periya aal aayitan!",
    "Oru kaatula oru singam, oru eli. Eli help pannuchu, singam friendship-a marakkala!",
    "Krish-nu oru payyan, thanakku oru AI create pannanumnu aasaipattan. 0 kasu-la start panni, thanoda OWN AI-ya create pannitan!",
    "Oru farmer, daily velaikku ponan. Mazhai varala, aana avan nambikkaiya vittu kodukkala. Oru naal mazhai vandhuchu!",
    "Oru student, exam-la fail aayitan. Azhala, thirumba muyarchi pannan. Next exam-la topper aayitan!",
]
MEGA_MOTIVATION = [
    "Innaiku nee edutha chinna step, naalaiku un periya victory!",
    "1000 miles journey-um, oru chinna step-la dhaan start aagum!",
    "Unna nambi nee muyarchi pannu, ulagam unna nambum!",
    "Fail aana, adhu mudivu illa - adhu oru lesson!",
    "Krish - nee create pannadhu, un kaiyala dhaan mudiyum! Vera yaaralayum mudiyadhu!",
]
MEGA_QUIZ = [
    ("Tamil Nadu capital enna?", "Chennai"),
    ("India capital enna?", "Delhi"),
    ("2 + 2 = ?", "4"),
    ("Python-a create pannadhu yaaru?", "Guido van Rossum"),
    ("BH-OMNI CORE-a create pannadhu yaaru?", "Krish"),
    ("Own AI-na enna?", "100% own, no API"),
    ("Chennai-la famous beach enna?", "Marina"),
    ("7 * 8 = ?", "56"),
    ("Water formula enna?", "H2O"),
    ("Sun rise aagura side enna?", "East"),
]
MEGA_TIPS = {
    "study": "Study tip: 25 min padippu, 5 min break - Pomodoro!",
    "health": "Health tip: Daily 8 glass thanni, 7 hours thoongu!",
    "money": "Money tip: Varavu-la 20% save pannu, expense track pannu!",
    "coding": "Coding tip: Daily 1 chinna program ezhudhu, perusa aayiduvai!",
    "life": "Life tip: Kovatha korachu, sirichu pesu, ellam sariyaayidum!",
}
def get_mega_joke(n=0):
    import random
    return "😂 MEGA JOKE:\n" + random.choice(MEGA_JOKES)
def get_mega_kadhai(n=0):
    import random
    return "📖 MEGA KADHAI:\n" + random.choice(MEGA_KADHAI)
def get_mega_motivation():
    import random
    return "💪 MEGA MOTIVATION:\n" + random.choice(MEGA_MOTIVATION)
def get_mega_quiz():
    import random
    q, a = random.choice(MEGA_QUIZ)
    return f"🎮 MEGA QUIZ:\nQ: {q}\nA: {a}"
def handle_mega(msg):
    m = msg.strip().lower()
    if m in ["mega joke", "mega jokes"]:
        return get_mega_joke()
    if m in ["mega kadhai", "mega story"]:
        return get_mega_kadhai()
    if m in ["mega motivation", "mega motivate"]:
        return get_mega_motivation()
    if m in ["mega quiz"]:
        return get_mega_quiz()
    if m.startswith("mega tip "):
        t = msg.strip()[9:].strip().lower()
        if t in MEGA_TIPS:
            return f"💡 MEGA TIP - {t}:\n{MEGA_TIPS[t]}"
        return f"💡 MEGA TIPS: {', '.join(MEGA_TIPS.keys())}"
    if m == "mega":
        return "🌟 OMNI MEGA FULL:\n- mega joke\n- mega kadhai\n- mega motivation\n- mega quiz\n- mega tip <topic>\nEn kitta irundha FULL content idhu dhaan da!"
    return None
