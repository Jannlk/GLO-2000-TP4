import smtplib, re, socket, optparse, sys
import os.path
from email.mime.text import MIMEText
from hashlib import sha256

#Choisir le port
parser = optparse.OptionParser()
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1337)
port = parser.parse_args(sys.argv[1:])[0].port

#Création du socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("localhost", port))
serversocket.listen(5)
print("Listening on port " + str(serversocket.getsockname()[1]))
nbConnexions = 0

while True:
    #Un client se connecte au serveur
    (s, address) = serversocket.accept()
    nbConnexions += 1
    print(str(nbConnexions) + "e connexion au serveur")

    #Présentation des options
    msg = "Menu de connexion \n1. Se connecter \n2. Creer un compte "
    s.send(msg.encode())

    #Réception du choix de l'option. On s'assure qu'elle est valide
    option = s.recv(1024).decode().replace("\n", "")
    while option != "1" and option != "2":
        msg = "Saisissez une option valide : "
        s.send(msg.encode())
        option = s.recv(1024).decode().replace("\n", "")


    #Si l'utilisateur choisit de se connecter
    if option == "1":
        msg = "Veuillez saisir votre identifiant:"
        s.send(msg.encode())
        identifiant = s.recv(1024).decode().replace("\n", "")

        #On vérifie que le compte existe
        while not os.path.exists(identifiant+"/config.txt"):
            msg = "Veuillez saisir un identifiant valide:"
            s.send(msg.encode())
            identifiant = s.recv(1024).decode().replace("\n", "")

        #On s'assure qu'il n'y a pas de problème avec le compte du côté du serveur
        try:
            file = open(identifiant+"/config.txt", "r")
            password = file.readline().replace("\n", "")
        except:
            msg = "Désolé, un problème est survenu. Appuyer sur entrer pour retourner au menu:"
            s.send(msg.encode())
            continue

        #On vérifie le mot de passe
        msg = "Veuillez saisir votre mot de passe:"
        s.send(msg.encode())
        mdp = s.recv(1024).decode().replace("\n", "")
        while sha256(mdp.encode()).hexdigest() != password:
            msg = "Ce n'est pas le bon mot de passe. Veuillez essayer de nouveau:"
            s.send(msg.encode())
            mdp = s.recv(1024).decode().replace("\n", "")



    #Si l'utilisateur choisit de se créer un compte
    else:
        #Création de l'identifiant
        msg = "Veuillez choisir un identifiant pour votre compte:"
        s.send(msg.encode())
        identifiant = s.recv(1024).decode().replace("\n", "")
        while os.path.exists(identifiant+"/config.txt"):
            msg = "Cet identifiant est deja pris. Veuillez en choisir un nouveau:"
            s.send(msg.encode())
            identifiant = s.recv(1024).decode().replace("\n", "")

        #Création du dossier
        try:
            os.makedirs(identifiant)
            file = open(identifiant+"/config.txt", "w")
        except:
            msg = "Desole, un probleme est survenu. Appuyer sur entrer pour retourner au menu:"
            s.send(msg.encode())
            s.recv(1024).decode()
            continue

        #Création du mot de passe
        msg = "Veuillez choisir un mot de passe qui contient 6 a 12 caracteres, dont au moins une lettre et un chiffre: "
        s.send(msg.encode())
        mdp = s.recv(1024).decode().replace("\n", "")
        while not (re.search(r"^[a-zA-Z0-9]{6,12}$", mdp) and re.search(r".*[0-9].*", mdp) and re.search(r".*[a-zA-Z].*", mdp)):
            msg = "Ce mot de passe ne respecte pas les conditions. Veuillez en choisir en autre: "
            s.send(msg.encode())
            mdp = s.recv(1024).decode().replace("\n", "")
        file.write(sha256(mdp.encode()).hexdigest())
        file.close()
        msg = "Le compte a ete cree "
        s.send(msg.encode())


    #Une fois connecté ou inscrit, l'utilisateur aboutit au menu principal
    msg = "Menu principale\n1. Envoi de courriels\n2. Consultation de courriels\n3. Statistiques\n4. Quitter "
    s.send(msg.encode())

    # Réception du choix de l'option. On s'assure qu'elle est valide
    option = s.recv(1024).decode().replace("\n", "")
    while option != ("1" or "2" or "3" or "4"):
        msg = "Saisissez une option valide : "
        s.send(msg.encode())
        option = s.recv(1024).decode().replace("\n", "")