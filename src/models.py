class Livre:
    def __init__ (self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
    
    def __str__(self):
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn})"

class LivreNumerique(Livre):
    def __init__ (self, titre , auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def __str__ (self):
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn}, {self.taille_fichier} Mo)"
    
class Bibliotheque:
    def __init__ (self):
        self.livres = []
    
    def ajouter_livre (self, livre):
        self.livres.append(livre)
        print(f"Livre '{livre.titre}' ajouté à la bibliothèque.")
    
    def supprimer_livre_par_isbn (self, isbn):
        for livre in self.livres:
            if livre.isbn == isbn:
                self.livres.remove(livre)
                print(f"Livre '{livre.titre}' supprimé.")
                return
        print("Livre non trouvé.")
    
    def rechercher_par_titre (self, titre):
        resultats = [livre for livre in self.livres if titre.lower() in livre.titre.lower()]
        return resultats
    
    def rechercher_par_auteur (self, auteur):
        resultats = [livre for livre in self.livres if auteur.lower() in livre.auteur.lower()]
        return resultats

if __name__ == "__main__":
    biblio = Bibliotheque()

    livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123456")
    livre2 = LivreNumerique("Python pour les nuls", "Jean Dupont", "987654", 5)

    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    print("\nRecherche par titre 'abraca':")
    for livre in biblio.rechercher_par_titre("abraca"):
        print(livre)

    print("\nRecherche par auteur 'Antoine':")
    for livre in biblio.rechercher_par_auteur("Antoine"):
        print(livre)

    biblio.supprimer_livre_par_isbn("123456")

class Copy:
    
    def __init__(self, book_id, copy_id=None, status="Disponible", condition="Bon état", current_loan_id=None):
        
        self.copy_id = copy_id if copy_id is not None else str(uuid.uuid4())
        self.book_id = book_id
        self.status = status
        self.condition = condition
        self.current_loan_id = current_loan_id
        
        if self.status not in ["Disponible", "Emprunté", "Endommagé", "Perdu"]:
            raise ValueError("Statut d'exemplaire invalide.")

    def __str__(self):
        return f"Exemplaire ID: {self.copy_id[:4]}... - Statut: {self.status}"

class Book:

    def __init__(self, title, author, category,book_id=None,loan_history=None,reservation_queue=None,ratings=None,comments=None,copies=None):

        self.book_id = book_id if book_id is not None else str(uuid.uuid4())
        self.title = title
        self.author = author
        self.category = category
        self.ratings = ratings if ratings is not None else []
        self.comments = comments if comments is not None else [] 
        self.loan_history = loan_history if loan_history is not None else [] 
        self.reservation_queue = reservation_queue if reservation_queue is not None else deque()
        self.copies = copies if copies is not None else []

    def __str__(self):
        return f"'{self.title}' par {self.author} ({self.category})"
        
    def available_copies_count(self):
        return sum(1 for copy in self.copies if copy.status == "Disponible")
        
    def add_copy(self, copy):
        if copy.book_id != self.book_id:
            raise ValueError("L'exemplaire n'est pas lié à ce livre.")
        self.copies.append(copy)

class LibraryManager:
    def __init__(self, storage_service):
        self.storage = storage_service

    def add_new_book(self, title, author, category):
        new_book = Book(title=title, author=author, category=category)
        self.storage.save_book(new_book)
        return new_book

    def add_copy(self, book_id, condition="Bon état"):
        book = self.storage.get_book_by_id(book_id)
        if book is None:
            raise ValueError("Livre introuvable. Impossible d'ajouter un exemplaire.")
        
        new_copy = Copy(book_id=book_id, condition=condition)
        
        book.copies.append(new_copy)
        
        self.storage.save_book(book)
        return new_copy

    def update_copy_status(self, copy_id, new_status):
        copy, book = self.storage.get_copy_and_parent_book(copy_id)
        if copy is None:
            raise ValueError(f"Exemplaire ID {copy_id} introuvable.")
            
        if new_status not in ["Disponible", "Emprunté", "Endommagé", "Perdu"]:
            raise ValueError("Statut non valide.")
        
        copy.status = new_status
        self.storage.save_book(book) 
        return copy

    def search_books(self, query=None, category=None):
        results = []
        query = query.lower() if query else None
        category = category.lower() if category else None
        
        for book in self.storage.books.values():
            match = True
            
            if category and book.category.lower() != category:
                match = False
            
            if query and not (query in book.title.lower() or query in book.author.lower()):
                match = False
                
            if match:
                results.append(book)
                
        return results

    def get_availability(self, book_id):
        book = self.storage.get_book_by_id(book_id)
        if book is None:
            return 0
        return book.available_copies_count()

