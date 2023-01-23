from colorama import init, Fore
import os

init()

# matrix = [
#     ["a","b","a","b","a"],
#     ["b","a","b","a","b"],
#     ["a","b","a","b","a"],
#     ["b","a","b","a","b"],
#     ["a","b","a","b","a"]
# ]

matrix = []

with open("{}".format("test_maze.txt"), "r") as maze_file:
    row = []
    
    for line in maze_file:
        for char in line.strip():
            row.append(char)
        
        matrix.append(row)    
        row = []
        
os.system('cls' if os.name =='nt' else 'clear')

x = 0
for i in range(0, len(matrix)):
    for j in range(0, len(matrix[0])):
        if matrix[i][j] == "|" or matrix[i][j] == "-":
            print(Fore.RED + f"{matrix[i][j]}", end="")
        else:
            print(Fore.WHITE + f"{matrix[i][j]}", end="")
        
        x += 1
        
        if x == 33:
            print('\r')
            x = 0