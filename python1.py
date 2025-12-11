import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from icalendar import Calendar
from datetime import datetime

# Fonction pour choisir le fichier
def choisir_fichier():
    chemin_fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier", 
        filetypes=[("Fichiers ICS", "*.ics")]
    )
    if chemin_fichier:
        label_chemin.config(text=f"Fichier sélectionné : {chemin_fichier}")
        lire_fichier_ics(chemin_fichier)
    else:
        label_chemin.config(text="Aucun fichier sélectionné")

# Fonction pour quitter l'application
def quitter():
    fenetre.destroy()

# Fonction pour formater les dates au format lisible
def formater_date(dt):
    if dt:
        return dt.strftime("%d %B %Y à %H:%M")
    return "Date inconnue"

def lire_fichier_ics(fichier):
    with open(fichier, 'r') as f:
        contenu = f.read()

    cal = Calendar.from_ical(contenu)
    
    texte_resultat = ""

    for event in cal.walk('vevent'):
        summary = event.get('summary')
        dtstart = event.get('dtstart')
        dtend = event.get('dtend')
        description = event.get('description')
        
        date_debut = formater_date(dtstart.dt)
        date_fin = formater_date(dtend.dt)

        texte_resultat += f"Résumé : {summary}\n"
        texte_resultat += f"Début : {date_debut}\n"
        texte_resultat += f"Fin : {date_fin}\n"
        texte_resultat += f"Description : {description if description else 'Pas de description'}\n\n"
    
    # Efface le contenu précédent et insère le nouveau texte
    text_resultat.delete("1.0", tk.END)
    text_resultat.insert(tk.END, texte_resultat)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Sélectionner un fichier ICS")
fenetre.geometry("600x500")

btn_choisir_fichier = tk.Button(fenetre, text="Choisir un fichier", command=choisir_fichier)
btn_choisir_fichier.pack(pady=10)

label_chemin = tk.Label(fenetre, text="Aucun fichier sélectionné")
label_chemin.pack(pady=10)

# Zone de texte avec barre de défilement
text_resultat = ScrolledText(fenetre, wrap=tk.WORD, width=70, height=20)
text_resultat.pack(pady=10, fill=tk.BOTH, expand=True)

btn_quitter = tk.Button(fenetre, text="Quitter", command=quitter)
btn_quitter.pack(pady=10)

fenetre.mainloop()

