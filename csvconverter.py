import csv

def csvconverter(array_of_arrays, dictionary, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the first smaller array
        writer.writerows(array_of_arrays[0])
        
        # Write an empty row to separate the sections
        writer.writerow([])
        
        # Write the second smaller array
        writer.writerows(array_of_arrays[1])
        
        # Write an empty row to separate the sections
        writer.writerow([])
        
        # Write the dictionary
        writer.writerow(["Key", "Value"])
        for key, value in dictionary.items():
            writer.writerow([key, value])

# Example usage:
players = [["player1","player2","player3","player4","player5"],["player1","player2","player3","player4","player5"]]

games = {

1: [["kaisa","jax","renekton","zac","yasuo"], ["zoe","kennen","malphite","rell","jinx"]],
2:  [["kaisa","jax","renekton","zac","yasuo"], ["zoe","kennen","malphite","rell","jinx"]],
3: [["kaisa","jax","renekton","zac","yasuo"], ["zoe","kennen","malphite","rell","jinx"]]
}

csvconverter(players, games, 'output.csv')