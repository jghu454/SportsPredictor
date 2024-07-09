from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import LeagueDatabase as LD
import sqlite3
import time

player_stats = {
    'S14':'https://gol.gg/players/list/season-S14/split-ALL/tournament-ALL/',
    'S13':'https://gol.gg/players/list/season-S13/split-ALL/tournament-ALL/',
    'S12':'https://gol.gg/players/list/season-S12/split-ALL/tournament-ALL/',
    'S11':'https://gol.gg/players/list/season-S11/split-ALL/tournament-ALL/',
    'S10':'https://gol.gg/players/list/season-S10/split-ALL/tournament-ALL/',
    'S9' :'https://gol.gg/players/list/season-S9/split-ALL/tournament-ALL/',
}

champion_winrates = {

    'S13':'https://gol.gg/champion/list/season-S13/split-ALL/tournament-ALL/',
    'S12':'https://gol.gg/champion/list/season-S12/split-ALL/tournament-ALL/',
    'S11':'https://gol.gg/champion/list/season-S11/split-ALL/tournament-ALL/',
    'S10':'https://gol.gg/champion/list/season-S10/split-ALL/tournament-ALL/',
    'S9' :'https://gol.gg/champion/list/season-S9/split-ALL/tournament-ALL/',
}

team_stats = {
    'S13': 'https://gol.gg/teams/list/season-S13/split-ALL/tournament-ALL/',
    'S12': 'https://gol.gg/teams/list/season-S12/split-ALL/tournament-ALL/',
    'S11': 'https://gol.gg/teams/list/season-S11/split-ALL/tournament-ALL/',
    'S10': 'https://gol.gg/teams/list/season-S10/split-ALL/tournament-ALL/',
    'S9': 'https://gol.gg/teams/list/season-S9/split-ALL/tournament-ALL/'
}

synergy_stats = {
    'S14': 'https://gol.gg/premium/synergy/season-S14/split-ALL/tournament-ALL/',
    'S13': 'https://gol.gg/premium/synergy/season-S13/split-ALL/tournament-ALL/',
    'S12': 'https://gol.gg/premium/synergy/season-S12/split-ALL/tournament-ALL/',
    'S11': 'https://gol.gg/premium/synergy/season-S11/split-ALL/tournament-ALL/',
    'S10': 'https://gol.gg/premium/synergy/season-S10/split-ALL/tournament-ALL/',
    'S9': 'https://gol.gg/premium/synergy/season-S9/split-ALL/tournament-ALL/'
}


options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--window-size=3840,1080")

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service = service, options = options)

URL = "https://gol.gg/user/login/"


def login():
    driver.get("https://gol.gg/user/login/")
    #driver.maximize_window()
    #input user
    input = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/form/div[1]/div/input")
    input.send_keys("jafarakbar6969")


    #input password
    input = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/form/div[2]/div/input")
    input.send_keys("jewlover123")
    #print(input)

    #press login
    input = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/form/div[4]/button").click()




def scrape_champions():
    ChampionDatabase = sqlite3.connect('ChampionStats.db')
    cursor = ChampionDatabase.cursor()

    login()

    for season in champion_winrates:

        #get the top regions, no wildcard regions
        driver.get(champion_winrates[season])
        driver.find_element(By.XPATH, "//input[@id='leagues_top']").click()
        time.sleep(3)
        if ("display: none" in driver.find_element(By.XPATH, "//button[@id='btn_refresh']").get_attribute('style')):
            driver.find_element(By.XPATH, "//button[@id='btn_refresh']").click()
        time.sleep(5)


        LD.create_table(cursor, season, {
        'CHAMPION': 'TEXT',
        'PICKS': 'TEXT',
        'BANS': 'TEXT',
        'PRESENCE': 'TEXT',
        'WINS': 'TEXT',
        'LOSSES': 'TEXT',
        'WINRATE': 'TEXT',
        'KDA': 'TEXT',
        'AVG BT': 'TEXT',
        'GT': 'TEXT',
        'CSM': 'TEXT',
        'DPM': 'TEXT',
        'GPM': 'TEXT',
        'CSD15': 'TEXT',
        'GD15': 'TEXT',
        'XPD15': 'TEXT'
    })
        for x in range(1,167):

            myArray = []
            for y in range(1,17):
                if (x == 1 and (y == 1 or y == 2)):
                    string = driver.find_elements(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})")[5].text
                    myArray.append(string)
                    continue


                myArray.append(driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})").text)

            LD.insert_entry(cursor,season,myArray)
        ChampionDatabase.commit()


