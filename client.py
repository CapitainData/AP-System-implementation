#!/usr/bin/env python3
import socket

BUFFER_SIZE = 6000000000

adresseIP = "127.0.0.1"	# Ici, le poste local
port = 45001	# Se connecter sur le port 50000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((adresseIP, port))
print("Connecté au serveur")
client.send("Bonjour, je suis le client".encode("utf-8"))
reponse = client.recv(BUFFER_SIZE)
print(reponse.decode("utf-8"))

reponse = client.recv(BUFFER_SIZE)
print(reponse.decode("utf-8"))

while True:
    try:

        data = input("Please enter a request for: \n")
        client.send(data.encode("utf-8"))

        reponse = client.recv(BUFFER_SIZE)
        print(reponse.decode("utf-8"))

    except KeyboardInterrupt:
        print("Fermeture de la connexion")
        client.close()
        serveur.close()

print("Connexion fermée")
client.close()
