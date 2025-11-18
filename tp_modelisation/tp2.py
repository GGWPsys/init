etudiants = [
    {"nom": "Alice", "note": 15, "annee": 2},
    {"nom": "Bob", "note": 12, "annee": 1},
    {"nom": "Charlie", "note": 18, "annee": 2}
]

etudiants_admis = [
    etudiant for etudiant in etudiants 
    if etudiant["note"] >= 12
]

print("Étudiants admis :")
print(etudiants_admis)

# 2. Calculer la moyenne
notes_par_annee = {}
for etudiant in etudiants:
    annee = etudiant["annee"]
    note = etudiant["note"]
    
    if annee not in notes_par_annee:
        notes_par_annee[annee] = []
        
    notes_par_annee[annee].append(note)

moyenne_par_annee = {}
for annee, notes in notes_par_annee.items():

    moyenne = sum(notes) / len(notes)
    moyenne_par_annee[annee] = moyenne

print("\nMoyenne par année :")
print(moyenne_par_annee)

# 3. Créer un dictionnaire
def obtenir_mention(note):
    if note >= 16:
        return "Très Bien (TB)"
    elif note >= 14:
        return "Bien (B)"
    elif note >= 12:
        return "Assez Bien (AB)"
    else:
        return "Échec (Fail)"

mentions_etudiants = {
    etudiant["nom"]: obtenir_mention(etudiant["note"])
    for etudiant in etudiants
}

print("\nDictionnaire nom -> mention :")
print(mentions_etudiants)