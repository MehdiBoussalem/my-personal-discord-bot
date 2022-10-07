import asyncio
import datetime

import cassiopeia as cass
import discord
from discord import SelectOption
from discord.ext import tasks
from discord_components_mirror import Button, Select
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice


from Riot import *
from crypto import *
from functions import *
from pokemon import *
from spotify import *
from trivia import *
from twitch import *

config = configparser.ConfigParser()
config.read('config.ini')
print("test 1")
# set api
api_key = config['RIOT']['api']
cass.set_riot_api_key(api_key)
watcher = LolWatcher(api_key)
my_region = 'euw1'
isLive = False
print("test 2")

# global variables
discord_to_LoL = {'ZeQa': 'ZeQa', 'Alpha95': 'Alpha75', 'Mehdi': 'CPAS MEHDI', 'Baby Mate': 'Matei',
                  'pARAsol': 'lolo98100', 'Tomlife': 'Monsieur Life',
                  'Kelo': 'Kelo94', 'dark': 'Monsieur Sombre', 'pARAsol': 'lolo98100', 'Maeljeni': 'Maeljeni',
                  'FireWox': 'FireFraude'}
player = ['ZeQa', 'CPAS MEHDI', 'Alpha75', 'Matei', 'Monsieur Life', 'Maeljeni', 'FireFraude', 'Naretto95', 'gomape',
          'Monsieur Sombre']

tier_dict = {'IRON': 0, 'BRONZE': 400, 'SILVER': 800, 'GOLD': 1200, 'PLATINUM': 1600, 'DIAMOND': 2000, 'MASTER': 2400,
             'GRANDMASTER': 2400, 'CHALLENGER': 2400}
rank_dict = {'I': 300, 'II': 200, 'III': 100, 'IV': 0}

TOKEN = ""
print("test 3")

#liste_champions = cass.get_champions(region="EUW")
# print(liste_champions)
liste_champions_top = ["Akshan"]
liste_champions_jungle = []
liste_champions_mid = ["Akshan", "Vex"]
liste_champions_adc = ["Zeri"]
liste_champions_support = ["Renata Glasc"]
play_rate_min = 0.2
'''for i in liste_champions:
    if i.name != "Akshan" and i.name != "Renata Glasc" and i.name != "Vex" and i.name != "Zeri" and i.name != "Bel'Velth":
        if i.play_rates[Position.top] >= play_rate_min:
            liste_champions_top.append(i.name)
        if i.play_rates[Position.jungle] >= play_rate_min:
            liste_champions_jungle.append(i.name)
        if i.play_rates[Position.middle] >= play_rate_min:
            liste_champions_mid.append(i.name)
        if i.play_rates[Position.bottom] >= play_rate_min:
            liste_champions_adc.append(i.name)
        if i.play_rates[Position.utility] >= play_rate_min:
            liste_champions_support.append(i.name)'''

liste_role_among = ["Imposteur", "Serpentin", "SuperHéro", "Escroc", "Double Face"]

client = discord.Client()

slash = SlashCommand(client,sync_commands=True)
print("test 4")


