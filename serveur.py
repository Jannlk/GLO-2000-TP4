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
    elif option == "2":
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


    #Envoie d'un courriel
    elif option == "3":
        # reception du courriel et verification qu’il est valide
        print("Test 5")
        emailFrom = s.recv(1024).decode()
        print("Test 5")
        emailAddress = s.recv(1024).decode()
        print("Test 5")
        while not re.search(r"^[^@]+@[^@]+\.[^@]+$", emailAddress):
            print("Test 6")
            msg = "-1"
            s.send(msg.encode())
            emailAddress = s.recv(1024).decode()
        msg = "0"

        # creation du courriel
        subject = s.recv(1024).decode()
        data = s.recv(1024).decode()
        courriel = MIMEText(data)
        courriel["From"] = emailFrom
        courriel["To"] = emailAddress
        courriel["Subject"] = subject

        #Externe
        use_smtp_ulaval = False
        if(not re.search(r"^[^@]+@reseauglo\.ca$", emailAddress)):
            use_smtp = True

        if(use_smtp_ulaval):

            # envoi du courriel par le smtp de l'ecole
            try:
                smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
                smtpConnection.sendmail(courriel["From"], courriel["To"], courriel.as_string())
                smtpConnection.quit()
                msg = "0"
                s.send(msg.encode())
            except:
                msg = "0"
                s.send(msg.encode())


            s.send(msg.encode())
        else:
            chemin_dossier = emailAddress.replace("@reseauglo.ca", "")
            verification = utilitaires.creerLocal(chemin_dossier, courriel['Subject'], courriel['From'], data)


