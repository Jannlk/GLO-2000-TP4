import smtplib, re, socket, optparse, sys
import os.path
from email.mime.text import MIMEText
from hashlib import sha256
import utilitaires

#Création du socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("localhost", 1337))
serversocket.listen(5)
print("Listening on port " + str(serversocket.getsockname()[1]))
nbConnexions = 0

while True:
    #Un client se connecte au serveur
    (s, address) = serversocket.accept()
    nbConnexions += 1
    print(str(nbConnexions) + "e connexion au serveur")

    #Réception du choix d'option du menu connexion.
    option = s.recv(1024).decode()

    #Si l'utilisateur choisit de se connecter
    if option == "1":

        #On vérifie que le compte existe
        id = s.recv(1024).decode()
        verification = utilitaires.verifierID(id)
        s.send(verification.encode())
        while verification != "1":
            id = s.recv(1024).decode()
            verification = utilitaires.verifierID(id)
            s.send(verification.encode())

        #On vérifie le mot de passe
        mdp = s.recv(1024).decode()
        verification = utilitaires.connexion(id, mdp)
        s.send(verification.encode())
        #Si un problème est survenu
        if verification == "-1":
            continue
        #Sinon on vérifie que le mot de passe est bon
        while verification != "1":
            mdp = s.recv(1024).decode()
            verification = utilitaires.connexion(id, mdp)
            s.send(verification.encode())




    #Si l'utilisateur choisit de se créer un compte
    else:
        #Création de l'identifiant
        id = s.recv(1024).decode()
        verification = utilitaires.verifierID(id)
        s.send(verification.encode())
        while utilitaires.verifierID(id) == "1":
            id = s.recv(1024).decode()
            verification = utilitaires.verifierID(id)
            s.send(verification.encode())

        #Création du mot de passe
        mdp = s.recv(1024).decode()
        verification = utilitaires.creerCompte(id, mdp)
        s.send(verification.encode())
        if verification == "0":
            continue


    while True:
        # Réception du choix d'option du menu principal
        option = s.recv(1024).decode().replace("\n", "")

        if option == "1":
            

