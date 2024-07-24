import csv
import LeagueDatabase as ld
import sqlite3 
import Datascraper as dsc
from LeagueDataset import LeagueDataset
from torch.utils.data import DataLoader


# Example usage:
label = [
    # Team 1 Stats
    "Top1_Games",
    "Top1_Winrate",
    "Top1_KDA",
    "Top1_AVG Kills",
    "Top1_AVG Deaths",
    "Top1_AVG Assists",
    "Top1_CSM",
    "Top1_GPM",
    "Top1_KP",
    "Top1_DMG%",
    "Top1_DPM",
    "Top1_GOLD_DIFF_15",
    "Top1_CS_DIFF_15",
    "Top1_XP_DIFF_15",
    "Top1_Champ_Presence",
    "Top1_Champ_Winrate",
    
    "Jg1_Games",
    "Jg1_Winrate",
    "Jg1_KDA",
    "Jg1_AVG Kills",
    "Jg1_AVG Deaths",
    "Jg1_AVG Assists",
    "Jg1_CSM",
    "Jg1_GPM",
    "Jg1_KP",
    "Jg1_DMG%",
    "Jg1_DPM",
    "Jg1_Champ_Presence",
    "Jg1_Champ_Winrate",
    
    "Mid1_Games",
    "Mid1_Winrate",
    "Mid1_KDA",
    "Mid1_AVG Kills",
    "Mid1_AVG Deaths",
    "Mid1_AVG Assists",
    "Mid1_CSM",
    "Mid1_GPM",
    "Mid1_KP",
    "Mid1_DMG%",
    "Mid1_DPM",
    "Mid1_GOLD_DIFF_15",
    "Mid1_CS_DIFF_15",
    "Mid1_XP_DIFF_15",
    "Mid1_Champ_Presence",
    "Mid1_Champ_Winrate",
    
    "Adc1_Games",
    "Adc1_Winrate",
    "Adc1_KDA",
    "Adc1_AVG Kills",
    "Adc1_AVG Deaths",
    "Adc1_AVG Assists",
    "Adc1_CSM",
    "Adc1_GPM",
    "Adc1_KP",
    "Adc1_DMG%",
    "Adc1_DPM",
    "Adc1_GOLD_DIFF_15",
    "Adc1_CS_DIFF_15",
    "Adc1_XP_DIFF_15",
    "Adc1_Champ_Presence",
    "Adc1_Champ_Winrate",
    
    "Support1_Games",
    "Support1_Winrate",
    "Support1_KDA",
    "Support1_AVG Kills",
    "Support1_AVG Deaths",
    "Support1_AVG Assists",
    "Support1_Vision_Per_Min",
    "Support1_Champ_Presence",
    "Support1_Champ_Winrate",
    
    
    # Team 2 Stats
    "Top2_Games",
    "Top2_Winrate",
    "Top2_KDA",
    "Top2_AVG Kills",
    "Top2_AVG Deaths",
    "Top2_AVG Assists",
    "Top2_CSM",
    "Top2_GPM",
    "Top2_KP",
    "Top2_DMG%",
    "Top2_DPM",
    "Top2_GOLD_DIFF_15",
    "Top2_CS_DIFF_15",
    "Top2_XP_DIFF_15",
    "Top2_Champ_Presence",
    "Top2_Champ_Winrate",
    
    "Jg2_Games",
    "Jg2_Winrate",
    "Jg2_KDA",
    "Jg2_AVG Kills",
    "Jg2_AVG Deaths",
    "Jg2_AVG Assists",
    "Jg2_CSM",
    "Jg2_GPM",
    "Jg2_KP",
    "Jg2_DMG%",
    "Jg2_DPM",
    "Jg2_Champ_Presence",
    "Jg2_Champ_Winrate",
    
    "Mid2_Games",
    "Mid2_Winrate",
    "Mid2_KDA",
    "Mid2_AVG Kills",
    "Mid2_AVG Deaths",
    "Mid2_AVG Assists",
    "Mid2_CSM",
    "Mid2_GPM",
    "Mid2_KP",
    "Mid2_DMG%",
    "Mid2_DPM",
    "Mid2_GOLD_DIFF_15",
    "Mid2_CS_DIFF_15",
    "Mid2_XP_DIFF_15",
    "Mid2_Champ_Presence",
    "Mid2_Champ_Winrate",
    
    "Adc2_Games",
    "Adc2_Winrate",
    "Adc2_KDA",
    "Adc2_AVG Kills",
    "Adc2_AVG Deaths",
    "Adc2_AVG Assists",
    "Adc2_CSM",
    "Adc2_GPM",
    "Adc2_KP",
    "Adc2_DMG%",
    "Adc2_DPM",
    "Adc2_GOLD_DIFF_15",
    "Adc2_CS_DIFF_15",
    "Adc2_XP_DIFF_15",
    "Adc2_Champ_Presence",
    "Adc2_Champ_Winrate",
    
    "Support2_Games",
    "Support2_Winrate",
    "Support2_KDA",
    "Support2_AVG Kills",
    "Support2_AVG Deaths",
    "Support2_AVG Assists",
    "Support2_Vision_Per_Min",
    "Support2_Champ_Presence",
    "Support2_Champ_Winrate",
    "WinningTeam" #will either be 0 or 1 for team 1 or 0

]
#csvconverter(label, games, 'output.csv')
player_format = {
    'top' : [1,2,3,4,5,6,7,8,9,10,11,16,17,18],
    'jg' : [1,2,3,4,5,6,7,8,9,10,11],
    'mid' : [1,2,3,4,5,6,7,8,9,10,11,16,17,18],
    'adc' : [1,2,3,4,5,6,7,8,9,10,11,16,17,18],
    'sup' : [1,2,3,4,5,6,12]

}

