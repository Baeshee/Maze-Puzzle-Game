import os
import sys
import itertools
import copy
import msvcrt

from colorama import init, Fore
import keyboard



init()

initial_print = False
key_pressed_down = False
key_pressed_up = False
key_pressed_left = False
key_pressed_right = False

maze_link = "mazes/test_maze-2.txt"

def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

def open_maze_file(file):
    maze_matrix = []

    with open("{}".format(file), "r") as maze_file:
        row = []
        
        for line in maze_file:
            for char in line.strip():
                row.append(char)
            
            maze_matrix.append(row)    
            row = []
            
    return maze_matrix

def get_maze_start_end(maze_matrix):
    for row in range(0, len(maze_matrix)):
        for col in range(0, len(maze_matrix[row])):
            if maze_matrix[row][col] == "S":
                start_pos = [row, col]
                cur_pos = copy.deepcopy(start_pos)
            elif maze_matrix[row][col] == "E":
                end_pos = [row, col] 
                
    return start_pos, cur_pos, end_pos

def create_movement_map(maze_matrix):
    move_dict = {}
    temp_moves_list = []
    
    for row in range(0, len(maze_matrix)):
        for col in range(0, len(maze_matrix[row])):
            if maze_matrix[row][col] == "S" or maze_matrix[row][col] == "O":
                if maze_matrix[row-1][col] == "x":
                    move_dict['up'] = True
                else:
                    move_dict['up'] = False
                    
                if maze_matrix[row+1][col] == "x":
                    move_dict['down'] = True
                else:
                    move_dict['down'] = False
                    
                if maze_matrix[row][col-2] == "x":
                    move_dict['left'] = True
                else:
                    move_dict['left'] = False
                    
                if maze_matrix[row][col+2] == "x":
                    move_dict['right'] = True
                else:
                    move_dict['right'] = False
            
            temp_moves_list.append(move_dict)
            move_dict = {}
    
    return temp_moves_list

def print_matrix(maze_matrix, difficulty, length):
    os.system('cls' if os.name =='nt' else 'clear')
    
    if difficulty == 0:
        for line in maze_matrix:
            print("".join(line), end="\n")
    elif difficulty == 1:
        x = 0
        for i in range(0, len(maze_matrix)):
            for j in range(0, len(maze_matrix[0])):
                if maze_matrix[i][j] == "|" or maze_matrix[i][j] == "-":
                    print(Fore.RED + f"{maze_matrix[i][j]}", end="")
                elif maze_matrix[i][j] == "P":
                    print(Fore.BLUE + f"{maze_matrix[i][j]}", end="")
                elif maze_matrix[i][j] == "E":
                    print(Fore.GREEN + f"{maze_matrix[i][j]}", end="")
                else:
                    print(Fore.WHITE + f"{maze_matrix[i][j]}", end="")
                
                x += 1
                if x == length:
                    print('\r')
                    x = 0
            
def handle_press_event(direction, value, maze_matrix, maze_moves, start_pos, cur_pos):
    if maze_moves[cur_pos[0]][cur_pos[1]][f"{direction}"] == True:
        if cur_pos[0] == start_pos[0] and cur_pos[1] == start_pos[1]:
            maze_matrix[cur_pos[0]][cur_pos[1]] = "S"
        else:
            maze_matrix[cur_pos[0]][cur_pos[1]] = "O"
            
        if direction == "up" or direction == "down":
            cur_pos[0] = cur_pos[0]+value
        elif direction == "left" or direction == "right":
            cur_pos[1] = cur_pos[1]+value  
            
        maze_matrix[cur_pos[0]][cur_pos[1]] = "P"

def handle_keyboard(maze_matrix, maze_moves, start_pos, cur_pos, difficulty, length):
    global key_pressed_up
    global key_pressed_left
    global key_pressed_down
    global key_pressed_right
    
    if keyboard.is_pressed("down") and key_pressed_down == False:
        if maze_moves[cur_pos[0]][cur_pos[1]]["down"] == True:
            handle_press_event("down", 2, maze_matrix, maze_moves, start_pos, cur_pos)
        
        print_matrix(maze_matrix, difficulty, length)
        key_pressed_down = True

    if keyboard.is_pressed("up") and key_pressed_up == False:
        if maze_moves[cur_pos[0]][cur_pos[1]]["up"] == True:
            handle_press_event("up", -2, maze_matrix, maze_moves, start_pos, cur_pos)
        
        print_matrix(maze_matrix, difficulty, length)
        key_pressed_up = True
        
    if keyboard.is_pressed("left") and key_pressed_left == False:
        if maze_moves[cur_pos[0]][cur_pos[1]]["left"] == True:
            handle_press_event("left", -4, maze_matrix, maze_moves, start_pos, cur_pos)
        
        print_matrix(maze_matrix, difficulty, length)
        key_pressed_left = True
        
    if keyboard.is_pressed("right") and key_pressed_right == False:
        if maze_moves[cur_pos[0]][cur_pos[1]]["right"] == True:
            handle_press_event("right", 4, maze_matrix, maze_moves, start_pos, cur_pos)
        
        print_matrix(maze_matrix, difficulty, length)
        key_pressed_right = True

def main():
    global initial_print
    global key_pressed_up
    global key_pressed_left
    global key_pressed_down
    global key_pressed_right
    
    difficulty = None
    
    maze_matrix = open_maze_file(maze_link)
    start_pos, cur_pos, end_pos = get_maze_start_end(maze_matrix);
    temp_moves_list = create_movement_map(maze_matrix)
    maze_moves = []
    
    length = len(maze_matrix[0])
    
    for group in grouper(length, temp_moves_list):
        maze_moves.append(group)
        
    while True:
        if difficulty == None:
            difficulty_input = input("Select the color for the maze (black - more difficult, color): ")
            if difficulty_input.lower() == "black":
                difficulty = 0
            elif difficulty_input.lower() == "color":
                difficulty = 1
        else:
            if initial_print == False:
                print_matrix(maze_matrix, difficulty, length)
                initial_print = True
            
            handle_keyboard(maze_matrix, maze_moves, start_pos, cur_pos, difficulty, length)
                
            if not keyboard.is_pressed("up"):
                key_pressed_up = False
                
            if not keyboard.is_pressed("left"):
                key_pressed_left = False
                
            if not keyboard.is_pressed("down"):
                key_pressed_down = False
                
            if not keyboard.is_pressed("right"):
                key_pressed_right = False
            
            if cur_pos == end_pos:
                print(Fore.WHITE + "You have solved the maze, congrats!")
                break
        
if __name__ == "__main__":
    main()
    sys.stdout.flush()
    while msvcrt.kbhit():
        msvcrt.getch()