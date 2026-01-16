import tkinter as tk
from tkinter import ttk, messagebox
from comptabilite import charger_operations, generer_ecritures, ajouter_au_journal, generer_grand_livre
from stockage import lire_json

operations = charger_operations()

root = tk.Tk()
root.title("Application de Gestion Comptable")
root.geometry("700x500")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# --- ONGLET OPERATIONS ---
tab_op = ttk.Frame(notebook)
notebook.add(tab_op, text="Opérations")

tk.Label(tab_op, text="Choisir une opération").pack(pady=5)
combo = ttk.Combobox(tab_op, values=[o["nom"] for o in operations], state="readonly")
combo.pack()

tk.Label(tab_op, text="Montant").pack(pady=5)
ent = tk.Entry(tab_op)
ent.pack()

def valider():
    if combo.current() == -1:
        messagebox.showerror("Erreur", "Choisir une opération")
        return
    if not ent.get():
        messagebox.showerror("Erreur", "Entrer un montant")
        return

    op = operations[combo.current()]
    lignes = generer_ecritures(op, {"montant": float(ent.get())})
    ajouter_au_journal(lignes)
    messagebox.showinfo("Succès", "Opération enregistrée")
    ent.delete(0, tk.END)

tk.Button(tab_op, text="Valider l'opération", command=valider).pack(pady=10)

# --- ONGLET JOURNAL ---
tab_j = ttk.Frame(notebook)
notebook.add(tab_j, text="Journal")

tree = ttk.Treeview(tab_j, columns=("date","libelle","compte","debit","credit"), show="headings")
for c in tree["columns"]:
    tree.heading(c, text=c)
tree.pack(expand=True, fill="both")

for l in lire_json("journal.json"):
    tree.insert("", "end", values=(l["date"], l["libelle"], l["compte"], l["debit"], l["credit"]))

# --- ONGLET GRAND LIVRE ---
tab_gl = ttk.Frame(notebook)
notebook.add(tab_gl, text="Grand Livre")

text = tk.Text(tab_gl)
text.pack(expand=True, fill="both")

gl = generer_grand_livre()
for c, v in gl.items():
    text.insert("end", f"Compte {c} | Débit: {v['debit']} | Crédit: {v['credit']}\n")

root.mainloop()
