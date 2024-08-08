import torch
import torch.nn as nn # All neural network modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim # For all Optimization algorithms, SGD, Adam, etc.
import torch.nn.functional as F # All functions that don't have any parameters
from torch.utils.data import DataLoader # Gives easier dataset managment and creates mini batches
import torchvision.datasets as datasets # Has standard datasets we can import in a nice and easy way
import torchvision.transforms as transforms # Transformations we can perform on our dataset
from LeagueDataset import LeagueDataset
from torch.utils.data import DataLoader
from NeuralNetwork import proplay_prediction as network
from torch.optim.lr_scheduler import StepLR
from NeuralNetwork import proplay_prediction as Model
import LeagueDatabase as ld
import Datascraper as dsc
import sqlite3

istop1 = [False]
player_format = {
    'top' : [1,2,3,4,5,6,7,8,9,10,11,16],
    'jg' : [1,2,3,4,5,6,7,8,9,10,11,16],
    'mid' : [1,2,3,4,5,6,7,8,9,10,11,16],
    'adc' : [1,2,3,4,5,6,7,8,9,10,11,16],
    'sup' : [1,2,3,4,5,6,12]

}

lane_format = {
    0 : 'top',
    1 : 'jg',
    2 : 'mid',
    3 : 'adc',
    4 : 'sup'

}
def calculate_comfortability(stats, avg_stats, min_games=1):
    """
    Calculate the comfortability score based on player stats and champion's average stats.

    Parameters:
    stats (dict): Player's stats with keys 'Games', 'Winrate', 'KDA', 'CS/MIN', 'GOLD/MIN'.
    avg_stats (dict): Champion's average stats with keys 'AVG_Winrate', 'AVG_KDA', 'AVG_CS/MIN', 'AVG_GOLD/MIN'.
    min_games (int): Minimum number of games to adjust the comfortability score.

    Returns:
    float: Comfortability score.
    """

    if len(stats) == 0:
        return 0

    # Extract player's stats
    games = stats["Games"]
    winrate = stats["Winrate"]
    kda = stats["KDA"]
    cs_min = stats["CS/MIN"]
    gold_min = stats["GOLD/MIN"]

    # Extract champion's average stats
    avg_winrate = avg_stats["AVG_Winrate"]
    avg_kda = avg_stats["AVG_KDA"]
    avg_cs_min = avg_stats["AVG_CS/MIN"]
    avg_gold_min = avg_stats["AVG_GOLD/MIN"]

    # Calculate raw comfortability score
    raw_score = (
        (cs_min - avg_cs_min) +
        (gold_min - avg_gold_min) +
        (kda - avg_kda)
    )

    # Calculate the game factor
    game_factor = games / (games + min_games)

    # Adjust the comfortability score
    comfortability_score = raw_score * game_factor

    return comfortability_score
#loaded my model
myModel = Model(95)
myModel.load_state_dict(torch.load('PlayerComfortabilityIncluded.pth'))
myModel.eval()

#have to grab my data for a game

players = sqlite3.connect('PlayerStats.db')
champs = sqlite3.connect('ChampionStats.db')

player_cursor = players.cursor()
champs_cursor = champs.cursor()

"""#FLYQUEST VS LIQUID (LCS SPring Playoffs 2024) 2/4 correct (wrong,wrong,correct,correct)
Fly_Players = ['Bwipo','Inspired','Jensen','Massu','Busio']
Liquid_Players = ['Impact','UmTi','APA','Yeon','CoreJJ']


Fly_champs = ['Renekton','LeeSin','Annie','Kalista','Nautilus']
Liquid_champs = ['KSante','Sejuani','Taliyah','Varus','TahmKench']"""


"""#C9 VS LIQUID (1/3) right,wrong,wrong
C9_Players = ['Fudge','Blaber','jojopyun','Berserker','Vulcan']
Liquid_Players = ['Impact','UmTi','APA','Yeon','CoreJJ']

C9_champs = ['Olaf','XinZhao','Karma','Lucian','Nami']
Liquid_champs = ['Renekton','Vi','Ziggs','Varus','Rell']"""