lane_format = {
    0 : 'top',
    1 : 'jg',
    2 : 'mid',
    3 : 'adc',
    4 : 'sup'

}

def csvconverter(players, games,results, file, season):
    #games will be a dictionary of champions
    connection = sqlite3.connect('PlayerStats.db')
    cursor = connection.cursor()
    team1_player_stats_base = {
        'top' : [],
        'jg' : [],
        'mid' : [],
        'adc' : [],
        'sup' : []
    } #just use to hold all the stats of every single player first
    team1 = players[0] #name of all players in team1
    id = 0
    #get values for team
    for i in team1_player_stats_base:
        #get role 
        role = lane_format[id] #top jg mid adc or sup depends on index

        #now using said role , we will get the player's stats in a tuple
        player_stats_tuple = ld.retrieve_player(cursor, season, team1[id])
        
        #player_format[role] tells us all indices where the important information is for said role
        for index in player_format[role]:
            
            if (player_stats_tuple[0][index] != '-'):
                print(player_stats_tuple[0][index], ":", '%' not in player_stats_tuple[0][index], ";", player_stats_tuple[0][index][:-1])
                if '%' not in player_stats_tuple[0][index]:
                    team1_player_stats_base[role].append(player_stats_tuple[0][index]) 
                else:
                    team1_player_stats_base[role].append(player_stats_tuple[0][index][:-1])
            
            else:
                team1_player_stats_base[role].append(0)


        id += 1 #index to the next player after getting all data



    team2_player_stats_base = {
        'top' : [],
        'jg' : [],
        'mid' : [],
        'adc' : [],
        'sup' : []
    }
    team2 = players[1]
    id = 0
    #get values for team
    for i in team2_player_stats_base:
        #get role 
        role = lane_format[id] #top jg mid adc or sup depends on index

        #now using said role , we will get the player's stats in a tuple
        player_stats_tuple = ld.retrieve_player(cursor, season, team2[id])
        
        #player_format[role] tells us all indices where the important information is for said role
        for index in player_format[role]:

            if (player_stats_tuple[0][index] != '-'):
                if '%' not in player_stats_tuple[0][index]:
                    team2_player_stats_base[role].append(player_stats_tuple[0][index]) 
                else:
                    team2_player_stats_base[role].append(player_stats_tuple[0][index][:-1])
            
            else:
                team2_player_stats_base[role].append(0) 


        id += 1 #index to the next player after getting all data

    
    connection = sqlite3.connect('ChampionStats.db')
    cursor = connection.cursor()
    

    

    
    writer = csv.writer(file)
    result_id = 1
    for i in games:
        picks = games[i] #this gets the array of champion picks
        team1_picks = picks[0]
        team2_picks = picks[1]


        print(team1_picks)
        print(team2_picks)

        entire_line = []
        id = 0
        for champs in team1_picks:
            x = ld.retrieve_champ(cursor,season,champs)
            role = lane_format[id] #this gets role


            
            entire_line = entire_line + team1_player_stats_base[role] #adds laner stats + champion stats

            #print('%' in x[0][3], ":", x[0][3], ":", x[0][3][:-1])
            #print('%' in x[0][6], ":", x[0][6], ":", x[0][6][:-1])

            entire_line.append(x[0][3][:-1])
            entire_line.append(x[0][6][:-1])

            
            id += 1
            #3 and 6 are presence and WR

        id = 0
        for champs in team2_picks:
            x = ld.retrieve_champ(cursor,season,champs)
            role = lane_format[id] #this gets role

            

            entire_line = entire_line + team2_player_stats_base[role]
            #print('%' in x[0][3], ":", x[0][3], ":", x[0][3][:-1])
            #print('%' in x[0][6], ":", x[0][6], ":", x[0][6][:-1])

            entire_line.append(x[0][3][:-1])
            entire_line.append(x[0][6][:-1])

            
            id += 1
            #3 and 6 are presence and WR
        
        
        entire_line = entire_line + [int(results[result_id][1] == "WIN")]
        result_id += 1
        writer.writerow(entire_line)
        print(len(entire_line))


dictionary_games = {
    'S14' : [],
    'S13' : [],
    'S12' : [],
    'S11' : [],
    'S10' : []



}


dictionary_games['S14'] = dictionary_games["S14"] + dsc.scrape_links_games()
dictionary_games['S13'] = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202023/')
dictionary_games['S12'] = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/')
dictionary_games['S11'] = dsc.scrape_links_games('https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%202024/')

with open('Summer24_LPL_Placements.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(label)

    for season in dictionary_games:
        for games in dictionary_games[season]:
            plrs = dsc.scrape_teams_game(games)

            gmes,res = dsc.scrape_picks(games)
            csvconverter(plrs,gmes,res,file,season)


    """for games in LPL_SUMMER_links:
        plrs = dsc.scrape_teams_game(games)

        gmes,res = dsc.scrape_picks(games)
        csvconverter(plrs,gmes,res,file,'S14')
"""

    