def scrape_teams():


    TeamDatabase = sqlite3.connect('TeamStats.db')
    cursor = TeamDatabase.cursor()
    

    login()
    data = {
    "`NAME`": "TEXT",       
    "`REGION`": "TEXT",
    "`GAMES`": "TEXT",
    "`WINRATE`": "TEXT",
    "`KDA`": "TEXT",
    "`GPM`": "TEXT",
    "`GDM`": "TEXT",
    "`GAMEDURATION`": "TEXT",
    "`KILLS_PER_GAME`": "TEXT",
    "`DEATHS_PER_GAME`": "TEXT",
    "`TOWERS_KILLED`": "TEXT",
    "`TOWERS_LOST`": "TEXT",
    "`FB`": "TEXT",
    "`FT`": "TEXT",
    "`DRAPG`": "TEXT",
    "`DRA`": "TEXT",
    "`VGPG`": "TEXT",
    "`HERPG`": "TEXT",
    "`HER`": "TEXT",
    "`DRA_AT_15`": "TEXT",
    "`TD_AT_15`": "TEXT",
    "`GD_AT_15`": "TEXT",
    "`PPG`": "TEXT",
    "`NASHPG`": "TEXT",
    "`NASH`": "TEXT",
    "`CSM`": "TEXT",
    "`DPM`": "TEXT",
}

    driver.get(team_stats['S13'])
    for season in team_stats:
        driver.get(team_stats[season])
        #print(cursor, ":", season, ":", data)
        LD.create_table(cursor,season,data)
        x = driver.find_elements(By.TAG_NAME, 'tr')
        x = x[4:]
        for i in x:
            y = driver.find_elements(By.TAG_NAME, 'td')
            


            row_text = i.text

            # Split the row text into individual columns
            
            team_names = row_text.split(season)[0:1]

            team_names[0] = team_names[0][:-1]
            team_statistics = row_text.split(season)[1].split()
            #print(team_names)
            #print(team_statistics)


            # Combine the first cell with the rest
            columns = team_names + team_statistics
            columns.pop()
            
            LD.insert_entry(cursor,season,columns)
            TeamDatabase.commit()
            
        
def scrape_players():

    data = {
    "PLAYER": "TEXT",
    "GAMES": "TEXT",
    "WIN_RATE": "TEXT",
    "KDA": "TEXT",
    "AVG_KILLS": "TEXT",
    "AVG_DEATHS": "TEXT",
    "AVG_ASSISTS": "TEXT",
    "CSM": "TEXT",
    "GPM": "TEXT",
    "KP": "TEXT",
    "DMG": "TEXT",
    "DPM": "TEXT",
    "VSPM": "TEXT",
    "AVG_WPM": "TEXT",
    "AVG_WCPM": "TEXT",
    "AVG_VWPM": "TEXT",
    "GD_AT_15": "TEXT",
    "CSD_AT_15":"TEXT",
    "XPD_AT_15": "TEXT",
    "FB": "TEXT",
    "FB_VICTIM": "TEXT",
    "PENTA_KILLS": "TEXT",
    "SOLO_KILLS": "TEXT"
}

    is_top = False
    

    PlayerDatabase = sqlite3.connect("PlayerStats.db")
    cursor = PlayerDatabase.cursor()
    
    for season in player_stats:
        #set it to top leagues
        driver.get(player_stats[season])
        if (not is_top):
            leagues = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div/form/div[3]/div[2]/table/tbody/tr/td[2]/span/div/div[1]/input')
            leagues.send_keys('IEM', Keys.ENTER)
            leagues.send_keys('LCK', Keys.ENTER)
            leagues.send_keys('LCS', Keys.ENTER)
            leagues.send_keys('LEC', Keys.ENTER)
            leagues.send_keys('LMS', Keys.ENTER)
            leagues.send_keys('LPL', Keys.ENTER)
            leagues.send_keys('MSC', Keys.ENTER)
            leagues.send_keys('MSI', Keys.ENTER)
            leagues.send_keys('WORLDS', Keys.ENTER)

            driver.find_element(By.XPATH,'/html/body/div/main/div/div/div[1]/div/form/div[3]/div[2]/table/tbody/tr/td[2]/div[4]/button').click()
            is_top = True
            
        
        LD.create_table(cursor,season,data)
        rows = driver.find_elements(By.TAG_NAME, 'tr')[5:]
        
        row_num = len(rows) 

        
        for x in range(1,row_num+1):
            player = []
            for y in range(1,25):
                if (y == 2):
                    continue
                z = driver.find_element(By.XPATH, f'''/html/body/div/main/div[2]/div/div[2]/div/table/tbody/tr[{x}]/td[{y}]''')
                player.append(z.text)
            LD.insert_entry(cursor,season,player)
            PlayerDatabase.commit()