def setup(Team1_Players,Team2_Players,Team1_Champs,Team2_Champs, season):
    entry = []
    #deal with players first
    for i in range(0,len(Team1_Players)):
        lane = lane_format[i]
        for value in player_format[lane]:
            team1_person = ld.retrieve_player(player_cursor,season,Team1_Players[i])[0][value]
            team2_person = ld.retrieve_player(player_cursor,season,Team2_Players[i])[0][value]

            if '%' in team1_person:
                team1_person = team1_person[:-1]
                team2_person = team2_person[:-1]

            if '-' == team1_person:
                team1_person = 0
                team2_person = 0

            team1_person = float(team1_person)
            team2_person = float(team2_person)

            difference = team1_person - team2_person
            entry.append(difference)

    
    #deal with champions
    #deal with champs now stat wise
    

    for i in range(0,len(Team1_Champs)):
        print(Team1_Champs[i])
        print(Team2_Champs[i])
        team1_champ_stat = ld.retrieve_champ(champs_cursor,season,Team1_Champs[i])[0]
        team2_champ_stat = ld.retrieve_champ(champs_cursor,season,Team2_Champs[i])[0]
        #The important stats are kda, csPerMin,damagePerMin,goldPerMin,CsDiffAt15,xpDiffat15,GoldDiffAt15
        #these are indices 7,10,11,12,13,14,15

        entry.append(float(team1_champ_stat[7]) - float(team2_champ_stat[7]))

        entry.append(float(team1_champ_stat[10]) - float(team2_champ_stat[10]))

        entry.append(float(team1_champ_stat[11]) - float(team2_champ_stat[11]))

        entry.append(float(team1_champ_stat[12]) - float(team2_champ_stat[12]))

        entry.append(float(team1_champ_stat[13]) - float(team2_champ_stat[13]))

        entry.append(float(team1_champ_stat[14]) - float(team2_champ_stat[14]))

        entry.append(float(team1_champ_stat[15]) - float(team2_champ_stat[15]))

        champ_AVG1 = {
            'AVG_Winrate' : float(team1_champ_stat[6][:-1]),
            'AVG_KDA' : float(team1_champ_stat[7][:-1]),
            'AVG_CS/MIN' : float(team1_champ_stat[10][:-1]),
            'AVG_GOLD/MIN' : float(team1_champ_stat[12][:-1])
        }

        champ_AVG2 = {
            'AVG_Winrate' : float(team2_champ_stat[6][:-1]),
            'AVG_KDA' : float(team2_champ_stat[7][:-1]),
            'AVG_CS/MIN' : float(team2_champ_stat[10][:-1]),
            'AVG_GOLD/MIN' : float(team2_champ_stat[12][:-1])
        }

        team1_comfort = dsc.scrape_champ_comfort(Team1_Players[i],season,Team1_Champs[i],istop1)
        team2_comfort = dsc.scrape_champ_comfort(Team2_Players[i],season,Team2_Champs[i],istop1)

        difference = calculate_comfortability(team1_comfort,champ_AVG1,1) - calculate_comfortability(team2_comfort,champ_AVG2,1)
        entry.append(difference)


    #print(len(entry))
    assert(len(entry) == 95)
    print("Valid Entry: ", len(entry))
    return entry


tourney = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LPL%20Summer%20Season%202024/')






"""# Assuming 'model' is your neural network instance
for name, param in myModel.named_parameters():
    if param.requires_grad:
        print(name, param.data)"""

guesses = 0
total = 0
for series in tourney:
    champ_picks,result = dsc.scrape_picks2(series)
    players = dsc.scrape_teams_game()

    team1 = players[0]
    team2 = players[1]

    if len(team1) > 5 or len(team2) > 5:
        continue

    for x in champ_picks:
        team1_picks = champ_picks[x][0]
        team2_picks = champ_picks[x][1]

        outcome = result[x]

        data_values = setup(team1,team2,team1_picks,team2_picks,'S14')
        print("Length", ":", len(data_values))
        print(data_values)

        dataTensor = torch.tensor(data_values,dtype = torch.float32)
        dataTensor = dataTensor.unsqueeze(0)
        total += 1
        # Make prediction
        with torch.no_grad():  # Disable gradient computation for inference
            prediction = myModel(dataTensor)
            print(prediction)
            
            probabilities = F.softmax(prediction, dim=1)
            print(probabilities)
            prob = probabilities.numpy()[0]
            

            if (prob[0] > prob[1] and outcome[0] == 'WIN'):
                guesses+=1
            elif (prob[0] < prob[1] and outcome[1] == 'WIN'):
                guesses+=1
        print(guesses, ":", total)

print("TOTAL:",total)
print("GUESSES:",guesses)