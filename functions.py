import random
from genericpath import exists

import pandas as pd
from riotwatcher import LolWatcher, ApiError

# golbal variables
api_key = 'RGAPI-0fb667f2-e3fa-447c-bf05-2e7309bc0a4b'
watcher = LolWatcher(api_key)
my_region = 'euw1'


def get_player_rank_status(id_list):
    rank_data = []
    for i in id_list:
        try:
            my_ranked_stats = watcher.league.by_summoner(my_region, i['id'])
            rank_data.append(my_ranked_stats)
        except ApiError as err:
            print(err) 
    return rank_data  

def list_of_dict_to_df(list_of_dict):
    index = 0
    df = pd.DataFrame()
    for i in list_of_dict:
        if index == 0:
            df = pd.DataFrame(i)
            index += 1
        else:
            df = df.append(pd.DataFrame(i))
    return df[(df.queueType == "RANKED_SOLO_5x5")]

def write_to_csv(df):
    if not exists('lol_rank.csv'):
        df.to_csv('lol_rank.csv', index=False)
    else:
        df.to_csv('lol_rank.csv', mode='a', header=True, index=False)
        
def create_rank(row, tier_dict, rank_dict):
    return  row['leaguePoints'] + tier_dict[str(row['tier'])] + rank_dict[str(row['rank'])]

def create_rank_col(df):
    df['rank_points'] = df.apply(lambda row: create_rank(row), axis=1)
    return df

def create_dict_from_tables(player, player_rank):
    dict_player = {}
    for i in range(len(player)):
        dict_player[player[i]] = player_rank[i]
    return dict_player

def create_dict_rank(list_player, rank_soloq):
    rank_player = []
    for player in list_player:
        if player == 'Naretto95':
            rank_player.append(800)
        else:
            rank_player.append(rank_soloq.loc[rank_soloq['summonerName'] == player]['rank_points'].values[0])
    return create_dict_from_tables(list_player, rank_player)

def create_two_random_team_from_dict(dict_player):
    team1 = []
    team2 = []
    list_player = list(dict_player.keys())
    for i in range(5):
        team1.append(list_player[random.randint(0, len(list_player)-1)])
        list_player.remove(team1[i])
        team2.append(list_player[random.randint(0, len(list_player)-1)])
        list_player.remove(team2[i])
    return team1, team2

def get_rank_of_team(team, dict_rank):
    rank_team = 0
    for player in team:
        rank_team += dict_rank[player]
    return rank_team

def balance_team(team1, team2, dict_rank):
    rank_diff = abs(get_rank_of_team(team1, dict_rank) - get_rank_of_team(team2, dict_rank))
    while rank_diff > 300:
        team1, team2 = create_two_random_team_from_dict(dict_rank)
        team1, team2 = balance_team(team1, team2, dict_rank)
        rank_diff = abs(get_rank_of_team(team1, dict_rank) - get_rank_of_team(team2, dict_rank))
    print('difference is : ', rank_diff)
    return team1, team2

def create_id_list(message):
    list_id = []
    x=message.split(" ")
    for i in x[1:]:
            i = i.replace("<", "")
            i = i.replace(">", "")
            i = i.replace("@", "")
            list_id.append(i)
    return list_id

def clean_id(id):
    id = id.replace("<", "")
    id = id.replace(">", "")
    id = id.replace("@", "")
    return id

def create_teams(list_joueur):
    random.shuffle(list_joueur)
    team1 = list_joueur[0:5]
    team2 = list_joueur[5:10]
    return team1, team2

def mettre_en_tete(liste, element):
    liste.remove(element)
    liste.insert(0, element)
    return liste

def check_rpc(J1_reponse,J2_reponse):
    if J1_reponse == J2_reponse:
        return "Tie"
    else:
        if J1_reponse== "Pierre" :
            if J2_reponse=="Feuille":
                return "J2_Won"
            else:
                return "J1_Won"
        elif J1_reponse=="Feuille":
            if J2_reponse=="Pierre":
                return "J1_Won"
            else:
                return "J2_Won"
        else :
            if J2_reponse =="Pierre":
                return "J2_Won"
            else :
                return "J1_Won"



