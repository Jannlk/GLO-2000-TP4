import smtplib, re, socket, optparse, sys
import os.path
from email.mime.text import MIMEText
from hashlib import sha256
import getpass
import pickle

parser = optparse.OptionParser()
parser.add_option("-a", "--address", action="store", dest="address", default="localhost")
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1337)
opts = parser.parse_args(sys.argv[1:])[0]

destination = (opts.address, opts.port)
#Connexion au serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect(destination)
s.settimeout(None)

while True:
    #Menu de connexion, choix d'une option
    option = input("Menu de connexion \n1. Se connecter \n2. Creer un compte \n")
    while option != "1" and option != "2":
        option = input("Veuillez saisir une option valide:\n")
    s.send(option.encode())

    #Se connecter
    if option == "1":
        id = input("Veuillez saisir votre identifiant:\n")
        mdp = getpass.getpass("Veuillez saisir votre mot de passe:\n")
        s.send(id.encode())
        s.send(mdp.encode())
        reponseID = s.recv(1024).decode()
        if reponseID != "0":
            reponseMDP = s.recv(1024).decode()
        while reponseID != "1" or reponseMDP != "1":
            if reponseID != "1":
                id = input("Veuillez saisir un identifiant valide:\n")
                mdp = getpass.getpass("Veuillez saisir votre mot de passe:\n")
            elif reponseMDP == "-1":
                print("Desole, un probleme est survenu.")
                continue
            else:
                print("Ce n'est pas le bon mot de passe. Veuillez reessayer.")
                id = input("Veuillez saisir votre identifiant:\n")
                mdp = getpass.getpass("Veuillez saisir votre mot de passe:\n")
            s.send(id.encode())
            s.send(mdp.encode())
            reponseID = s.recv(1024).decode()
            if reponseID != "0":
                reponseMDP = s.recv(1024).decode()



    #Créer un compte
    elif option == "2":
        id = input("Veuillez choisir un identifiant:\n")
        mdp = getpass.getpass("Veuillez choisir un mot de passe contenant de 6 à 12 carateres, dont au moins une lettre et un chiffre:\n")
        s.send(id.encode())
        s.send(mdp.encode())
        reponseID = s.recv(1024).decode()
        if reponseID != "1":
            reponseMDP = s.recv(1024).decode()
        while reponseID != "0" or reponseMDP != "1":
            if reponseID != "0":
                id = input("Cet identifiant est deja pris, veuillez en choisir un autre:\n")
                mdp = getpass.getpass("Veuillez saisir votre mot de passe:\n")
            else:
                print("Ce mot de passe ne respecte pas les conditions, veuilelz en choisir un autre.")
                id = input("Veuillez saisir votre identifiant a nouveau:\n")
                mdp = getpass.getpass("Veuillez saisir votre nouveau mot de passe:\n")
            s.send(id.encode())
            s.send(mdp.encode())
            reponseID = s.recv(1024).decode()
            if reponseID != "1":
                reponseMDP = s.recv(1024).decode()
        reponseCreationCompte = s.recv(1024).decode()
        if reponseCreationCompte == "0":
            print("Desole, un probleme est survenu")
            continue


    while True:
        option = input("\nMenu principale\n1. Envoi de courriels\n2. Consultation de courriels\n3. Statistiques\n4. Quitter\n")
        while option not in  ["1", "2", "3", "4"]:
            option = input("Veuillez saisir une option valide:\n")

        s.send(option.encode())

        if option == "1":
            email_from = id + "@reseauglo.ca"
            s.send(email_from.encode())

            response = "-1"
            while(response == "-1"):
                email_to = input("\nÀ: ")
                s.send(email_to.encode())
                response = s.recv(1024).decode()

            subject = input("\nSujet: ")
            s.send(subject.encode())
            data = input("\nMessage: ")
            s.send(data.encode())

            response = s.recv(1024).decode()
            if(response == "-1"):
                print("\nErreur lors de l'envoie du courriel.")
                continue
            else:
                print("\nCourriel envoyé avec succès!")
        elif option == "2":
            s.send(id.encode())
            data_string = s.recv(1024)
            mails = pickle.loads(data_string)

            print("\nListe de vos courriels: \n")

            compteur = 1;
            for mail in mails:
                print("\n" + str(compteur) + ". " + mail)
                compteur += 1

            email_id = input("\nQuel courriel souhaitez-vous visionner? \n")

            s.send(email_id.encode())

            email_content = s.recv(1024).decode()
            print("\n" + email_content)
            input("\nAppuyez sur Enter pour continuer...")
            continue
        elif option == "3":
            s.send(id.encode())

            filesize = s.recv(1024).decode()

            data_string = s.recv(1024)
            mails = pickle.loads(data_string)

            print("\nNombre de messages: " + str(len(mails)) + "\n")
            print("\nTaille du repertoire personnel (en octets): " + filesize + "\n")
            print("\nListe de vos courriels: \n")

            compteur = 1;
            for mail in mails:
                print("\n" + str(compteur) + ". " + mail)
                compteur += 1
            input("\nAppuyez sur Enter pour continuer...")
            continue
        elif option == "4":
            break;
    s.close()
    exit()