import os.path
from hashlib import sha256

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
#id, mdp : L'identifiant et le mot de passe de l'utilisateur
#Return : "-1" s'il y a un problème avec lors de l'ouverture du fichier
#         "0" si le mot de passe de correspond pas
#         "1" si la connexion est un succès
def creerLocal(id, sujet, emailFrom, data):
    state = "0"
    try:
        file = open(id + "/" + sujet + ".txt", "a")
        file.write("From: " + emailFrom + "\n")
        file.write("Message: " + data)
        file.close()
        state = "0"
    except:
        state = "-1"

    return state