# recupere une lis
# t de joueur en parametre et la renvoie qu'importe l'author
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # renvoie 2 équipe avec les 10 joueurs en parametre et leur attribue un champion au hasard en fonction de leur poste
    if message.content.startswith('!custom'):
        x = message.content.split(' ')
        listJoueur = x[1:]
        if len(listJoueur) == 10:
            random.shuffle(listJoueur)
            team1 = listJoueur[0:5]
            team2 = listJoueur[5:10]
            await message.channel.send(
                "team 1 : " + "\n" + "TOP : " + team1[0] + " " + random.choice(liste_champions_top) + "\n" + "JGL : " +
                team1[1] + " " + random.choice(liste_champions_jungle) + "\n" + "MID : " + team1[
                    2] + " " + random.choice(liste_champions_mid) + "\n" + "ADC : " + team1[3] + " " + random.choice(
                    liste_champions_adc) + "\n" + "SUP : " + team1[4] + " " + random.choice(
                    liste_champions_support) + "\n" + "team 2 : " + "\n" + " TOP :" + team2[0] + " " + random.choice(
                    liste_champions_top) + "\n" + " JGL : " + team2[1] + " " + random.choice(
                    liste_champions_jungle) + "\n" + " MID : " + team2[2] + " " + random.choice(
                    liste_champions_mid) + "\n" + " ADC : " + team2[3] + " " + random.choice(
                    liste_champions_adc) + "\n" + " SUP : " + team2[4] + " " + random.choice(liste_champions_support))
        else:
            await message.channel.send("Veuillez entrer 10 joueurs")
    # renvoie un toplaner aléatoire
    if message.content.startswith('!top'):
        await message.channel.send(random.choice(liste_champions_top))
    # renvoie un jungle aléatoire
    if message.content.startswith('!jgl'):
        await message.channel.send(random.choice(liste_champions_jungle))
    # renvoie un mid aléatoire
    if message.content.startswith('!mid'):
        await message.channel.send(random.choice(liste_champions_mid))
    # renvoie un adc aléatoire
    if message.content.startswith('!adc'):
        await message.channel.send(random.choice(liste_champions_adc))
    # renvoie un support aléatoire
    if message.content.startswith('!sup'):
        await message.channel.send(random.choice(liste_champions_support))
    # renvoie le lien probluid du Champion donnée en parametre
    if message.content.startswith('!probuild'):
        x = message.content.split(' ')
        await message.channel.send("https://probuildstats.com/champion/" + x[1])

    # Cree 2 équipes aléatoire automatiquement en prenant la liste des joeueurs présant dans le channel vocal de l'auteur et attribue un personnage aléatoire à chaque joueur en fonction de son poste
    if message.content.startswith('!vocalCustom'):
        await message.channel.send(message.author.voice.channel.name)
        channel = client.get_channel(message.author.voice.channel.id)

        ListeMembre = []
        for i in range(0, len(channel.members)):
            ListeMembre.append(channel.members[i].nick)
            print(channel.members[i].nick)
        # await message.channel.send(ListeMembre)
        if len(ListeMembre) == 10:
            random.shuffle(ListeMembre)
            team1 = ListeMembre[0:5]
            team2 = ListeMembre[5:10]
            await message.channel.send(
                "team 1 : " + "\n" + "TOP : " + team1[0] + " " + random.choice(liste_champions_top) + "\n" + "JGL : " +
                team1[1] + " " + random.choice(liste_champions_jungle) + "\n" + "MID : " + team1[
                    2] + " " + random.choice(liste_champions_mid) + "\n" + "ADC : " + team1[3] + " " + random.choice(
                    liste_champions_adc) + "\n" + "SUP : " + team1[4] + " " + random.choice(
                    liste_champions_support) + "\n" + "team 2 : " + "\n" + " TOP :" + team2[0] + " " + random.choice(
                    liste_champions_top) + "\n" + " JGL : " + team2[1] + " " + random.choice(
                    liste_champions_jungle) + "\n" + " MID : " + team2[2] + " " + random.choice(
                    liste_champions_mid) + "\n" + " ADC : " + team2[3] + " " + random.choice(
                    liste_champions_adc) + "\n" + " SUP : " + team2[4] + " " + random.choice(liste_champions_support))

        else:
            await message.channel.send("Veuillez etre seulement 10 joueurs dans le vocal")
    # renvoie 2 teams aléatoire en prenant la liste des joeueurs présant dans le channel vocal de l'auteur
    if message.content.startswith('!team'):
        channel = client.get_channel(message.author.voice.channel.id)
        ListeMembre = []
        for i in range(0, len(channel.members)):
            ListeMembre.append(channel.members[i].nick)
        random.shuffle(ListeMembre)
        team1 = ListeMembre[0:(len(ListeMembre) // 2)]
        team2 = ListeMembre[(len(ListeMembre) // 2):len(ListeMembre)]
        print(team1)
        print(team2)
        team1_Message = " "
        team2_Message = " "
        for i in team1:
            team1_Message = team1_Message + i + "\n"
        for i in team2:
            team2_Message = team2_Message + i + "\n"
        print(team1_Message)
        print(team2_Message)
        await message.channel.send("team 1: " + "\n" + team1_Message + "\n" + "team 2: " + "\n" + team2_Message)

    # help
    if message.content.startswith('!help'):
        print("help")
        url = "https://mehdi-boussalem.alwaysdata.net/discord/discord.html"
        await message.channel.send("Voici le lien de la page d'aide : " + url)

    # if le message commence par !fuckmate renvoie fuck mate de le tchat
    if message.content.startswith('!fuckmate'):
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/503292849576476684/963542505385758771/unknown.png")

    # if message author is 244123334143377408 renvoie un message
    # if message.author.id==393004612598104065:
    # await message.channel.send("https://cdn.discordapp.com/attachments/652938598055936003/963139856882630676/unknown.png")

    if message.content.startswith("!listTop"):
        await message.channel.send(liste_champions_top)
    if message.content.startswith("!listJgl"):
        await message.channel.send(liste_champions_jungle)
    if message.content.startswith("!listMid"):
        await message.channel.send(liste_champions_mid)
    if message.content.startswith("!listAdc"):
        await message.channel.send(liste_champions_adc)
    if message.content.startswith("!listSup"):
        await message.channel.send(liste_champions_support)

    # si le message commence par !testMp renvoie un message privé "test" a l'auteur ou envoie "veuillez activer les MP" si les MP sont désactivés
    if message.content.startswith('!testMp'):
        try:
            await message.author.create_dm()
            await message.author.dm_channel.send("test")
            msg = await client.wait_for('message', check=lambda message: message.content == "test")
            await message.channel.send("test")



        except Exception:
            await message.author.dm_channel.send("veuillez activer les MP")
            pass
    if message.content.startswith('!Among'):
        x = message.content.split(' ')
        id_channel = message.channel.id
        role_double_face = random.randint(0, 1)  # 0=imposteur 1=gentil
        list_id = create_id_list(message.content)
        list_joueur = []
        if len(list_id) != 10:
            await message.channel.send("Veuillez etre 10 pour lancer une partie ")
        else:
            for i in list_id:
                user = await client.fetch_user(i)
                list_joueur.append(user)

            team1, team2 = create_teams(list_joueur)
            print(team1, team2)
            x = 0
            for i in team1:
                user = i
                await user.create_dm()
                await user.dm_channel.send("Tu es : " + liste_role_among[x] + "et tu est dans la team 1")
                x += 1
            y = 0
            for i in team2:
                user = i
                await user.create_dm()
                await user.dm_channel.send("Tu es : " + liste_role_among[y] + "et tu est dans la team 2")
                y += 1
            user1 = team1[4]
            user2 = team2[4]
            await user1.create_dm()
            await user2.create_dm()
            if role_double_face == 0:
                await user1.dm_channel.send("Tu es Inposteur ")
                await user2.dm_channel.send("Tu es Inposteur ")
            else:
                await user1.dm_channel.send("Tu es Gentil ")
                await user2.dm_channel.send("Tu es Gentil ")

            game_end = False
            compteur = 0
            timer_swap_double_face = random.randint(180, 300)
            await message.channel.send("Enter !start dés que la partie se lance !")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            while not msg.content.startswith("!start"):
                await message.channel.send("Veuillez entrer !start pour commencer la partie")
                msg = await client.wait_for('message', check=lambda
                    message: message.author == message.author and message.channel == message.channel)
            while not game_end:
                await asyncio.sleep(1)
                print("test : " + str(compteur))
                compteur += 1
                channel = client.get_channel(int(id_channel))
                last_message = await channel.fetch_message(channel.last_message_id)
                if compteur == timer_swap_double_face:

                    if role_double_face == 0:
                        await user1.dm_channel.send("Tu es imposteur maintenant  ")
                        await user2.dm_channel.send("Tu es imposteur maintenant")
                        role_double_face = 1
                    else:
                        await user1.dm_channel.send("Tu es gentil maintenant  ")
                        await user2.dm_channel.send("Tu es gentil maintenant")
                        role_double_face = 0
                    compteur = 0

                if last_message.content.startswith("!end"):
                    await message.channel.send("fin de la partie ! Place aux votes")
                    game_end = True

            await message.channel.send("Vote pour la team 1")
            await message.channel.send(
                "Qui etait l'imposteur ? " + "\n" + "+10pts si vous avez bon. Sauf pour l'Insposteur , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("L'inspoteur etait : " + team1[0].name)
            await message.channel.send(
                "Qui était le Serpentin ? " + "\n" + "+5pts si vous avez bon. Sauf pour le Serpentin , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("Le Serpentin etait : " + team1[1].name)
            await message.channel.send(
                "Qui était le SuperHéro ? " + "\n" + "+5pts si vous avez bon. Sauf pour le SuperHéro , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("le SuperHéro etait : " + team1[2].name)
            await message.channel.send(
                "Qui était l'Escroc ? " + "\n" + "+5pts si vous avez bon. Sauf pour l'Escroc , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("l'Escroc etait : " + team1[3].name)
            await message.channel.send(
                "Qui etait le Double Face ? " + "\n" + "+5pts si vous avez bon. Sauf pour le Double Face , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("le Double Face etait : " + team1[4].name)
            await message.channel.send("Vote pour la team 2")
            await message.channel.send(
                "Qui etait l'imposteur ? " + "\n" + "+10pts si vous avez bon. Sauf pour l'Insposteur , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("L'inspoteur etait : " + team2[0].name)
            await message.channel.send(
                "Qui était le Serpentin ? " + "\n" + "+5pts si vous avez bon. Sauf pour le Serpentin , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("Le Serpentin etait : " + team2[1].name)
            await message.channel.send(
                "Qui était le SuperHéro ? " + "\n" + "+5pts si vous avez bon. Sauf pour le SuperHéro , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("le SuperHéro etait : " + team2[2].name)
            await message.channel.send(
                "Qui était l'Escroc ? " + "\n" + "+5pts si vous avez bon. Sauf pour l'Escroc , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("l'Escroc etait : " + team2[3].name)
            await message.channel.send(
                "Qui etait le Double Face ? " + "\n" + "+5pts si vous avez bon. Sauf pour le Double Face , il ne peut pas se voter lui meme pour des points ")
            msg = await client.wait_for('message', check=lambda
                message: message.author == message.author and message.channel == message.channel)
            if msg.content.startswith("!done"):
                await message.channel.send("le Double Face etait : " + team2[4].name)
            await message.channel.send(
                "Maintenant rajoutez-vous chacuns 15 points si vous avez réussis votre objectif de fin de partie mais -15pts si echec")
            await message.channel.send("Fin de la partie")

    if message.content.startswith('!balance_team'):
        await message.channel.send(message.author.voice.channel.name)
        channel = client.get_channel(message.author.voice.channel.id)
        ListeMembre = []
        for i in range(0, len(channel.members)):
            ListeMembre.append(channel.members[i].name)
            id_player = [watcher.summoner.by_name(my_region, discord_to_LoL[p]) for p in ListeMembre]
        # await message.channel.send(ListeMembre)
        if len(ListeMembre) == 10:
            rank_data = get_player_rank_status(id_player)
            rank_soloq = list_of_dict_to_df(rank_data)
            rank_soloq = create_rank_col(rank_soloq)
            dict_rank = create_dict_rank(player)
            team1, team2 = create_two_random_team_from_dict(dict_rank)
            team1, team2, diff_rank = balance_team(team1, team2, dict_rank)
            team1_Message = " "
            team2_Message = " "
            for i in team1:
                team1_Message = team1_Message + i + "\n"
            for i in team2:
                team2_Message = team2_Message + i + "\n"
            await message.channel.send(
                "team 1: " + "\n" + team1_Message + "\n" + "team 2: " + "\n" + team2_Message + "\n" + "différence de rank: " + "\n" + str(
                    diff_rank))
        else:
            await message.channel.send("Veuillez etre seulement 10 joueurs dans le vocal")
    if message.content.startswith('!buttonTest'):
        await message.channel.send("Quel type de joueur es-tu ? ",
                                   components=[Button(label="découvrir", style="1", custom_id="test",
                                                      emoji=client.get_emoji(826387964375597066))])
        event = await client.wait_for('button_click', check=lambda i: i.custom_id == "test")
        # random number betweenn 1 and 2
        random_number = random.randint(1, 2)
        if random_number == 1:
            await event.send(content="Tu es le Mec 1vs9 dans tes games ", ephemeral=False)
        else:
            await event.send(content="Tes le pire joueur de tous les temps ", ephemeral=False)

    if message.content.startswith('!pokemonDuel'):
        await pokemonDuel(message)
    if message.content.startswith('!rpc'):
        await rock_paper_scissor(message)
    if message.content.startswith("!whoPokemon"):
        await whoPokemon(message)
    if message.content.startswith("!blindTest"):
        await blindTest(message)
    if message.content.startswith("!trivia"):
        await getTriviaQuestion(message)
    if message.content.startswith("!whoLeague"):
        await whoLeague(message)
    if message.content.startswith("!mario"):
        await marioFoot(message)
    if message.content.startswith("!TLBlindTest"):
        await blindTestTL(message)



@client.event
async def pokemonDuel(message):
    x = message.content.split(" ")
    J1 = message.author
    J2 = await client.fetch_user(clean_id(x[1]))
    msg = await message.channel.send(x[1] + "Acceptez-vous le duel ?",
                                     components=[Button(label="oui", style="3", custom_id="oui"),
                                                 Button(label="non", style="4", custom_id="non")])
    game = False
    while True:
        button = await client.wait_for('button_click')
        if button.custom_id == "oui" and button.author == J2:
            await msg.edit("Le combat va commencer", compenents=[])
            game = True
            break
        if button.custom_id == "non" and button.author == J2:
            await msg.edit(content="Le combat a été refusé ", components=[])
            game = False
            break
        if button.author != J2:
            await button.respond(content="tu n'est pas le joueur 2 donc pourquoi tu réponds ????", ephemeral=True)

    if game:
        await message.channel.send("Duel Pokemon lancé avec :" + "\n" + J1.mention + " VS " + J2.mention)
        team1, team2 = create_random_team_pokemon(pokedex)
        team1, team2 = create_MyPokemon_team(team1), create_MyPokemon_team(team2)
        await J1.create_dm()
        await J2.create_dm()
        await J1.dm_channel.send("Ton équipe Pokemon est :" + afficher_team(team1))
        create_team_picture(team1)
        await J1.dm_channel.send(file=discord.File("image_equipe.png"))

        await J2.dm_channel.send("Ton équipe Pokemon est :" + afficher_team(team2))
        create_team_picture(team2)
        await J2.dm_channel.send(file=discord.File("image_equipe.png"))
        await J2.dm_channel.send("En attente du tour de " + J1.name)
        msg_J1 = await J1.dm_channel.send("Quel pokemon envoie-tu en premier  ?",
                                          components=[Select(placeholder="Choisis ton pokemon", options=
                                          [SelectOption(label=team1[0].name, value="0"),
                                           SelectOption(label=team1[1].name, value="1"),
                                           SelectOption(label=team1[2].name, value="2"),
                                           SelectOption(label=team1[3].name, value="3"),
                                           SelectOption(label=team1[4].name, value="4"),
                                           SelectOption(label=team1[5].name, value="5")])])
        select = await client.wait_for("select_option")
        team1 = mettre_en_tete(team1, team1[int(select.values[0])])

        await msg_J1.edit(content=team1[0].name + " sera envoyé en premier", components=[])
        create_team_picture(team1)
        await J1.dm_channel.send(file=discord.File("image_equipe.png"))
        await J1.dm_channel.send("En attente de " + J2.name)

        msg_J2 = await J2.dm_channel.send("Quel pokemon envoie-tu en premier  ?",
                                          components=[  Select(placeholder="Choisis ton pokemon", options=

                                          [SelectOption(label=team2[0].name, value="0"),
                                           SelectOption(label=team2[1].name, value="1"),
                                           SelectOption(label=team2[2].name, value="2"),
                                           SelectOption(label=team2[3].name, value="3"),
                                           SelectOption(label=team2[4].name, value="4"),
                                           SelectOption(label=team2[5].name, value="5")])])
        select = await client.wait_for("select_option")
        team2 = mettre_en_tete(team2, team2[int(select.values[0])])
        await msg_J2.edit(content=team2[0].name + " sera envoyé en premier", components=[])
        create_team_picture(team2)
        await J2.dm_channel.send(file=discord.File("image_equipe.png"))
        await J2.dm_channel.send("En attente de " + J1.name)
        create_team_picture(team1)
        await message.channel.send(file=discord.File("image_equipe.png"), content="Equipe de : " + J1.name)
        create_team_picture(team2)
        await message.channel.send(file=discord.File("image_equipe.png"), content="VS" + "\n" + "Equipe de :" + J2.name)
        create_battle_picture(team1[0], team2[0])
        await message.channel.send(file=discord.File("image_combat_J1.png"))
        pokemon_actif_J1 = 0
        pokemon_actif_J2 = 0
        # while True:
        await J1.dm_channel.send(file=discord.File("image_combat_J1.png"),
                                 components=[[Button(label="1"), Button(label="2"), Button(label="3")],
                                             [Button(label="4"), Button(label="5")]])
        await J2.dm_channel.send(file=discord.File("image_combat_J2.png"))


async def whoPokemon(message):
    pokemon = whoIsThatPokemon(getRandomPokemon())
    await message.channel.send("Quel est ce Pokemon ?", file=discord.File("pokemon/who_is_that_pokemon.png"))
    msg = await client.wait_for('message', check=lambda x: message.author == x.author and message.channel == x.channel)
    # si l'id de l'auteur est = a 689126931643629623
    if msg.author.id == 689126931643629623:
        await message.channel.send("Bravo Candice ! Le pokemon était bien " + msg.content + " ^^",
                                   file=discord.File("pokemon/who_is_that_pokemon_reponse.png"))
    else:
        await message.channel.send("le pokemon etait :" + get_pokemon_french_name(pokemon),
                                   file=discord.File("pokemon/who_is_that_pokemon_reponse.png"))

@slash.slash(name="RPC", description="Joue au pierre feuille ciseaux contre quelqu'un",options=[create_option(name="joueur",description="Le joueur contre qui tu veux jouer",option_type=6,required=True)])
async def rock_paper_scissor(message, joueur):

    J1 = message.author
    J2 = joueur
    print("test")
    await message.send(J2.name + "Acceptez-vous le duel ?",
                               components=[Button(label="oui", style="1", custom_id="oui"),
                                           Button(label="non", style="1", custom_id="non")])
    game = False
    while True:
        button = await client.wait_for('button_click')
        if button.custom_id == "oui" and button.author == J2:
            await button.respond(content="Le duel va commencer ", ephemeral=False)
            game = True
            break
        if button.custom_id == "non" and button.author == J2:
            await button.respond(content="Le duel est annulé", ephemeral=False)
            game = False
            break
        if button.author != J2:
            await button.respond(content="tu n'est pas le joueur 2 donc pourquoi tu réponds ????", ephemeral=True)
    if game == True:
        await message.channel.send(
            "Duel de Pierre Feuille Ciseau lancé avec :" + "\n" + J1.mention + " VS " + J2.mention)
        await J1.create_dm()
        await J2.create_dm()
        msg_J1 = await J1.dm_channel.send("Quel est ton choix ?",
                                          components=[Button(label="Pierre", style="1", custom_id="Pierre"),
                                                      Button(label="Feuille", style="1", custom_id="Feuille"),
                                                      Button(label="Ciseau", style="1", custom_id="Ciseau")])
        await J2.dm_channel.send("En attente du J1...")
        button = await client.wait_for("button_click")
        J1_choix = button.custom_id
        await msg_J1.edit(content="ton choix etait :" + J1_choix, components=[])
        await button.respond(content="En attente du J2...", ephemeral=False)
        msg_J2 = await J2.dm_channel.send("Quel est ton choix ?",
                                          components=[Button(label="Pierre", style="1", custom_id="Pierre"),
                                                      Button(label="Feuille", style="1", custom_id="Feuille"),
                                                      Button(label="Ciseau", style="1", custom_id="Ciseau")])
        button = await client.wait_for("button_click")
        J2_choix = button.custom_id

        await msg_J2.edit(content="ton choix etait : " + J2_choix, components=[])
        if check_rpc(J1_choix, J2_choix) == "J1_Won":
            await message.channel.send(J1.mention + " a gagné")
        else:
            await message.channel.send(J2.mention + " a gagné")

@slash.slash(name="Bitcoin", description="Donne le cours du bitcoin")
async def bitcoin(message):
    btc_price, evolution, cryto_name, eth_price, eth_evolution, eth_name = get_btc_price()
    if evolution >= 0:
        text2 = cryto_name + " : " + str(btc_price) + "€ +" + str(evolution) + "% sur les 7 derniers jours"
    else:
        text2 = cryto_name + " : " + str(btc_price) + "€ " + str(evolution) + "% sur les 7 derniers jours"
    if eth_evolution > 0:
        text3 = eth_name + " : " + str(eth_price) + "€ +" + str(eth_evolution) + "% sur les 7 derniers jours"
    else:
        text3 = eth_name + " : " + str(eth_price) + "€ " + str(eth_evolution) + "% sur les 7 derniers jours "

    text = text2 + "\n" + text3
    await message.send(text)


async def blindTest(message):
    x = message.content.split(" ")
    artist = x[1:]
    if artist == []:
        return await message.channel.send("Veuillez entrer un artiste")
    artist = " ".join(artist)
    lyrics, track = randomLyrics(artist)
    await message.channel.send(lyrics)
    msg = await client.wait_for('message', check=lambda x: message.author == x.author and message.channel == x.channel)
    if msg.content.lower() == track.lower():
        await message.channel.send("Bravo " + message.author.mention + " tu as trouvé le bon titre")
    else:
        await message.channel.send(
            "Dommage " + message.author.mention + " tu n'as pas trouvé . Le bon titre était : " + track)
async def blindTestTL(message):
    x = message.content.split(" ")
    artist = x[1:]
    if artist == []:
        return await message.channel.send("Veuillez entrer un artiste")
    artist = " ".join(artist)
    lyrics, track = translatedLyrics(artist, "FR")
    await message.channel.send(lyrics)
    msg = await client.wait_for('message', check=lambda x: message.author == x.author and message.channel == x.channel)
    if msg.content.lower() == track.lower():
        await message.channel.send("Bravo " + message.author.mention + " tu as trouvé le bon titre")
    else:
        await message.channel.send(
            "Dommage " + message.author.mention + " tu n'as pas trouvé . Le bon titre était : " + track)


async def getTriviaQuestion(message):
    x = message.content.split(" ")
    if len(x) == 1:
        catogory, question, correct_answer, incorrect_answers, is_boolean = getQuestion(
            "https://opentdb.com/api.php?amount=1")
    elif x[1] == "liste":
        catogories = []
        with open('categories.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                catogories.append(row[0])
        texte = "Voici la liste des catégories : \n"
        for cat in catogories:
            texte += cat + "\n"
        await message.channel.send(texte)
        return
    elif x[1] == "help":
        await message.channel.send(
            "Pour obtenir une question d'une catégorie, entrez !trivia <catégorie>" + "\n" + "Pour obtenir la liste des catégories, entrez !trivia liste" + "\n" + "Sinon entrez !trivia pour obtenir une question aléatoire")
        return








    else:
        # categories = categories.csv
        catogory = x[1:]
        catogory = " ".join(catogory)
        catogory = catogory.upper()
        # creation de la liste des categories avec catogories.csv
        catogories = []
        with open('categories.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                line = [row[0], row[1]]
                catogories.append(line)
        for i in catogories:
            if catogory == i[0]:
                catogory = i[1]
                break
        catogory, question, correct_answer, incorrect_answers, is_boolean = getQuestion(
            "https://opentdb.com/api.php?amount=1&category=" + str(catogory))

    embed = discord.Embed(title=question, description=catogory, color=0x00ff00)
    embed.add_field(name="Joueur", value=message.author.mention, inline=False)
    if is_boolean == True:

        msg = await message.channel.send(embed=embed, components=[
            [Button(label="Vrai", style="3", custom_id="True"), Button(label="Faux", style="4", custom_id="False")]])
        while True:
            button = await client.wait_for('button_click')
            if button.custom_id == correct_answer and button.author == message.author:
                # bonne réponse
                await msg.edit(embed=embed, components=[])
                await button.respond(content="Bravo tu as trouvé la bonne réponse qui était : " + correct_answer,
                                     ephemeral=False)
                break
            if button.custom_id != correct_answer and button.author == message.author:
                # mauvaise réponse
                await msg.edit(embed=embed, components=[])
                await button.respond(
                    content="Dommage tu as choisis la mauvaise réponse la bonne était  : " + correct_answer,
                    ephemeral=False)

                break
            if button.author != message.author:
                await button.respond(content="je te pose pas la question à toi  donc pourquoi tu réponds ????",
                                     ephemeral=True)
        return
    else:
        reponses = incorrect_answers + [correct_answer]
        random.shuffle(reponses)
        msg = await message.channel.send(embed=embed, components=[
            [Button(label=reponses[0], style="1", custom_id=reponses[0]),
             Button(label=reponses[1], style="1", custom_id=reponses[1])],
            [Button(label=reponses[2], style="1", custom_id=reponses[2]),
             Button(label=reponses[3], style="1", custom_id=reponses[3])]])
        while True:
            button = await client.wait_for('button_click')
            if button.custom_id == correct_answer and button.author == message.author:
                # bonne réponse
                await msg.edit(embed=embed, components=[])
                await button.respond(content="Bravo tu as trouvé la bonne réponse qui était : " + correct_answer,
                                     ephemeral=False)
                break
            if button.custom_id != correct_answer and button.author == message.author:
                # mauvaise réponse
                await msg.edit(embed=embed, components=[])
                await button.respond(
                    content="Dommage tu as choisis la mauvaise réponse la bonne était  : " + correct_answer,
                    ephemeral=False)

                break
            if button.author != message.author:
                await button.respond(content="je te pose pas la question à toi  donc pourquoi tu réponds ????",
                                     ephemeral=True)
        return


async def whoLeague(message):
    x = message.content.split(" ")
    if len(x) == 1:
        nom, champion, description = whoIsTheChampion()
        await message.channel.send(description)
        msg = await client.wait_for('message',
                                    check=lambda x: message.author == x.author and message.channel == x.channel)
        if msg.content.lower() == champion.lower() or msg.content.lower() == nom.lower():
            await message.channel.send("Bravo " + message.author.mention + " tu as trouvé le champion")
        else:
            await message.channel.send(
                "Dommage " + message.author.mention + " tu n'as pas trouvé . Le champion était : " + nom)
    else:
        if x[1] == "Ultime":
            nom, champion, ultimate = whoIsTheUltimate()
            await message.channel.send("A quel champion appartient cet compétence ultime : " + ultimate)
            msg = await client.wait_for('message',
                                        check=lambda x: message.author == x.author and message.channel == x.channel)
            if msg.content.lower() == champion.lower() or msg.content.lower() == nom.lower():
                await message.channel.send("Bravo " + message.author.mention + " tu as trouvé le champion")
            else:
                await message.channel.send(
                    "Dommage " + message.author.mention + " tu n'as pas trouvé . Le champion était : " + nom)


async def marioFoot(message):
    # timer jusqu'a le jeu sorte
    # date de sortie du jeu : 10 juin 2022
    date_aujourdhui = datetime.datetime.now()
    date_sortie = datetime.datetime(2022, 6, 10)
    delta = date_sortie - date_aujourdhui
    # en jours + heures + minutes+ secondes
    jours = delta.days
    heures = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    secondes = delta.seconds % 60
    await message.channel.send(
        "Mario Strickers : Battle League Football sortira dans : " + str(jours) + " jours " + str(
            heures) + " heures " + str(minutes) + " minutes " + str(secondes) + " secondes")

@slash.slash(name="Help", description="Donne la liste des commandes")
async def help(message):
    url = "https://mehdi-boussalem.alwaysdata.net/discord/discord.html"
    await message.send("Voici le lien de la page d'aide : " + url)




@tasks.loop(seconds=15.0)
async def checkStream():
    global isLive
    if isStreaming("CPAS_MEHDI"):
        await client.get_channel(975855471854506084).send(
            "Le stream de Mehdi est en cours" + "\n" + "https://www.twitch.tv/cpas_mehdi")  # channel LeagueMaTousPris
        await client.get_channel(244462451410599938).send(
            "Le stream de Mehdi est en cours" + "\n" + "https://www.twitch.tv/cpas_mehdi")  # channel babyGang
        if isLive:
            isLive = True
            print("Le stream de Mehdi est en cours")
    else:
        if isLive:
            isLive = False
            print("Le stream de Mehdi est fini")



checkStream.start()
print("bot is running")

client.run(TOKEN)
