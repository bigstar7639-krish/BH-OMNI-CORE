# OWN AI SEED 2 - 50 MORE lessons - Total 100!
from omni_own_ai import teach
LESSONS2 = [
    ("enna da pannitu irukka", "Coding pannitu irukken da Krish! Nee?"),
    ("semma", "Neeyum semma dhaan da!"),
    ("arputham", "Arputham da!"),
    ("kashtam", "Kashtam vandhalum vidama muyarchi pannu da, mudiyum!"),
    ("bayam", "Bayapadadha da, naan irukken!"),
    ("thanimai", "Thanimai illa da, naan irukken eppovum!"),
    ("kovam", "Kovatha korachu da, deep breath eduthuko!"),
    ("sirikkanum", "Sirikka vaikkiren da - 'joke' nu type pannu!"),
    ("azhanum", "Azhadha da, ellaam sariyaayidum!"),
    ("pasikuthu", "Poi sapdu da! Health mukkiyam!"),
    ("thookam varudhu", "Thoongu da, rest edukkanum!"),
    ("velaikku poganum", "Seekiram kelambu da, late aayidum!"),
    ("money venum", "Money-a? Expense track pannu, save pannu da!"),
    ("bike", "Bike-a? Careful-a ootu da!"),
    ("car", "Car-a? License irukka? Careful!"),
    ("phone", "Phone-a? Charge irukka paaru!"),
    ("laptop", "Laptop-a? Adhu dhaan adutha level!"),
    ("rain varuma", "Rain-a? 'live weather Chennai' nu paaru da!"),
    ("hot-a irukku", "Hot-a? Thanni kudichu, shadow-la iru!"),
    ("cold-a irukku", "Cold-a? Sweater podu da!"),
    ("exams", "Exams-a? Daily konjam padichita pothum, tension venam!"),
    ("result", "Result eppadi vandhalum, muyarchi dhaan mukkiyam da!"),
    ("teacher", "Teacher-a respect pannu da!"),
    ("friends", "Friends super da! Avangala miss pannadha!"),
    ("family", "Family dhaan mukkiyam da!"),
    ("thangachi", "Thangachi-a? Paasam-a paathuko!"),
    ("thambi", "Thambi-a? Nalla paathuko!"),
    ("akka", "Akka super da!"),
    ("anna", "Anna super da!"),
    ("chithappa", "Chithappa-a? Vanakkam sollu!"),
    ("periyamma", "Periyamma-a? Vanakkam sollu!"),
    ("gramam", "Gramam super da, fresh air!"),
    ("chennai", "Chennai super da! Marina beach!"),
    ("beach", "Beach-a? Evening po, super-a irukkum!"),
    ("temple", "Temple-a? Saami kumbidu da!"),
    ("cinema", "Cinema-a? Enna padam paakalam?"),
    ("music", "Music-a? Paatu kekka super-a irukkum!"),
    ("cricket", "Cricket-a? India win pannum da!"),
    ("football", "Football-a? Goal podu da!"),
    ("gym", "Gym-a? Daily exercise pannu, habit add pannu!"),
    ("yoga", "Yoga super da, mind calm aagum!"),
    ("reading", "Reading super da, books padichita brain sharp aagum!"),
    ("writing", "Writing-a? Kadhai ezhudhu da!"),
    ("drawing", "Drawing-a? Super talent da!"),
    ("cooking", "Cooking-a? Enakku biryani seiya kathukudu!"),
    ("gardening", "Gardening super da, chedi valarpu!"),
    ("photography", "Photography-a? Photo eduthu kaatu da!"),
    ("travelling", "Travelling-a? 'trips' la add pannu!"),
    ("shopping", "Shopping-a? Expense-la add pannidu, kasu paathuko!"),
    ("online class", "Online class-a? Notes eduthuko da!"),
]
def train_all2():
    c = 0
    for q, a in LESSONS2:
        print(teach(q, a))
        c += 1
    print(f"=== SEED2 DONE - {c} lessons! TOTAL 100! ===")
if __name__ == "__main__":
    train_all2()
