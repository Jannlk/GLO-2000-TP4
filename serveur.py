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

        #On vérifie que le compte existe et que le mot de passe est valide
        id = s.recv(1024).decode()
        mdp = s.recv(1024).decode()
        verificationID = utilitaires.verifierID(id)
        s.send(verificationID.encode())
        if verificationID != "0":
            verificationMDP = utilitaires.connexion(id, mdp)
            s.send(verificationMDP.encode())

        while verificationID != "1" or verificationMDP != "1":
            id = s.recv(1024).decode()
            mdp = s.recv(1024).decode()
            verificationID = utilitaires.verifierID(id)
            s.send(verificationID.encode())
            if verificationID != "0":
                verificationMDP = utilitaires.connexion(id, mdp)
                s.send(verificationMDP.encode())
        if verificationMDP == "-1":
            continue





    #Si l'utilisateur choisit de se créer un compte
    else:
        #Création de l'identifiant
        id = s.recv(1024).decode()
        mdp = s.recv(1024).decode()
        verificationID = utilitaires.verifierID(id)
        s.send(verificationID.encode())
        if verificationID != "1":
            verificationMDP = utilitaires.veififierMDP(mdp)
            s.send(verificationMDP.encode())
        while verificationID != "0" or verificationMDP != "1":
            id = s.recv(1024).decode()
            mdp = s.recv(1024).decode()
            verificationID = utilitaires.verifierID(id)
            s.send(verificationID.encode())
            if verificationID != "1":
                verificationMDP = utilitaires.veififierMDP(mdp)
                s.send(verificationMDP.encode())
        verificationErreur = utilitaires.creerCompte(id, mdp)
        s.send(verificationErreur.encode())
        if verificationErreur == "0":
            continue


    while True:
        # Réception du choix d'option du menu principal
        option = s.recv(1024).decode()
            

