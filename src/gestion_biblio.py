import sqlite3

DATABASE = 'bibliotheque.db'

def initialiser_db():
    "Crée la connexion et la table des livres si elle n'existe pas."
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            isbn TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def ajouter_livre(titre, auteur, isbn):
    "nouveau livre. Retourne True en cas de succès, False en cas d'erreur."
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO livres (titre, auteur, isbn) VALUES (?, ?, ?)",
                    (titre, auteur, isbn))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_livres():
    "livres triés par titre."
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT titre, auteur, isbn FROM livres ORDER BY titre")
    livres = cursor.fetchall()
    conn.close()
    return livres

def search_by_auteur(auteur):
    "Recupere les livres dont le nom de l'auteur contient le terme recherché."
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT titre, auteur, isbn FROM livres WHERE auteur LIKE ?", ('%' + auteur + '%',))
    livres = cursor.fetchall()
    conn.close()
    return livres

initialiser_db()