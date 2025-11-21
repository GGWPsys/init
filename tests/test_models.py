from src.models import Livre, LivreNumerique, Bibliotheque


def test_bibliotheque_initialement_vide():
    bibli = Bibliotheque()
    assert hasattr(bibli, "livres")
    assert len(bibli.livres) == 0


def test_ajouter_livre_et_str():
    bibli = Bibliotheque()
    livre = Livre("Titre A", "Auteur A", "ISBN-A")
    bibli.ajouter_livre(livre)
    assert len(bibli.livres) == 1
    assert "Titre A" in str(bibli.livres[0])


def test_supprimer_par_isbn():
    bibli = Bibliotheque()
    livre1 = Livre("T1", "A1", "ISBN1")
    livre2 = Livre("T2", "A2", "ISBN2")
    bibli.ajouter_livre(livre1)
    bibli.ajouter_livre(livre2)
    assert len(bibli.livres) == 2
    bibli.supprimer_livre_par_isbn("ISBN1")
    assert all(getattr(x, "isbn", None) != "ISBN1" for x in bibli.livres)
    assert len(bibli.livres) == 1


def test_recherche_par_titre_et_auteur():
    bibli = Bibliotheque()
    livre_py = Livre("Python pour les nuls", "Jean Dupont", "ISBN-PY")
    livre_c = Livre("Apprendre C", "Jean Durand", "ISBN-C")
    bibli.ajouter_livre(livre_py)
    bibli.ajouter_livre(livre_c)
    res_t = bibli.rechercher_par_titre("python")
    assert len(res_t) == 1
    assert res_t[0].titre == "Python pour les nuls"
    res_a = bibli.rechercher_par_auteur("jean")
    assert len(res_a) == 2


def test_livre_numerique_str():
    livre_num = LivreNumerique("T Num", "Auteur", "ISBN-N", 12.5)
    s = str(livre_num)
    assert "12.5" in s or "12" in s
