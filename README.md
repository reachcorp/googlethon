# googlethon

## Prerequis
Installation des libs nécessaires

    pip install -r requirements.txt
    
### Démarrage du programme principale

    python googlethon.py

Argument :

    -n --number, nombre d'url retourné
    -e --endpoint, adresse:port Kafka
    -s --only_standard, urls renvoyés par google standard : True si non False

### Démarrage du bouchon

    python bouchongooglethon.py
Bouchon qui permet de générer de Biographics

### Démarrage du consumer

    python consumerTopic.py
Consumer s'abonne à un topic qui contient les résultats retournés par googlethon et qui les affiche
    
#### Format de données attendu dans la file Kafka
En entrée : {'nom': '', 'prenom': '', 'idBio': 'xxxx' }

En sortie : {'url': list[], 'nom': '', 'prenom': '', 'idBio': 'xxxx'}