class Loan:
    def __init__(self,user_id,copy_id,loan_id=None,loan_date=None,due_date=None,return_date=None,penalty_rate=1.0):
        
        self.loan_id = loan_id if loan_id is not None else str(uuid.uuid4())
        self.user_id = user_id
        self.copy_id = copy_id
        self.loan_date = loan_date if loan_date is not None else date.today()
        self.due_date = due_date
        self.return_date = return_date
        self.penalty_rate = penalty_rate

    def is_overdue(self):
        if self.return_date is None:
            return date.today() > self.due_date
        return self.return_date > self.due_date

    def calculate_delay_days(self):
        if self.is_overdue():
            if self.return_date is None:
                delay = date.today() - self.due_date
            else:
                delay = self.return_date - self.due_date
            
            return max(0, delay.days)
        return 0

class Penalty:
    FIXED_DAILY_RATE = 0.50

    def __init__(self,user_id,source_loan_id,penalty_id=None,amount=0.0,is_paid=False,reason="Retard"):
        
        self.penalty_id = penalty_id if penalty_id is not None else str(uuid.uuid4())
        self.user_id = user_id
        self.source_loan_id = source_loan_id
        self.amount = amount
        self.is_paid = is_paid
        self.reason = reason

    @classmethod
    def create_from_delay(cls, loan, delay_days):
        daily_rate_adjusted = cls.FIXED_DAILY_RATE * loan.penalty_rate
        total_amount = round(daily_rate_adjusted * delay_days, 2)
        
        return cls(
            user_id=loan.user_id,
            source_loan_id=loan.loan_id,
            amount=total_amount,
            reason=f"Retard de {delay_days} jour(s)"
        )


class Reservation:
    def __init__(self, user_id, book_id,reservation_id=None, reservation_date=None, is_active=True):
        
        self.reservation_id = reservation_id if reservation_id is not None else str(uuid.uuid4())
        self.user_id = user_id
        self.book_id = book_id
        self.reservation_date = reservation_date if reservation_date is not None else date.today()
        self.is_active = is_active

    def __str__(self):
        return f"Réservation ID: {self.reservation_id[:4]}... par User {self.user_id[:4]}..."

SUBSCRIPTION_RULES = {
    "BASIQUE": {
        "max_loans_per_month": 3,
        "loan_duration_days": 14,
        "penalty_multiplier": 1.0
    },
    "PREMIUM": {
        "max_loans_per_month": 5,
        "loan_duration_days": 21,
        "penalty_multiplier": 0.75
    },
    "VIP": {
        "max_loans_per_month": 10,
        "loan_duration_days": 30,
        "penalty_multiplier": 0.5
    }
}
class User:
    def __init__(self, username, password_hash,is_admin=False,subscription_type="BASIQUE",user_id=None,current_loan_id=None,monthly_loan_count=0,current_penalties=0.0,loan_history=None,subscription_expiry_date=None):
        
        self.user_id = user_id if user_id is not None else str(uuid.uuid4())
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        
        # abonnement
        if subscription_type not in SUBSCRIPTION_RULES:
            raise ValueError(f"Type d'abonnement invalide: {subscription_type}")
        self.subscription_type = subscription_type
        
        # expiration
        if subscription_expiry_date is None:
            self.subscription_expiry_date = date.today().replace(year=date.today().year + 1)
        else:
            self.subscription_expiry_date = subscription_expiry_date
        
        # emprunt
        self.current_loan_id = current_loan_id  # Un seul livre à la fois
        self.monthly_loan_count = monthly_loan_count 
        self.loan_history = loan_history if loan_history is not None else [] # Historique
        
        # penalite
        self.current_penalties = current_penalties
        
    def __str__(self):
        return f"Utilisateur: {self.username} (Abonnement: {self.subscription_type}, Pénalités: {self.current_penalties}€)"

    def get_limits(self):
        return SUBSCRIPTION_RULES.get(self.subscription_type, SUBSCRIPTION_RULES["BASIQUE"])

    def can_borrow(self):
        limits = self.get_limits()
        today = date.today()
        
        # Pénalités impayées
        if self.current_penalties > 0.0:
            return (False, "Pénalités impayées.")
        
        # Abonnement expiré
        if self.subscription_expiry_date < today:
            return (False, "Abonnement expiré.")

        # Un seul livre à la fois
        if self.current_loan_id is not None:
            return (False, "Un livre est déjà emprunté en cours.")
        
        # Limite d'emprunt mensuel
        if self.monthly_loan_count >= limits["max_loans_per_month"]:
            return (False, f"Limite d'emprunt mensuel atteinte ({limits['max_loans_per_month']}).")

        return (True, "Emprunt autorisé.")

    def reset_monthly_count(self):
        self.monthly_loan_count = 0