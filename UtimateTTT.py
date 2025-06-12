#This is a program where you can play tic tac toe using your mouse.


#Imports and creating tkinter setup
from tkinter import *
import random
import math

root = Tk()

screen = Canvas(root, width = 400, height = 400, bg = "white")
screen.pack()

#Callback function for the mouse that houses all the computation
def place(event):
    global whose_turn,board,winner,turn_count,ranks,abs_winner,xgamex,xgamey,ogamey,ogamex
    num_games = 0
    #Checks if the game is over.
    #If so, prevents any more pieces from being placed and displays the game result.
    for layer in big_board:
        for piece in layer:
            if not piece == 0:
                num_games += 1
    if abs_winner:
        if whose_turn == 0:
            print("Game is over, Match result: Blue Victory")
        else:
            print("Game is over, Match result: Red Victory")
    elif num_games == 9:
        print("Game is over, Match result: Cat's Game")
        
    else:
        #using truncation to turn mouse x and y (event.x/y) into ints.
        #These ints are then the indexs used to find 
        #what piece the user clicked in the game given by gamex and gamey
        x = math.floor(event.x/(400/ranks))
        y = math.floor(event.y/(400/ranks))
        gamex = math.floor(x/3)
        gamey = math.floor(y/3)
        go = False
        legal = False
        while x > 2:
            x -= 3
        while y > 2:
            y -= 3
        
        #determines if the game the user in attemping to play in is correct.
        #If not, the function stops and prints what board the user should play in
        if (whose_turn == 0 and (not xgamex == -1)) or (whose_turn == 1 and (not ogamex == -1)):
            if whose_turn == 0:
                if xgamex == gamex and xgamey == gamey:
                    legal = True
                else:
                    print("That's the wrong game, you must play in the "+get_game(xgamey,xgamex)+" game")
            else:
                if ogamex == gamex and ogamey == gamey:
                    legal = True
                else:
                    print("That's the wrong game, you must play in the "+get_game(ogamey,ogamex)+" game")
        else:
            legal = True
        if legal:
            legal_move = False
            #finds if the place you are playing is already won or if there is already a peice there
            if not board[gamey][gamex][y][x] == 0: 
                print("This square is taken")
            elif not big_board[gamey][gamex] == 0:
                print("This game is finished, play somewhere else")
                
                
            #This places the correct tile color on the list the represents the board
            #It also changes the turn and increases the total amount of pieces placed to determine a draw
            #It also assigns the x and y of the game to these vars
            #to find what game the user must play in. determined above starting on line 45.
            elif whose_turn == 0:
                board[gamey][gamex][y][x] = 1
                whose_turn = 1
                turn_count += 1
                legal_move = True
            else:
                board[gamey][gamex][y][x] = 2
                whose_turn = 0
                turn_count += 1
                legal_move = True
            
            
            #Checks if there are 3 Xs or Os in a row
            #if so it declares winner of the game at that index.
            #this information in then given to the refresh function 
            if legal_move:
                for i,layer_game in enumerate(board):
                    for j, game in enumerate(layer_game):
                        num_pieces = 0
                        for k, layer in enumerate(game):
                            #These lines deal with if there is a three in a row in a horizontal line
                            if layer.count(1) == ranks/3:
                                if big_board[i][j] == 0:
                                    winner = "X"+str(i)+str(j)
                                    go = True
                                    break
                            elif layer.count(2) == ranks/3:
                                if big_board[i][j] == 0:
                                    winner = "O"+str(i)+str(j)
                                    go = True
                                    break
                            for space in layer:
                                if not space == 0:
                                    num_pieces += 1
                        if num_pieces == 9:
                            if big_board[i][j] == 0:
                                winner = "="+str(i)+str(j)
                                go = True
                        #This uses a flag to see if a winner has already been declared
                        if not go:
                            #This code checks if a game in one with a vertical line
                            for o in range(3):
                                xs = 0
                                os = 0
                                for p in range(3):
                                    piece = game[p][o]
                                    if piece == 2:
                                        os += 1
                                    elif piece == 1:
                                        xs += 1
                                    else:
                                        break
                                    if os == 3:
                                        if big_board[i][j] == 0:
                                            winner = "O"+str(i)+str(j)
                                            go = True
                                    elif xs == 3:
                                        if big_board[i][j] == 0:
                                            winner = "X"+str(i)+str(j)
                                            go = True
                        
                        if not go:
                            #This code checks the diagonals for the game in the correct for loop
                            offset = 0
                            turn = -1
                            for o in range(3):
                                xs = 0
                                os = 0
                                for p in range(3):
                                    piece = game[p][offset-p*turn]
                                    if piece == 2:
                                        os += 1
                                    elif piece == 1:
                                        xs += 1
                                    else:
                                        break
                                    if os == 3:
                                        if big_board[i][j] == 0:
                                            winner = "O"+str(i)+str(j)
                                            go = True
                                    elif xs == 3:
                                        if big_board[i][j] == 0:
                                            winner = "X"+str(i)+str(j)
                                            go = True
                                offset = int(ranks/3-1)
                                turn = 1
                
                #Calls function that changes the visual board(explained there)
                refresh_board(winner)
                if whose_turn == 1:
                    if not big_board[y][x] == 0:
                        ogamex = -1
                        ogamey = -1
                    else:
                        ogamex = x
                        ogamey = y
                else:
                    if not big_board[y][x] == 0:
                        xgamex = -1
                        xgamey = -1
                    else:
                        xgamex = x
                        xgamey = y
