import sqlite3



# @param cursor - a cursor from the connection to the database
# @param table_name - the name of the table that will be created
# @param setup - a dictionary that will dictate the columns and their datatype 

"""Example of the setup Param

setup = {
    "Player_Name" : "TEXT",
    "Winrate" : "FLOAT",
    "TEAM" : "TEXT"
}
"""

def create_table(cursor, table_name, setup):

    format = ""
    for i in setup:
        format += i + " " + setup[i] + ", "

    format = format[0:len(format) - 2]


    print(format)
    
    cursor.execute(f'''CREATE TABLE {table_name} ({format}) ''')

#entry should be an array of values

def insert_entry(cursor, table_name, entry):
    #print(entry)
    #These instructions will combine the entries into code that will work for insertion into a sqlite database
    entry_tostring = ''

    for i in entry:
        if (str(type(i)) != "<class 'str'>"):
            entry_tostring += str(i) + ', '
        else:
            entry_tostring += '\'' + str(i) + '\', '


    entry_tostring = entry_tostring[0: len(entry_tostring) - 2] #cut off the last comma


    #Get the columns and combine the column names into code that will work for the insertion into database
    #connection_obj.execute( """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk2@gmail.com","Geek2",15)""") ---EXAMPLE
    cursor.execute("select * from %s where 1=0;" % table_name)
    columns = [ d[0] for d in cursor.description]

    column_names = ','.join(columns)

    #print(column_names)
    #print(entry[0], ":" , columns[0])
    #check for duplicates
    cursor.execute(f'''SELECT * FROM {table_name} WHERE {columns[0]} = '{entry[0]}' ''')

    
    if (cursor.fetchone()): #if duplicate update stats instead
        #print("Duplicate Player")
        pass
    else:
        #print(f'''INSERT INTO {table_name} ({column_names}) VALUES ({entry_tostring})''')
        cursor.execute(f'''INSERT INTO {table_name} ({column_names}) VALUES ({entry_tostring})''')
    
    

