#Hangman in Python using a Tkinter GUI
#Made by AJ

#Notations:

#Start of a process: ---
#Continuation of the process: ^
#One line instruction: <<

#Modules

from tkinter import *
import random
import time

#Variables
words = []

try: # Get words from a textfile called WordList.txt
    with open("WordList.txt", "r") as wordlistfile:
        for line in wordlistfile.readlines():
            words.append(line[:-1])
    print(words)
except: # If the text file does not exist then default words are selected
    words = ["Hello", "Word", "House", "Orange", "Fruit"]
    print("File was unreadable")

current_word = ""
starting_lives = 6
guessed_letters = ""
legalcharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
tempstr = ""
lives = [starting_lives, 0] #Starting lives , Fraction of "lives remaining/starting lives"
results = [0, 0] #Wins/Losses
backcolour = "white" #Colour of the programs background
userinputobjectcolour = "beige" #Colour of the user interactive objects

#Functions

def reveal(): #Displays the unlocked letters of the word from trial and error
    global tempstr
    tempstr = ""
    for x in range(0, len(current_word)):
        flag = False
        for z in range(0, len(guessed_letters)):
            if current_word[x].upper() == guessed_letters[z].upper():
                flag = True
        if flag == True:
            tempstr += current_word[x]
        else:
            tempstr += "*"
    if tempstr.lower() == current_word.lower():
        setup(1)
    else:
        wordlbl.config(text = tempstr)
        wordlbl.place(x = int(113 - len(current_word) * (12/5)))

def attempt(): #Runs through a single attempt :: Only uses the first letter given in the guess box
    global guessed_letters, lives
    if lives[0] != 0 and attemptent.get() != "" and legalcharacters.count(attemptent.get()) != 0: #Checks if the user can still play
        flag = False #Declares a flag variable <<
        for x in range(len(guessed_letters)): #Checks if letter has already been used ---
            if guessed_letters[x].upper() == attemptent.get()[0].upper():#^
                flag = True #^
                print("Already guessed that letter!") #^
                attemptent.delete(0, END) #Clears the entry box <<
                return #^
        if flag == False: #^
            guessed_letters += attemptent.get()[0].lower() #Adds letter to guessed letters if it hasnt already been guessed ^
            lblstr = guesseslbl.cget("text") + attemptent.get()[0].upper() + ", "
            lblnum = lblstr.count(",")
            if lblnum % 9 == 0:
                lblstr += "\n"
            if lblnum <= 9:
                guesseslbl.place(x = int(308 - (lblnum * 6)))
            guesseslbl.config(text = lblstr)
        for x in range(0, len(current_word)): #Checks if the guessed letter is in the chosen word ---
            if attemptent.get()[0].upper() == current_word[x].upper(): #^
                flag = True #^
        attemptent.delete(0, END) #Clears the entry box <<
        if flag == True: #Updates the keyword if a correct letter is guessed ---
            reveal() #^
        else: #If an incorrect letter was guessed then a life is lost ---
            lives[0] -= 1 #^
            liveslbl.config(text = str("Current lives: " + str(lives[0])))#^
            if lives[0] == 0: #If player is now dead then it tells the game to reset ---
                lives = [lives[0], lives[0]/starting_lives] #Lives list is updated <<
                animation_update()
                setup(2)
                return #Exits the function <<
            reveal() #Displays keyword to go with updated lives status ---
        lives = [lives[0], lives[0]/starting_lives] #Lives list is updated <<
        animation_update()
    elif lives[0] == 0: #If person is dead then it skips all above and returns ---
        return
    else: #Or else if nothing was input into the box (or an invalid character) but the user is alive it asks for input ---
        print("Please input a valid guess!") #^
        attemptent.delete(0, END) #Clears the entry box <<

