class ErreurBibliotheque(Exception):
    pass

class LivreNonTrouveErreur(ErreurBibliotheque):
    def __init__(self, isbn):
        self.isbn = isbn
        self.message = f"Livre avec ISBN {self.isbn} non trouvé dans la bibliothèque."
        super().__init__(self.message)

class LivreDejaExistantErreur(ErreurBibliotheque):
    def __init__(self, isbn):
        self.isbn = isbn
        self.message = f"Livre avec ISBN {self.isbn} existe déjà dans la bibliothèque."
        super().__init__(self.message)

class FormatFichierInvalideErreur(ErreurBibliotheque):
    def __init__(self, format_fichier):
        self.format_fichier = format_fichier
        self.message = f"Format de fichier '{self.format_fichier}' invalide pour le livre numérique."
        super().__init__(self.message)

class EspaceInsuffisantErreur(ErreurBibliotheque):
    def __init__(self, taille_requise, taille_disponible):
        self.taille_requise = taille_requise
        self.taille_disponible = taille_disponible
        self.message = (f"Espace insuffisant : {self.taille_requise} Mo requis, "
                        f"mais seulement {self.taille_disponible} Mo disponible.")
        super().__init__(self.message)

class AuteurInvalideErreur(ErreurBibliotheque):
    def __init__(self, nom_auteur):
        self.nom_auteur = nom_auteur
        self.message = f"Nom d'auteur invalide : '{self.nom_auteur}'."
        super().__init__(self.message)

class TitreInvalideErreur(ErreurBibliotheque):
    def __init__(self, titre):
        self.titre = titre
        self.message = f"Titre de livre invalide : '{self.titre}'."
        super().__init__(self.message)

class ISBNInvalideErreur(ErreurBibliotheque):
    def __init__(self, isbn):
        self.isbn = isbn
        self.message = f"ISBN invalide : '{self.isbn}'."
        super().__init__(self.message)

class TailleFichierInvalideErreur(ErreurBibliotheque):
    def __init__(self, taille_fichier):
        self.taille_fichier = taille_fichier
        self.message = f"Taille de fichier invalide : '{self.taille_fichier}' Mo."
        super().__init__(self.message)

class LivreVideErreur(ErreurBibliotheque):
    def __init__(self, titre):
        self.titre = titre
        self.message = f"Le livre '{self.titre}' est vide et ne peut pas être ajouté."
        super().__init__(self.message)

class UserNonTrouveErreur(ErreurBibliotheque):
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"Utilisateur avec ID {self.user_id} non trouvé."
        super().__init__(self.message)

class UserDejaExistantErreur(ErreurBibliotheque):
    def __init__(self, username):
        self.username = username
        self.message = f"Le nom d'utilisateur '{self.username}' existe déjà."
        super().__init__(self.message)

class ExemplaireNonTrouveErreur(ErreurBibliotheque):
    def __init__(self, copy_id):
        self.copy_id = copy_id
        self.message = f"Exemplaire avec ID {self.copy_id} non trouvé."
        super().__init__(self.message)

class ExemplaireNonDisponibleErreur(ErreurBibliotheque):
    def __init__(self, statut):
        self.statut = statut
        self.message = f"L'exemplaire ne peut pas être emprunté. Statut actuel : '{self.statut}'."
        super().__init__(self.message)

class LoanNonTrouveErreur(ErreurBibliotheque):
    def __init__(self, loan_id):
        self.loan_id = loan_id
        self.message = f"Prêt (Loan) avec ID {self.loan_id} non trouvé."
        super().__init__(self.message)

class EmpruntNonAutoriseErreur(ErreurBibliotheque):
    def __init__(self, raison):
        self.raison = raison
        self.message = f"Emprunt non autorisé : {self.raison}"
        super().__init__(self.message)