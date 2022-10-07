import random

import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def getRecentPatch():
    url = 'https://ddragon.leagueoflegends.com/api/versions.json'
    req = requests.get(url)
    jsondata = req.json()
    return jsondata[0]


def getDescription(champion):
    version = getRecentPatch()

    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/data/fr_FR/champion/' + champion + '.json'
    data = requests.get(url).json()
    lore= data['data'][champion]['lore']
    nom = data['data'][champion]['name']
    return nom,lore

def hideChampionName(champion):
    nom,lore = getDescription(champion)
    return lore.replace(nom, 'NomDuChampion')


def getRandomChampion():
    version = getRecentPatch()

    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/data/fr_FR/champion.json'
    data = requests.get(url).json()
    champion = random.choice(list(data['data'].keys()))
    nom = data['data'][champion]['name']
    return champion,nom

def getUltimate(champion):
    version = getRecentPatch()

    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/data/fr_FR/champion/' + champion + '.json'
    data = requests.get(url).json()
    return data['data'][champion]['spells'][3]['name']

def whoIsTheChampion():
    champion,nom = getRandomChampion()
    return nom,champion, hideChampionName(champion)


def whoIsTheUltimate():
    champion,nom = getRandomChampion()
    return nom,champion, getUltimate(champion)

# =============================================================================
#LOR API
# =============================================================================

def getInventory():
    url = "https://europe.api.riotgames.com/lor/ranked/v1/leaderboards"
    headers = {
        "X-Riot-Token": "RGAPI-96aa447c-b9b9-4e68-adc9-fbe2a3378e26"
    }
    req = requests.get(url, headers=headers)
    return req.json()