def setup(win = 3): #Sets up a new game
    global current_word, starting_lives, lives, guessed_letters, results
    if win == 3: #If game is reset ---
        results = [0, 0] #Reset wins and losses ^
    elif win == 2: #If game was lost ---
        results[1] += 1 #Add 1 to losses ^
    else: #If game was won ---
        results[0] += 1 #Add 1 to wins ^
    winslbl.config(text = "Wins: " + str(results[0]))
    losseslbl.config(text = "Losses: " + str(results[1]))
    wordlbl.config(text = "")
    guessed_letters = "" #Reset guessed letters
    lives = [starting_lives, 0, 0] #Starting lives , Lives left %, Level of death from 0 to 6 (6 = death)
    current_word = words[random.randint(0, len(words) - 1)]
    guesseslbl.config(text = "")
    liveslbl.config(text = str("Current lives: " + str(lives[0])))
    canvas.delete("all")
    canvas.create_line(35, 270, 195, 270)
    canvas.create_line(35, 270, 35, 75)
    canvas.create_line(35, 75, 125, 75)
    canvas.create_line(35, 145, 95, 75)
    canvas.create_line(125, 75, 125, 105)
    guesstitlelbl.config(text = "Guesses:")
    reveal()

def animation_update():
    if lives[1] == 0:
        guesstitlelbl.config(text = "Dead...")
        for x in range(22):
            time.sleep(0.15)
            canvas.delete("all")
            canvas.create_line(35, 270, 195, 270)
            canvas.create_line(35, 270, 35, 75)
            canvas.create_line(35, 75, 125, 75)
            canvas.create_line(35, 145, 95, 75)
            canvas.create_line(125, 75, 125, 105)
            canvas.create_oval(145 - x, 105, 105 + x, 145)
            canvas.create_line(125, 145, 125, 210)
            canvas.create_line(125, 145, 162.5 - x, 170)
            canvas.create_line(125, 145, 87.5 + x, 170)
            canvas.create_line(125, 210, 150 - x, 252.5)
            canvas.create_line(125, 210, 100 + x, 252.5)
            game.update()
    if lives[1] <= 1/6:
        canvas.create_line(125, 210, 150, 252.5)
    if lives[1] <= 2/6:
        canvas.create_line(125, 145, 87.5, 170)
    if lives[1] <= 3/6:
        canvas.create_line(125, 145, 162.5, 170)
    if lives[1] <= 4/6:
        canvas.create_line(125, 145, 125, 210)
    if lives[1] <= 5/6:
        canvas.create_oval(145, 105, 105, 145)
    game.update()

#GUI :: Setting up the graphical user interface

game = Tk()
game.resizable(width = False, height = False)
game.geometry("450x305")
game.title("Hangman")
canvas = Canvas(game, bg = backcolour)
canvas.pack(expand = 1, fill = BOTH)
attemptent = Entry(canvas, width = 15, bg = userinputobjectcolour)
attemptent.place(x = 140, y = 9)
attemptlbl = Label(canvas, text = "Attempt/Letter Input:", bg = backcolour).place(x = 13, y = 7)
attemptbtn = Button(canvas, text = "Check", width = 15, command = attempt, bg = userinputobjectcolour)
attemptbtn.place(x = 252, y = 5)
guesstitlelbl = Label(canvas, text = "Guesses:", bg = backcolour, font = ("ComicSans", 12))
guesstitlelbl.place(x = 272, y = 85)
guesseslbl = Label(canvas, text = "", bg = backcolour)
guesseslbl.place(x = 284, y = 108)
newgamebtn = Button(canvas, text = "Reset game (Lose progress)", bg = userinputobjectcolour, command = setup)
newgamebtn.place(x = 236, y = 255)
liveslbl = Label(canvas, bg = backcolour, text = str("Current lives: " + str(lives[0])))
liveslbl.place(x = 267, y = 167)
wordtitlelbl = Label(canvas, text = "Hangman Word:", bg = backcolour).place(x = 75, y = 33)
wordlbl = Label(canvas, text = "", bg = backcolour)
wordlbl.place(x = 113, y = 52)
winslbl = Label(canvas, text = "Wins: 0", bg = backcolour)
losseslbl = Label(canvas, text = "Losses: 0", bg = backcolour)
winslbl.place(x = 250, y = 205)
losseslbl.place(x = 322, y = 205)

#Body

setup()
game.mainloop()
