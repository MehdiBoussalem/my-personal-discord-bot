import random
import urllib
import json

import discord
import pypokedex
from PIL import Image, ImageDraw, ImageFilter
import requests
from urllib import request
import os

from MyPokemon import *

# cree une liste du nom de pokedex avec le fichier liste_pokemon.csv
pokedex = []

with open('liste_pokemon/liste_pokemon.csv', 'r') as f:
    for line in f:
        pokedex.append(line.strip())
list_attaque_non_acceptee = []
with open('liste_pokemon/liste_attaque_non_degats.csv', 'r') as f:
    for line in f:
        list_attaque_non_acceptee.append(line.strip())


def create_random_team_pokemon(pokedex):
    # cree une liste de pokemon aleatoire
    random_team1 = []
    random_team2 = []
    for i in range(6):
        random_team1.append(pypokedex.get(name=pokedex[random.randint(0, len(pokedex) - 1)]))
        random_team2.append(pypokedex.get(name=pokedex[random.randint(0, len(pokedex) - 1)]))

    return random_team1, random_team2


def afficher_team(team):
    team_str = ' '
    for pokemon in team:
        team_str += pokemon.name + " "
    return team_str


def create_team_picture(team):
    image_de_fond = Image.open("fond.png")
    image_equipe = image_de_fond.copy().convert("RGBA")
    for i in range(0, 6):
        url = team[i].sprite_front
        nom_image = str(team[i].id) + ".png"
        request.urlretrieve(url, nom_image)
        image_pokemon = Image.open(nom_image).convert("RGBA")
        image_equipe.paste(image_pokemon, (100 * i, 0), mask=image_pokemon)
        os.remove(nom_image)
    image_equipe.save("image_equipe.png", quality=95, format="png")


def create_battle_picture(pokemonJ1, pokemonJ2):
    image_de_fond = Image.open("pokemon_background.png")
    image_combat_J1 = image_de_fond.copy().convert("RGBA")
    image_combat_J2 = image_de_fond.copy().convert("RGBA")
    # image coté J1 :
    urlJ1 = pokemonJ1.sprite_back
    urlJ2 = pokemonJ2.sprite_front
    nom_imageJ1 = str(pokemonJ1.id) + ".png"
    nom_imageJ2 = str(pokemonJ2.id) + ".png"
    request.urlretrieve(urlJ1, nom_imageJ1)
    request.urlretrieve(urlJ2, nom_imageJ2)
    image_pokemonJ1 = Image.open(nom_imageJ1).convert("RGBA")
    image_pokemonJ2 = Image.open(nom_imageJ2).convert("RGBA")
    image_combat_J1.paste(image_pokemonJ1, (30, 160), mask=image_pokemonJ1)
    image_combat_J1.paste(image_pokemonJ2, (250, 75), mask=image_pokemonJ2)
    image_combat_J1.save("image_combat_J1.png", quality=95, format="png")
    os.remove(nom_imageJ1)
    os.remove(nom_imageJ2)
    # image coté J2
    urlJ2 = pokemonJ2.sprite_back
    urlJ1 = pokemonJ1.sprite_front
    request.urlretrieve(urlJ1, nom_imageJ1)
    request.urlretrieve(urlJ2, nom_imageJ2)
    image_pokemonJ1 = Image.open(nom_imageJ1).convert("RGBA")
    image_pokemonJ2 = Image.open(nom_imageJ2).convert("RGBA")
    image_combat_J2.paste(image_pokemonJ2, (30, 160), mask=image_pokemonJ2)
    image_combat_J2.paste(image_pokemonJ1, (250, 75), mask=image_pokemonJ1)
    image_combat_J2.save("image_combat_J2.png", quality=95, format="png")
    os.remove(nom_imageJ1)
    os.remove(nom_imageJ2)


def create_MyPokemon(pokemon):
    moves = []
    all_moves = []
    key = random.choice(list(pokemon.moves))
    for i in range(0, len(pokemon.moves[key]) - 1):
        all_moves.append(pokemon.moves[key][i].name)
    while len(moves) < 4:
        move = random.choice(all_moves)
        if get_move_french_name(move) not in moves and move not in list_attaque_non_acceptee:
            moves.append(get_move_french_name(move))

    mypokemon = MyPokemon(name=get_pokemon_french_name(pokemon), level=50, type=pokemon.types[0],
                          hp=pokemon.base_stats.hp,
                          attack=pokemon.base_stats.attack, defense=pokemon.base_stats.defense,
                          speed=pokemon.base_stats.speed, sp_atk=pokemon.base_stats.sp_atk,
                          sp_def=pokemon.base_stats.sp_def, moves=moves, id=pokemon.dex,
                          sprite_front=pokemon.sprites.front['default'], sprite_back=pokemon.sprites.back['default'])
    return mypokemon


def create_MyPokemon_team(team):
    myteam = []
    for pokemon in team:
        myteam.append(create_MyPokemon(pokemon))
    return myteam


# get a json file from the pokemon api
def get_pokemon_french_name(pokemon):
    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(pokemon.dex) + "/"
    response = requests.get(url)
    data = response.json()
    return data['names'][4]['name']


def get_move_french_name(move):
    url = "https://pokeapi.co/api/v2/move/" + move + "/"
    response = requests.get(url)
    data = response.json()
    return data['names'][3]['name']


"""pokemon = pypokedex.get(dex=200)

pikachu = create_MyPokemon(pokemon)
team = create_random_team_pokemon(pokedex)[0]
team = create_MyPokemon_team(team)
for i in team:
    print(i.sprite_front)
"""

def getRandomPokemon():
    pokemon = pypokedex.get(name=pokedex[random.randint(0, len(pokedex) - 1)])
    return pokemon

def whoIsThatPokemon(pokemon):
        image_de_fond = Image.open("fond.png")
        image=image_de_fond.copy()
        url = pokemon.sprites.front['default']
        nom_image = str(pokemon.dex) + ".png"
        request.urlretrieve(url, nom_image)
        image_pokemon = Image.open(nom_image)
        image.paste(image_pokemon, (0, 0))
        image.save("pokemon/who_is_that_pokemon.png", quality=95, format="png")
        image=image_de_fond.copy().convert("RGBA")
        image_pokemon = Image.open(nom_image).convert("RGBA")

        image.paste(image_pokemon, (0, 0), mask=image_pokemon)
        image.save("pokemon/who_is_that_pokemon_reponse.png", quality=95, format="png")
        os.remove(nom_image)
        return pokemon





