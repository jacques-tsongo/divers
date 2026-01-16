from datetime import date
from stockage import lire_json, ecrire_json

def charger_operations():
    return lire_json("operations.json")

def generer_ecritures(operation, valeurs):
    lignes = []
    montant = valeurs["montant"]

    for r in operation["ecritures"]:
        lignes.append({
            "date": str(date.today()),
            "libelle": operation["nom"],
            "compte": r["compte"],
            "debit": montant if r["sens"] == "debit" else 0,
            "credit": montant if r["sens"] == "credit" else 0
        })
    return lignes

def ajouter_au_journal(lignes):
    journal = lire_json("journal.json")
    journal.extend(lignes)
    ecrire_json("journal.json", journal)

def generer_grand_livre():
    journal = lire_json("journal.json")
    gl = {}

    for l in journal:
        c = l["compte"]
        if c not in gl:
            gl[c] = {"debit": 0, "credit": 0}
        gl[c]["debit"] += l["debit"]
        gl[c]["credit"] += l["credit"]

    return gl