#This is the function that updates the visual board
def refresh_board(winner):
    global object_board,dif,board,big_board,abs_winner
    for i,game_layer in enumerate(board):
        for j,game in enumerate(game_layer):
            for k, layer in enumerate(game):
                for l,piece in enumerate(layer):
                    if piece == 1:
                        if screen.itemcget(object_board[i][j][k][l],"text") == " ":
                            screen.itemconfig(object_board[i][j][k][l], text = "X",fill = "green")
                        else:
                            screen.itemconfig(object_board[i][j][k][l], text = "X",fill = "red")
                    elif piece == 2:
                        if screen.itemcget(object_board[i][j][k][l],"text") == " ":
                            screen.itemconfig(object_board[i][j][k][l], text = "O", fill = "green")
                        else:
                            screen.itemconfig(object_board[i][j][k][l], text = "O", fill = "blue")
    #This code checks the larger board and sees if there is a abs_winner
    if not winner == 0:
        #This creates the object that goes over the game that is won.
        screen.create_text(dif*3/2+dif*3*int(winner[2]),dif*3/2+dif*3*int(winner[1]),text=winner[0],font=("Arial",int(1000/ranks)),fill=get_fill(winner[0]))
        #This updates the list of the larger board so the following code can evaluate it
        big_board[int(winner[1])][int(winner[2])] = winner[0]
        #This code is almost completely identical to the code that check every game
        #It's a bit simpler since the list is smaller and there has to be less checks
        winner = 0
        go = True
        
        for layer in big_board:
            if layer.count("X") == 3:
                abs_winner = True
                go = False
                break
            elif layer.count("O") == 3:
                abs_winner = True
                go = False
                break
        if go:
            for i in range(3):
                xs = 0
                os = 0
                for j in range(3):
                    piece = big_board[j][i]
                    if piece == "X":
                        xs += 1
                    elif piece == "O":
                        os += 1
                    else:
                        break
                    if os == 3 or xs == 3:
                        abs_winner = True
                        go = False
                        break
        if go:
            offset = 0
            turn = -1
            for o in range(3):
                xs = 0
                os = 0
                for p in range(3):
                    piece = big_board[p][offset-p*turn]
                    if piece == "O":
                        os += 1
                    elif piece == "X":
                        xs += 1
                    else:
                        break
                    if os == 3 or xs == 3:
                        abs_winner = True
                        break
                offset = int(ranks/3-1)
                turn = 1
            
    screen.update()

#This function turns part of the winner var into the color 
#that is used to create the big letter over a won game
def get_fill(letter):
    if letter == "X":
        return "red"
    elif letter == "O":
        return "blue"
    else:
        return "gray"

#This function turns the gamex and gamey from the callback function into 
#a string of what board they need to play in.
def get_game(y,x):
    if y == 0:
        yspace = "top"
    elif y == 1:
        yspace = "middle"
    else:
        yspace = "bottom"
    if x == 0:
        xspace = "left"
    elif x == 1:
        xspace = "center"
    else:
        xspace = "right"
        
    return yspace+" "+xspace
    
#Creating all of the varibles for the program
object_board = []
#Representaion of the board, 2d list with 0 being emtpy, 1 being X, and 2 being O
board = []

whose_turn = 0
winner = 0
turn_count = 0
ranks = 9
dif = 400/ranks
width = 30/ranks
abs_winner = False
xgamex = -1
xgamey = -1
ogamex = -1
ogamey = -1

#Creates the "visual board" that houses the text objects
#They start as invisible spaces that can be changed to X or O


for i in range(int(ranks/3)):
    board.append([])
    object_board.append([])
    for j in range(int(ranks/3)):
        board[i].append([])
        object_board[i].append([])
        for k in range(3):
            board[i][j].append([])
            object_board[i][j].append([])
            for l in range(3):
                board[i][j][k].append(0)
                object_board[i][j][k].append(screen.create_text(dif/2+dif*l+dif*3*j,dif/2+dif*k+dif*3*i,text=" ",font = ("Arial",int(200/ranks))))
big_board = []
for i in range(int(ranks/3)):
    big_board.append([])
    for j in range(int(ranks/3)):
        big_board[i].append(0)
                    
#Making the lines that makeup the Board
for i in range(ranks-1):
    if ranks%3 == 0:
        if (i+1)%3 == 0:
            width = 60/ranks
    screen.create_line(dif*(i+1),0,dif*(i+1),400,width = width)
    screen.create_line(0,dif*(i+1),400,dif*(i+1),width = width)
    width = 30/ranks

#Binds left clicking the mouse to the function "place", giving the function the x and y of the mouse as parameters
screen.bind("<Button-1>",place)

root.mainloop()