import argparse
from pathlib import Path
import os
import sys
from src import models
from src import file_manager
from src import exceptions as exc

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
JSON_PATH = DATA_DIR / "bibliotheque.json"
CSV_PATH = DATA_DIR / "catalogue.csv"
CONSIGNES_IMG = Path(__file__).resolve().parent / "consignes.png"

def build_arg_parser():
    p = argparse.ArgumentParser(description="Mini-gestionnaire de bibliothèque")
    p.add_argument("--init", action="store_true", help="Créer une biblio d'exemple et l'enregistrer")
    p.add_argument("--load", action="store_true", help="Charger et afficher la biblio")
    p.add_argument("--add", action="store_true", help="Ajouter un livre (nécessite --titre --auteur --isbn)")
    p.add_argument("--remove", action="store_true", help="Supprimer un livre (nécessite --isbn)")
    p.add_argument("--titre", type=str)
    p.add_argument("--auteur", type=str)
    p.add_argument("--isbn", type=str)
    p.add_argument("--taille", type=float, help="Taille fichier pour livre numérique")
    p.add_argument("--no-open-image", action="store_true", help="Ne pas ouvrir l'image des consignes")
    return p

def print_summary(biblio: models.Bibliotheque):
    print(f"Nombre de livres : {len(biblio.livres)}")
    for livre in biblio.livres:
        print("-", livre)

def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    fm = file_manager.FileManager(JSON_PATH)

    if args.init:
        b = models.sample_bibliotheque()
        fm.save(b)
        print("Bibliothèque d'exemple créée.")
        return 0

    try:
        biblio = fm.load()
    except exc.FichierNonTrouve:
        print("Aucun fichier trouvé, création d'une bibliothèque d'exemple.")
        biblio = models.sample_bibliotheque()
        fm.save(biblio)
    except exc.FormatInvalide:
        print("Le fichier JSON est invalide. Utilisez --init pour le réinitialiser.")
        return 2
    except exc.PermissionInsuffisante:
        print("Permissions insuffisantes pour lire le fichier.")
        return 3
    
    if args.add:
        if not (args.titre and args.auteur and args.isbn):
            print("Pour ajouter un livre, précisez --titre --auteur --isbn")
            return 4
        if args.taille is not None:
            livre = models.LivreNumerique(args.titre, args.auteur, args.isbn, args.taille)
        else:
            livre = models.Livre(args.titre, args.auteur, args.isbn)
        biblio.ajouter_livre(livre)
        fm.save(biblio)
        print("Livre ajouté.")
        return 0

    if args.remove:
        if not args.isbn:
            print("Précisez --isbn pour supprimer.")
            return 5
        removed = biblio.supprimer_livre_par_isbn(args.isbn)
        if removed:
            fm.save(biblio)
            print("Livre supprimé.")
        else:
            print("ISBN non trouvé.")
        return 0

    if args.load:
        print_summary(biblio)

    if args.export:
        try:
            fm.export_csv(biblio, CSV_PATH)
            print("Export CSV effectué :", CSV_PATH)
        except exc.PermissionInsuffisante:
            print("Impossible d'écrire le CSV : permissions insuffisantes.")
            return 6

    if not args.no_open_image and CONSIGNES_IMG.exists():
        try:
            if os.name == "nt":
                os.startfile(CONSIGNES_IMG)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                os.system(f"{opener} '{CONSIGNES_IMG}'")
        except Exception:
            print("Impossible d'ouvrir l'image des consignes (problème d'ouverture).")

    elif not current_user.is_admin:
                choice = show_user_menu(current_user)
                if choice == '1': handle_search()
                elif choice == '2': handle_borrow()
                elif choice == '3': handle_return()
                elif choice == '4': 
                    # Fonctionnalité de réservation
                    book_id = input("ID du livre à réserver: ")
                    try:
                        user_manager.reserve_book(current_user.user_id, book_id)
                        print("\n Réservation enregistrée. Vous serez notifié lorsque le livre sera disponible.")
                    except Exception as e:
                        print(f"\n Erreur de réservation: {e}")
                elif choice == '5': handle_pay_penalties()
                elif choice == '6':
                    print(f"Déconnexion de {current_user.username}.")
                    current_user = None
                else: print("Option invalide ou non implémentée.")
            
            # admin
    else:
                choice = show_user_menu(current_user)
                if choice == '1': handle_search()
                elif choice == '2': handle_admin_manage_books()
                elif choice == '3':
                    print(f"Déconnexion de l'Administrateur {current_user.username}.")
                    current_user = None
                else: print("Option invalide ou non implémentée.")
                
                except KeyboardInterrupt:
            print("\nInterruption de l'utilisateur. Sauvegarde et sortie.")
            storage_service.save_data()
            sys.exit(0)
            except Exception as e:
            print(f"\nUne erreur critique est survenue: {e}")
            
    return 0

try:
    manager = LibraryManager()
except Exception as e:
    print(f"Erreur critique lors de l'initialisation du LibraryManager: {e}")
    manager = None

def show_login_menu():
    print("\n--- Connexion ---")
    username = input("Nom d'utilisateur: ")
    if not username: return None, None
    password = input("Mot de passe: ")
    return username, password

def show_user_menu(user: User):
    print(f"\n--- Menu Utilisateur ({user.username}) ---")
    print("1: Rechercher un livre")
    print("2: Emprunter un exemplaire")
    print("3: Retourner un exemplaire")
    print("4: Réserver un livre (si emprunté)")
    print("5: Payer les pénalités ({:.2f}€)".format(user.current_penalties))
    print("6: Déconnexion")
    return input("Votre choix: ")

def show_admin_menu(user: User):
    print(f"\n--- Menu Administrateur ({user.username}) ---")
    print("1: Rechercher un livre")
    print("2: Gérer Livres/Exemplaires (Ajout/Suppression)")
    print("3: Voir Statistiques (Non implémenté)")
    print("4: Déconnexion")
    return input("Votre choix: ")

def handle_admin_manage_books():
    print("Fonction de gestion admin non implémentée (Utilisez --add-book CLI pour l'instant).")
    
def handle_search():
    print("Fonction de recherche non implémentée.")

def handle_borrow(user: User):
    copy_id = input("ID de l'exemplaire à emprunter: ")
    try:
        loan = manager.borrow_copy(user.user_id, copy_id)
        print(f"\n Emprunt réussi ! Prêt ID: {loan.loan_id}. Retour avant le: {loan.due_date}")
    except exc.ErreurBibliotheque as e:
        print(f"\n Erreur d'emprunt: {e}")

def handle_return(user: User):
    loan_id = input("ID du prêt (Loan ID) à retourner: ")
    try:
        loan = manager.return_copy(loan_id)
        penalty = loan.calculate_penalty_amount()
        if penalty > 0:
            print(f"\n Retour effectué avec {penalty}€ de pénalités de retard. Votre solde est mis à jour.")
        else:
            print("\n Retour effectué à temps. Aucune pénalité.")
    except exc.ErreurBibliotheque as e:
        print(f"\n Erreur de retour: {e}")

def handle_pay_penalties(user: User):
    if user.current_penalties <= 0:
        print("Vous n'avez aucune pénalité à payer.")
        return
    
    print(f"Paiement de {user.current_penalties:.2f}€ effectué (Simulation).")
    user.current_penalties = 0.0
    manager.storage.save_object(user)
    manager.save_data()
    print(" Pénalités réglées. Vous pouvez maintenant emprunter de nouveau.")

if __name__ == "__main__":
    raise SystemExit(main())






