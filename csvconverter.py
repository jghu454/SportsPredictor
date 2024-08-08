import csv
import LeagueDatabase as ld
import sqlite3 
import Datascraper as dsc
from LeagueDataset import LeagueDataset
from torch.utils.data import DataLoader

#create sqlite cursors
connection = sqlite3.connect('ChampionStats.db')
connection2 = sqlite3.connect('PlayerStats.db')


champ_cursor = connection.cursor()
player_cursor = connection2.cursor()

player_format = {
    'top' : [1,2,3,4,5,6,7,8,9,10,11,16], #16-18 is 0 for lpl
    'jg' :  [1,2,3,4,5,6,7,8,9,10,11,16],
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
labels = [
    # Top
    'Top_Games_Difference', 'Top_Winrate_Difference', 'Top_KDA_Difference', 'Top_AVG_Kills_Difference',
    'Top_AVG_Deaths_Difference', 'Top_AVG_Assists_Difference', 'Top_CSM_Difference', 'Top_GPM_Difference',
    'Top_KP_Difference', 'Top_DMG%_Difference', 'Top_DPM_Difference', 'Top_GOLD_DIFF_15_Difference',

    
    # Jg
    'Jg_Games_Difference', 'Jg_Winrate_Difference', 'Jg_KDA_Difference', 'Jg_AVG_Kills_Difference',
    'Jg_AVG_Deaths_Difference', 'Jg_AVG_Assists_Difference', 'Jg_CSM_Difference', 'Jg_GPM_Difference',
    'Jg_KP_Difference', 'Jg_DMG%_Difference', 'Jg_DPM_Difference', 'Jg_GOLD_DIFF_15_Difference',
    
    # Mid
    'Mid_Games_Difference', 'Mid_Winrate_Difference', 'Mid_KDA_Difference', 'Mid_AVG_Kills_Difference',
    'Mid_AVG_Deaths_Difference', 'Mid_AVG_Assists_Difference', 'Mid_CSM_Difference', 'Mid_GPM_Difference',
    'Mid_KP_Difference', 'Mid_DMG%_Difference', 'Mid_DPM_Difference', 'Mid_GOLD_DIFF_15_Difference',
    
    
    # Adc
    'Adc_Games_Difference', 'Adc_Winrate_Difference', 'Adc_KDA_Difference', 'Adc_AVG_Kills_Difference',
    'Adc_AVG_Deaths_Difference', 'Adc_AVG_Assists_Difference', 'Adc_CSM_Difference', 'Adc_GPM_Difference',
    'Adc_KP_Difference', 'Adc_DMG%_Difference', 'Adc_DPM_Difference', 'Adc_GOLD_DIFF_15_Difference',
    
    
    # Support
    'Support_Games_Difference', 'Support_Winrate_Difference', 'Support_KDA_Difference', 'Support_AVG_Kills_Difference',
    'Support_AVG_Deaths_Difference', 'Support_AVG_Assists_Difference', 'Support_Vision_Per_Min_Difference',
]

champion_stat_labels = [
    # Top
    'Top_Champ_KDA_Difference', 'Top_Champ_CS_Per_Min_Difference', 'Top_Champ_Damage_Per_Min_Difference', 
    'Top_Champ_Gold_Per_Min_Difference', 'Top_Champ_CS_Diff_At_15_Difference', 'Top_Champ_XP_Diff_At_15_Difference',
    'Top_Champ_Gold_Diff_At_15_Difference', 'TopComfortabilityDifference',

    # Jg
    'Jg_Champ_KDA_Difference', 'Jg_Champ_CS_Per_Min_Difference', 'Jg_Champ_Damage_Per_Min_Difference', 
    'Jg_Champ_Gold_Per_Min_Difference', 'Jg_Champ_CS_Diff_At_15_Difference', 'Jg_Champ_XP_Diff_At_15_Difference',
    'Jg_Champ_Gold_Diff_At_15_Difference', 'JgComfortabilityDifference',

    # Mid
    'Mid_Champ_KDA_Difference', 'Mid_Champ_CS_Per_Min_Difference', 'Mid_Champ_Damage_Per_Min_Difference', 
    'Mid_Champ_Gold_Per_Min_Difference', 'Mid_Champ_CS_Diff_At_15_Difference', 'Mid_Champ_XP_Diff_At_15_Difference',
    'Mid_Champ_Gold_Diff_At_15_Difference', 'MidComfortabilityDifference',

    # Adc
    'Adc_Champ_KDA_Difference', 'Adc_Champ_CS_Per_Min_Difference', 'Adc_Champ_Damage_Per_Min_Difference', 
    'Adc_Champ_Gold_Per_Min_Difference', 'Adc_Champ_CS_Diff_At_15_Difference', 'Adc_Champ_XP_Diff_At_15_Difference',
    'Adc_Champ_Gold_Diff_At_15_Difference', 'AdcComfortabilityDifference',

    # Support
    'Support_Champ_KDA_Difference', 'Support_Champ_CS_Per_Min_Difference', 'Support_Champ_Damage_Per_Min_Difference', 
    'Support_Champ_Gold_Per_Min_Difference', 'Support_Champ_CS_Diff_At_15_Difference', 'Support_Champ_XP_Diff_At_15_Difference',
    'Support_Champ_Gold_Diff_At_15_Difference','SupportComfortabilityDiffernce',

    "GAME_RESULT"
]




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

def csvconverter(players, champs ,result, file, season,istop):
    writer = csv.writer(file)
    
    entry = []
    team1 = players[0]
    team2 = players[1]

    for i in range(0,len(team1)):
        #i is the position the player plays which correlates to a value in lane_format above
        
        lane = lane_format[i]
        for player_format_values in player_format[lane]: #this gets the player values in player_format according to their lane
            team1_player_stat = ld.retrieve_player(cursor=player_cursor,table_name=season,player=team1[i])[0][player_format_values]
            team2_player_stat = ld.retrieve_player(cursor=player_cursor,table_name=season,player=team2[i])[0][player_format_values]

            if '%' in team1_player_stat:
                team1_player_stat = team1_player_stat[:-1]
                team2_player_stat = team2_player_stat[:-1]


            if '-' == team1_player_stat: ##this is mainly because lpl does not track cs per min for god knows why and we may remove this stat later
                team1_player_stat = 0
                team2_player_stat = 0

            team1_player_stat = float(team1_player_stat)
            team2_player_stat = float(team2_player_stat)

            difference = team1_player_stat - team2_player_stat
            entry.append(difference)#appending each player stat from the format
            
            #print("Team1 Player is: ", team1[i], "|| Team2 Player is: ", team2[i], "|| Their stats are =", team1_player_stat, ":", team2_player_stat, "and the difference = ", difference)


    #deal with champs now stat wise
    print("AFTER PLAYERS: ", id)
    team1_champs = champs[0]
    team2_champs = champs[1]

    for i in range(0,len(team1_champs)):
        team1_champ_stat = ld.retrieve_champ(champ_cursor,season,team1_champs[i])[0]
        team2_champ_stat = ld.retrieve_champ(champ_cursor,season,team2_champs[i])[0]
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

        print(team1[i] , ":", team2[i])
        print(team1_champs[i], ":", team2_champs[i])
        player_comfort_scrape1 = dsc.scrape_champ_comfort(team1[i],season,team1_champs[i],istop)
        player_comfort_scrape2 = dsc.scrape_champ_comfort(team2[i],season,team2_champs[i],istop)

        

        player1_comfort = calculate_comfortability(player_comfort_scrape1,champ_AVG1)
        player2_comfort = calculate_comfortability(player_comfort_scrape2,champ_AVG2)
        
        player_comfort_difference = player1_comfort - player2_comfort

        entry.append(player_comfort_difference)
        
    
    entry.append(int(result[1] == "WIN"))
    writer.writerow(entry)








dictionary_games = {
    'S14' : [],
    'S13' : [],
    'S12' : [],
    'S11' : [],
}


#dictionary_games['S14'] = dictionary_games["S14"] + dsc.scrape_links_games()
#dictionary_games['S13'] = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202023/')
dictionary_games['S12'] = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/')
dictionary_games['S11'] = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%202024/')






with open('Summer24_LPL_Placements.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(labels + champion_stat_labels)
    istop = [False]
    
    for season in dictionary_games:
        for games in dictionary_games[season]:
            players = dsc.scrape_teams_game(games)
            champs,game_result = dsc.scrape_picks(games)
            print(game_result[1])
            if (len(players[0]) > 5 or len(players[1]) > 5):
                continue

            csvconverter(players,champs[1],game_result[1],file,season,istop)

