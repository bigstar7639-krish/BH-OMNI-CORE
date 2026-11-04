# OMNI BOOKS - Cat 06 - Gutenberg FREE API, NO key
import urllib.request, urllib.parse, json
def search_books(q):
    try:
        url = f"https://gutendex.com/books/?search={urllib.parse.quote(q)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read().decode())
            if not d.get("results"):
                return f"📚 BOOKS: '{q}' - onnum kedaikala da!"
            out = f"📚 BOOKS - '{q}' (Gutenberg FREE):\n"
            for b in d["results"][:3]:
                out += f"- {b['title']} - {', '.join([a['name'] for a in b['authors']])}\n"
            return out
    except Exception as e:
        return f"📚 BOOKS OFFLINE - Internet illa ({e})\nOffline: Gutenberg.org la paaru da!"
def handle_books(msg):
    m = msg.strip().lower()
    if m.startswith("book "):
        return search_books(msg.strip()[5:].strip())
    if m in ["books", "book list"]:
        return "📚 BOOKS: 'book tamil' / 'book python' nu try pannu da! Source: Gutenberg FREE"
    return None
