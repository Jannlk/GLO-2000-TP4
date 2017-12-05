import smtplib, re, socket, optparse, sys
import os.path
from email.mime.text import MIMEText
from hashlib import sha256
import getpass

#Connexion au serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 1337))

while True:
    #Menu de connexion, choix d'une option
    option = input("Menu de connexion \n1. Se connecter \n2. Creer un compte \n")
    while option != "1" and option != "2":
        option = input("Veuillez saisir une option valide:\n")
    s.send(option.encode())

    #Se connecter
    if option == "1":
        id = input("Veuillez saisir votre identifiant:\n")
        s.send(id.encode())
        reponse = s.recv(1024).decode()
        while reponse != "1":
            id = input("Veuillez saisir un identifiant valide:\n")
            s.send(id.encode())
            reponse = s.recv(1024).decode()

        mdp = getpass.getpass("Veuillez saisir votre mot de passe:\n")
        s.send(mdp.encode())
        reponse = s.recv(1024).decode()
        if reponse == "-1":
            print("Desole, un probleme est survenu.")
            continue
        while reponse != "1":
            mdp = getpass.getpass("Veuiller saisir un mot de passe valide")
            s.send(mdp.encode())
            reponse = s.recv(1024).decode()

    #Créer un compte
    else:
        id = input("Veuillez choisir un identifiant:\n")
        s.send(id.encode())
        reponse = s.recv(1024).decode()
        while reponse != "0":
            id = input("Cet identifiant est deja pris, veuillez en choisir un autre:\n")
            s.send(id.encode())
            reponse = s.recv(1024).decode()


        mdp = getpass.getpass("Veuillez choisir un mot de passe contenant de 6 à 12 carateres, dont au moins une lettre et un chiffre:\n")
        while not (re.search(r"^[a-zA-Z0-9]{6,12}$", mdp) and re.search(r".*[0-9].*", mdp) and re.search(r".*[a-zA-Z].*",mdp)):
            mdp = getpass.getpass("Ce mot de passe ne respecte pas les conditions, veuillez en choisir un autre:\n")
        s.send(mdp.encode())

        reponse = s.recv(1024).decode()
        if reponse == "0":
            print("Desole, un probleme est survenu.")
            continue



    while True:
        option = input("Menu principale\n1. Envoi de courriels\n2. Consultation de courriels\n3. Statistiques\n4. Quitter\n")
        while option != ("1" or "2" or "3" or "4"):
            option = input("Veuillez saisir une option valide:\n")
        s.send(option.encode())

        if option == "1":