def scrape_synergy():
    login()
    SynergyDatabase = sqlite3.connect("SynergyStats.db")
    cursor = SynergyDatabase.cursor()
    data = {
        "Champion1":"TEXT",
        "Role1" : "TEXT",
        "Champion2":"TEXT",
        "Role2" : "TEXT",
        "Games" :"TEXT",
        "Winrate" :"TEXT",
        "Gold_Diff15" : "TEXT",
        "CS_Diff15" : "TEXT"


    }
    
    is_top = False
    for seasons in synergy_stats:
        driver.get(synergy_stats[seasons ]) 

        LD.create_table(cursor,seasons,data)

        #set it to top leagues
        if (not is_top):
            leagues = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div/form/div[3]/div[1]/table/tbody/tr/td[2]/span/div/div[1]/input')
            leagues.send_keys('IEM', Keys.ENTER)
            leagues.send_keys('LCK', Keys.ENTER)
            leagues.send_keys('LCS', Keys.ENTER)
            leagues.send_keys('LEC', Keys.ENTER)
            leagues.send_keys('LMS', Keys.ENTER)
            leagues.send_keys('LPL', Keys.ENTER)
            leagues.send_keys('MSC', Keys.ENTER)
            leagues.send_keys('MSI', Keys.ENTER)
            leagues.send_keys('WORLDS', Keys.ENTER)

            driver.find_element(By.XPATH,'/html/body/div/main/div/div/div[1]/div/form/div[3]/div[1]/table/tbody/tr/td[2]/div[4]/button').click()
            is_top = True
            
        

        time.sleep(2)
        # Wait for the table to be present
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#result_tab table')))

        # Optionally, print the page source for debugging
    
        # Locate the rows of the table
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # Extract data from each row
        for row in rows:
            # Locate the cells in the row
            
            
            cells = row.find_elements(By.XPATH, './/td')
            row_data = []

            for cell in cells:
                roles = cell.find_elements(By.TAG_NAME, 'img')
                row_data.append(cell.text)
                for role in roles:
                    if (role.get_attribute('alt') is not None and role.get_attribute('alt') != ''):
                        row_data.append(role.get_attribute('alt'))

            
            LD.insert_entry(cursor,seasons,row_data)
            SynergyDatabase.commit()

def scrape_picks(link = "https://gol.gg/game/stats/59552/page-summary/"):
    
    driver.get(link)
    #opens website
    time.sleep(2)
    team_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'row pb-3')]")
    team_names = [x.text for x in team_names]
    rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'row pb-1')]")
    
    array_of_games = {}
    game_number = 1
    for i in rows:
        cols2 = i.find_elements(By.XPATH, ".//div[contains(@class, 'col-4 col-sm-5')]")
        
        array_of_games[game_number] = []
        for id in range(0, len(cols2)):
            i2 = cols2[id]
            champions = i2.find_elements(By.TAG_NAME, 'a')
            all_picks = []




            ##################################
            for champs in champions:
                picks= champs.find_element(By.TAG_NAME, 'img').get_attribute('src').split('/')
                #print(picks)
                x = [b for b in champs.find_element(By.TAG_NAME, 'img').get_attribute('src').split('/')[-1:]]
                ###############
                for v in range(0,len(x)):
                    x[v] = x[v].replace('.png', '')
                ###############
                all_picks.append(x[0])
            ####################################



            all_picks = all_picks[-5:]
            array_of_games[game_number].append(all_picks) 
            #print(all_picks)
        
        game_number = game_number + 1
    return array_of_games


def scrape_teams(link = "https://gol.gg/game/stats/59552/page-summary/"): 
    driver.get(link)
    time.sleep(2)
    teams = [[],[]]

    #give time
    

    teams_player = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-12 col-sm-6 pb-4')]")
    temp = []
    for i in teams_player:
        players = i.find_elements(By.TAG_NAME, 'a')
        
        for player in players:
            temp.append(player.text)
        
        

    teams[0] = temp[:-5]
    teams[1] = temp[-5:]
            
    return teams 
            
                





print(scrape_teams())
print(scrape_picks())
time.sleep(5)






