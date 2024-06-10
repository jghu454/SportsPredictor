from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


import LeagueDatabase as LD
import sqlite3

options = Options()
options.add_argument('--ignore-certificate-errors')

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)


URL = "https://gol.gg/user/login/"

driver.get(URL)

#input user
input = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/form/div[1]/div/input")
input.send_keys("jafarakbar6969")


#input password
input = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/form/div[2]/div/input")
input.send_keys("jewlover123")
#print(input)

#press login
input = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/form/div[4]/button").click()



#champion stats
driver.get("https://gol.gg/champion/list/season-S13/split-ALL/tournament-ALL/")
driver.find_element(By.XPATH, "//input[@id='leagues_top']").click()
time.sleep(3)
driver.find_element(By.XPATH, "//button[@id='btn_refresh']").click()
driver.maximize_window()



#wait = WebDriverWait(driver, 40)  # Wait up to 10 seconds

# Wait for the table to be present in the DOM

stat = driver.find_elements(By.XPATH, "//table/tbody/tr")
#input = driver.find_element(By.CLASS_NAME, "table_list playerslist tablesaw trhover tablesaw-swipe tablesaw-sortable")





for x in range(1,167):
    #print("-------")

    for y in range(1,16):
        if (x == 1 and (y == 1 or y == 2)):
            #print(driver.find_elements(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})")[5].text)
            continue

        #print(driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})").text)

#champ = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(167) td:nth-child(1)").text

#print(driver.page_source)


ChampionDatabase = sqlite3.connect('ChampionStats.db')
cursor = ChampionDatabase.cursor()


LD.create_table(cursor, "s13", {
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
    #print("-------")
    myArray = []
    for y in range(1,17):
        if (x == 1 and (y == 1 or y == 2)):
            string = driver.find_elements(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})")[5].text
            myArray.append(string)
            continue

        #print(driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})").text)
        myArray.append(driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({x}) td:nth-child({y})").text)
    print(myArray)
    LD.insert_entry(cursor,"s13",myArray)


ChampionDatabase.commit()
time.sleep(5)

ChampionDatabase.close()


time.sleep(10)
driver.quit()

