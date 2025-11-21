from models import (LivreNumerique, Bibliotheque)
from exceptions import (
    LivreDejaExistantErreur,
    EspaceInsuffisantErreur,
    TailleFichierInvalideErreur,
)

class Bibliotheque(Bibliotheque):
    def __init__(self):
        super().__init__()
        self.espace_disponible_mo = 1000
        
    def ajouter_livre(self, livre):
        if any(book.isbn == livre.isbn for book in self.livres):
            raise LivreDejaExistantErreur(livre.isbn)
        
        if isinstance(livre, LivreNumerique):
            if livre.taille_fichier <= 0:
                raise TailleFichierInvalideErreur(livre.taille_fichier)
            if livre.taille_fichier > self.espace_disponible_mo:
                raise EspaceInsuffisantErreur(livre.taille_fichier, self.espace_disponible_mo)
            self.espace_disponible_mo -= livre.taille_fichier
        
        super().ajouter_livre(livre)
        print(f"Espace disponible après ajout : {self.espace_disponible_mo} Mo")