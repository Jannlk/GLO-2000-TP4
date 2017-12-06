import os.path
import re
from hashlib import sha256
from os.path import getsize

#Méthode qui crée un nouveau compte dans le répertoire du serveur
#id : nom du dossier
#mdp : mot de passe
#return : "0" si un problème est survenu avec le fichier, "1" si le compte a été créé
def creerCompte(id, mdp):
    state = "1"
    try:
        os.makedirs(id)
        file = open(id + "/config.txt", "w")
        file.write(sha256(mdp.encode()).hexdigest())
        file.close()
    except:
        state = "0"
    return state

#Méthode qui vérifie si le compte existe
#id : Nom du dossier du compte
#return: "1" si le compte existe, "0" sinon
def verifierID(id):
    state = "0"
    if os.path.exists(id + "/config.txt"):
        state = "1"
    return state

#Méthode qui vérifie si le mot de passe respecte les conditions
#mdp : le mot de passe
#return : "1" si le mot de passe respecte les conditions, "0" sinon.
def veififierMDP(mdp):
    state = "0"
    if (re.search(r"^[a-zA-Z0-9]{6,12}$", mdp) and re.search(r".*[0-9].*", mdp) and re.search(r".*[a-zA-Z].*",mdp)):
        state = "1"
    return state

#Méthode qui permet d'ouvrir le dossier d'un utilisateur
#id, mdp : L'identifiant et le mot de passe de l'utilisateur
#Return : "-1" s'il y a un problème avec lors de l'ouverture du fichier
#         "0" si le mot de passe de correspond pas
#         "1" si la connexion est un succès
def connexion(id, mdp):
    state = "1"
    try:
        file = open(id + "/config.txt", "r")
        password = file.readline()
        file.close()
        if sha256(mdp.encode()).hexdigest() != password:
            state = "0"
    except:
        state = "-1"

    return state

#Méthode qui permet d'ouvrir le dossier d'un utilisateur
#id, subject, data: L'identifiant de l'utilisateur, le sujet et corps du message
#Return : "-1" s'il y a un problème avec lors de l'ouverture du fichier
#         "0" si tout se passe bien
def courrielLocal(id, subject, data):
    state = "0"
    try:
        file = open(id + "/" + subject + ".txt", "w")
        file.write(data)
        file.close()
        state = "0"
    except:
        state = "-1"

    return state

#Méthode qui permet d'ouvrir un courriel local
#subject, data: Sujet et corps du courriel
def ouvrirLocal(id, filename):
    try:
        file = open( id + "/" + filename, "r")
        str_content = file.read();
        file.close()
        return str_content
    except:
        print("Fichier introuvable.")



#Méthode qui permet d'enregistrer un courriel vers un utilisateur inexistant
#subject, data: Sujet et corps du courriel
def courrielDump(subject, data):
    try:
        if not os.path.exists("DESTERREUR"):
            os.makedirs("DESTERREUR")
        file = open("DESTERREUR/" + subject + ".txt", "w")
        file.write(data)
        file.close()
    except:
        print("Guess somebody fucked up good.")


#Méthode qui retourne la grosseur d'un directory
#id: le directory
def getSize(id):
    try:
        size = getsize(id)
        return size
    except:
        print("Mauvais nom de repertoire")


#Méthode qui retourne la liste trié par date
#id, liste: la liste a trier
def sortDate(id, liste):
    liste.sort(key=lambda x: os.path.getmtime(id + "/" + x))
    return liste

#Méthode qui retourne la liste trié alphabetiquement
#id, liste: la liste a trier
def sortAlpha(liste):
    liste = liste.sort()
    return liste
