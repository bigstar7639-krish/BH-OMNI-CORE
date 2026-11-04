# OMNI POETRY - Phase 21 Step 1 - SAME PROJECT
# Category 26 - Creative - Template poems, NOT real LLM
POEMS = {
    "friend": "Nanban endral uyir thozhan,\nKashtam vandhalum kai koduppan,\nSirippu vandhalum serndhu sirippan!",
    "amma": "Amma endral anbu kadal,\nThunbam vandhalum thunai nippal,\nUlagam muzhudhum aval anbu!",
    "dream": "Kanavu kaanu da, perusa kaanu,\nMuyarchi pannu, mudiyum da,\nNaalaiku un naal dhaan!",
    "rain": "Mazhai vandhal manvasam,\nBoomi engum santhosam,\nKulir kaatru, pudhu vazhkai!",
}

def handle_poem(msg):
    m = msg.strip().lower()
    if m.startswith("poem "):
        topic = msg.strip()[5:].strip().lower()
        if topic in POEMS:
            return f"📝 POEM - {topic}:\n{POEMS[topic]}"
        return f"📝 POEM: '{topic}' - topics: {', '.join(POEMS.keys())}"
    if m in ["poem", "poems", "poem list"]:
        return "📝 OMNI POEMS:\n" + "\n".join(f"- {k}" for k in POEMS.keys())
    return None
