import sqlite3
import LeagueDatabase as ld

connect = sqlite3.Connection("PlayerStats.db")
cursor = connect.cursor()
ld.insert_entry(cursor, "S14", ['Duro', '23', '56.5%', '3.3', '0.6', '2.7', '8.2', '1.6', '256', '65.1%', '5.9', '140', '3.55', '1.92', '0.43', '0.55', '-38', '6', '58', '17.4%', '26.1%', '0', '1'])

