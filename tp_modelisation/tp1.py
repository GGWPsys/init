from pathlib import Path
import json
import csv
import os
import sys
from typing import Dict, Any

class Livre:
    def __init__(self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn

    def __str__(self):
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn})"
    
class LivreNumerique(Livre):
    def __init__(self, titre, auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def __str__(self):
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn}, {self.taille_fichier} Mo)"
    
class Bibliotheque:
    def __init__(self):
        self.livres = []

    def ajouter_livre(self, livre):
        self.livres.append(livre)
        print(f"Livre '{livre.titre}' ajouté à la bibliothèque.")

    def supprimer_livre_par_isbn(self, isbn):
        for livre in self.livres:
            if livre.isbn == isbn:
                self.livres.remove(livre)
                print(f"Livre '{livre.titre}' supprimé.")
                return
        print("Livre non trouvé.")

    def rechercher_par_titre(self, titre):
        resultats = [livre for livre in self.livres if titre.lower() in livre.titre.lower()]
        return resultats
    
    def rechercher_par_auteur(self, auteur):
        resultats = [livre for livre in self.livres if auteur.lower() in livre.auteur.lower()]
        return resultats

if __name__ == "__main__":
    biblio = Bibliotheque()

    livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123456")
    livre2 = LivreNumerique("Python pour les nuls", "Jean Dupont", "987654", 5)

    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    print("\nRecherche par titre 'Python':")
    for livre in biblio.rechercher_par_titre("Python"):
        print(livre)

    print("\nRecherche par auteur 'Antoine':")
    for livre in biblio.rechercher_par_auteur("Antoine"):
        print(livre)

    biblio.supprimer_livre_par_isbn("123456")

    # final
    ROOT = Path(__file__).resolve().parent.parent
    json_path = ROOT / "data" / "bibliotheque.json"
    csv_path = ROOT / "data" / "catalogue.csv"

    def _serialize_livre(livre: Livre) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": "LivreNumerique" if isinstance(livre, LivreNumerique) else "Livre",
            "titre": livre.titre,
            "auteur": livre.auteur,
            "isbn": livre.isbn,
        }
        if isinstance(livre, LivreNumerique):
            d["taille_fichier"] = getattr(livre, "taille_fichier", None)
        return d

    def save_bibliotheque_json(path: Path, biblio: Bibliotheque) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            data = [_serialize_livre(item) for item in biblio.livres]
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Sauvegarde JSON écrite : {path}")
        except PermissionError:
            print(f"Erreur : permissions insuffisantes pour écrire {path}")
            raise

    def load_bibliotheque_json(path: Path) -> Bibliotheque:
        b = Bibliotheque()
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Le JSON doit contenir une liste d'objets représentant des livres.")
            for item in data:
                if isinstance(item, dict):
                    if item.get("type") == "LivreNumerique":
                        livre = LivreNumerique(item.get("titre", ""), item.get("auteur", ""), item.get("isbn", ""), item.get("taille_fichier", 0))
                    else:
                        livre = Livre(item.get("titre", ""), item.get("auteur", ""), item.get("isbn", ""))
                    b.ajouter_livre(livre)
            print(f"Chargement JSON réussi ({len(b.livres)} livres) depuis {path}")
            return b
        except FileNotFoundError:
            print(f"Fichier non trouvé : {path}")
            raise
        except json.JSONDecodeError:
            print(f"Erreur : JSON invalide dans {path}")
            raise
        except PermissionError:
            print(f"Erreur : permissions insuffisantes pour lire {path}")
            raise

    def export_catalogue_csv(path: Path, biblio: Bibliotheque) -> None:
        try:
            if not biblio.livres:
                print("Aucun livre à exporter.")
                return
            fieldnames = ["type", "titre", "auteur", "isbn", "taille_fichier"]
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for livre in biblio.livres:
                    writer.writerow({
                        "type": "LivreNumerique" if isinstance(livre, LivreNumerique) else "Livre",
                        "titre": livre.titre,
                        "auteur": livre.auteur,
                        "isbn": livre.isbn,
                        "taille_fichier": getattr(livre, "taille_fichier", ""),
                    })
            print(f"Export CSV réalisé : {path}")
        except PermissionError:
            print(f"Erreur : permissions insuffisantes pour écrire {path}")
            raise

    try:
        save_bibliotheque_json(json_path, biblio)
        export_catalogue_csv(csv_path, biblio)
    except Exception:
        print("Une erreur est survenue lors de la sauvegarde/export.")

    consignes_path = Path(__file__).resolve().parent / "consignes.png"
    if consignes_path.exists():
        try:
            if os.name == 'nt':
                os.startfile(consignes_path)
            else:
                opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                os.system(f"{opener} '{consignes_path}'")
        except Exception:
            print(f"Impossible d'ouvrir l'image {consignes_path}, mais elle est présente.")
    else:
        print(f"Pour afficher les consignes (image), placez 'consignes.png' dans {Path(__file__).resolve().parent}")