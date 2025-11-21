import tkinter as tk
from tkinter import ttk, messagebox
from gestion_biblio import ajouter_livre, get_all_livres, search_by_auteur

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TP - Application Bibliothèque")
        self.geometry("800x600")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        list_frame = ttk.Frame(self)
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.setup_add_section(control_frame)

        self.setup_list_and_search_section(control_frame, list_frame)
        
        self.update_list()

    def setup_add_section(self, parent_frame):
        "ajout de livre"
        add_label = ttk.Label(parent_frame, text="📚 Ajouter un Nouveau Livre", font=('Arial', 12, 'bold'))
        add_label.grid(row=0, column=0, columnspan=7, pady=(0, 5), sticky="w")

        ttk.Label(parent_frame, text="Titre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.titre_entry = ttk.Entry(parent_frame, width=20)
        self.titre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(parent_frame, text="Auteur:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.auteur_entry = ttk.Entry(parent_frame, width=20)
        self.auteur_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(parent_frame, text="ISBN:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.isbn_entry = ttk.Entry(parent_frame, width=15)
        self.isbn_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        ttk.Button(parent_frame, text="➕ Ajouter", command=self.handle_ajouter).grid(row=1, column=6, padx=10, pady=5, sticky="w")

    def setup_list_and_search_section(self, control_frame, list_frame):
        "champ de recherche "

        ttk.Label(control_frame, text="🔍 Rechercher par Auteur:").grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")
        self.search_entry = ttk.Entry(control_frame, width=20)
        self.search_entry.grid(row=2, column=1, padx=5, pady=(15, 5), sticky="w")
        
        ttk.Button(control_frame, text="Rechercher", command=self.handle_recherche).grid(row=2, column=2, padx=5, pady=(15, 5), sticky="w")
        ttk.Button(control_frame, text="Afficher Tout", command=self.update_list).grid(row=2, column=3, padx=5, pady=(15, 5), sticky="w")

        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(list_frame, columns=("Titre", "Auteur", "ISBN"), show="headings")
        self.tree.heading("Titre", text="Titre du Livre")
        self.tree.heading("Auteur", text="Auteur")
        self.tree.heading("ISBN", text="ISBN")

        self.tree.column("Titre", width=300, anchor="w")
        self.tree.column("Auteur", width=200, anchor="w")
        self.tree.column("ISBN", width=150, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def handle_ajouter(self):
        "Gère l'action d'ajout d'un livre."
        titre = self.titre_entry.get()
        auteur = self.auteur_entry.get()
        isbn = self.isbn_entry.get()

        if not titre or not auteur or not isbn:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs (Titre, Auteur, ISBN).")
            return

        success = ajouter_livre(titre, auteur, isbn) 
        
        if success:
            messagebox.showinfo("Succès", f"Livre '{titre}' ajouté à la bibliothèque.")
            self.titre_entry.delete(0, tk.END)
            self.auteur_entry.delete(0, tk.END)
            self.isbn_entry.delete(0, tk.END)
            self.update_list()
        else:
            messagebox.showerror("Erreur", f"L'ISBN '{isbn}' existe déjà dans la base de données.")
            
    def handle_recherche(self):
        "Gère la recherche par auteur."
        auteur = self.search_entry.get()
        if not auteur:
            messagebox.showwarning("Attention", "Veuillez saisir un nom d'auteur pour effectuer la recherche.")
            return
        
        livres = search_by_auteur(auteur)
        
        if livres:
            self.update_list(livres)
            messagebox.showinfo("Résultat", f"{len(livres)} livre(s) trouvé(s) pour '{auteur}'.")
        else:
            self.update_list([])
            messagebox.showinfo("Résultat", f"Aucun livre trouvé pour l'auteur '{auteur}'.")

    def update_list(self, livres=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        if livres is None:
            livres = get_all_livres()
        for livre in livres:
            self.tree.insert('', tk.END, values=livre)

if __name__ == "__main__":
    app = Application()
    app.mainloop()