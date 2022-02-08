#!/usr/bin/env python3
import socket
import json
import re, os

wd = os.getcwd()

path = os.path.join(wd, "Data")

from request_parsers.select import select_all, select_subset
from request_parsers.insert import insert_obs


BUFFER_SIZE = 10000000


serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 45001))	# Écoute sur le port 50000
serveur.listen(5)

client, infosClient = serveur.accept()
print("Client connecté. Adresse " + infosClient[0])
requete = client.recv(BUFFER_SIZE)	# Reçoit BUFFER_SIZE octets. Vous pouvez changer pour
                           # recevoir plus de données
print(requete.decode("utf-8"))
reponse = "Bonjour, je suis le serveur"

client.send(reponse.encode("utf-8"))

msg = """
    Le nom de la base de données est par défaut `Data`

    Un example d'enregistrement est sous le format suivant:

                {'id': 2140,
                 'title': 'gj',
                 'description': 'ghj',
                 'location': 'Hermannplatz 5-6, 10967 Berlin, Germany',
                 'lng': 0,
                 'lat': 0,
                 'userId': 4051,
                 'name': 'manoj',
                 'isdeleted': False,
                 'profilePicture': 'Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png',
                 'videoUrl': None,
                 'images': None,
                 'mediatype': 0,
                 'imagePaths': None,
                 'feedsComment': None,
                 'commentCount': 0,
                 'multiMedia': [{'id': 3240,
                   'name': '',
                   'description': None,
                   'url': 'http://www.youtube.com/embed/mPhboJR0Llc',
                   'mediatype': 2,
                   'likeCount': 0,
                   'place': None,
                   'createAt': '0001-01-01T00:00:00'}],
                 'likeDislike': {'likes': 0, 'dislikes': 0, 'userAction': 2},
                 'createdAt': '2020-01-02T13:32:16.7480006',
                 'code': 0,
                 'msg': None}

    Pour accéder à l'aide entrez la commande `?` | `help`
"""

client.send(msg.encode("utf-8"))

while True:
    try:

        requete = client.recv(BUFFER_SIZE)
        print(requete.decode("utf-8"))

        if(requete.decode("utf-8") in ['?', 'help']):

            aide = """
            Liste des commandes possibles:

            - select * from Data --> Permet de sélectionner toutes
            les observations du JSON.

            - select * from Data where `KEY` == `VALUE` --> Permet
            de selectionner les observations correspondant à la valeur
            du champ sélectionné.

            - insert into Data (colname1, colname2, ...) values (val1, val2, )
            --> Insère des observations dans la table Data.
            """

            client.send(aide.encode("utf-8"))


        elif(requete.decode("utf-8").lower().startswith("select *")):

            response = select_all()

            client.send(response.encode("utf-8"))

        elif("where" in requete.decode("utf-8").lower()):

            requete_decoded = requete.decode("utf-8")

            to_select = requete_decoded.split("from")[0].split("select")[1].strip() # cases '*' and 'key1, key2, ...' to distinguish

            key_and_values = [x.strip() for x in requete_decoded.split("where")[1].split('==')]

            response = str(select_subset(to_select, key_and_values))

            client.send(response.encode("utf-8"))

        elif ("insert" in requete.decode("utf-8").lower()):

            requete_decoded = requete.decode("utf-8")

            columns_and_values = re.findall('\(.*?\)', requete_decoded)

            columns = columns_and_values[0].lstrip("(").rstrip(")").split(",")

            values = columns_and_values[1].lstrip("(").rstrip(")").split(",")

            with open(f'{path}/historical_data.json') as json_data:
                data_dict = json.load(json_data)

            keys = list(data_dict["feeds"][0].keys())

            i = 0
            for column in columns:
                if columns not in keys:
                    client.send("Impossible to insert data. The specified columns does not match the existing schema.\n".encode("utf-8"))
                else:
                    i += 1

            if (len(columns) == i):
                written_obs = insert_obs(columns, values)


                msg = f"""
                {written_obs}

                inserted in the data file successfully.:smiley:
                """


                client.send(msg.encode("utf-8"))










    except KeyboardInterrupt:
        print("Fermeture de la connexion")
        client.close()
        serveur.close()






print("Connexion fermée")
client.close()
serveur.close()
