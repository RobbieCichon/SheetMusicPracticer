"""
Sheet Music Practicer Program
Author: Robert Cichon
Description: Using the tkinter package as a graphical userface base, the program will display a randomly chosen musical note
on a staff. The user is at the same time given a text box to input the identifying character(s) for that note.
The program will process the answer and, if correct, will award points dependent on the speed of the answer given.
The program has a leaderboard with logic to keep a running total score of only your last 25 inputs and once the user
is done with the program it will display the highest score achieved and prompt for a name.
This way, the leaderboard will represent speedy players rather than marathoners.
"""
#Import Libraries
from tkinter import *
import tkinter.messagebox
import asyncio
import os
import random
from PIL import ImageTk, Image

#Create main display
window = Tk()
window.title("Music Note Guesser")
window.geometry("640x500")
window.configure(background="black")

#Create and initialize global variables
CurrentTime = 0
Name = ""
LastTime = 0
HighScore = 0
ScoreList = [0]*25
ScoreListIndex = 0
MinuteCount = StringVar( value = ' 00 ')
SecondCount = StringVar(value = ' 00 ')
MilSecondCount = StringVar(value = ' 0 ')
Colon = StringVar(value = ':')
Period = StringVar(value = '.')
FirstEnter = True
TimerGoing = False

#Create Timer
MinuteLabel = Label(font=('Arial', 25), textvariable = MinuteCount)
FirstColon = Label(font=('Arial', 25), textvariable = Colon)
SecondLabel = Label(font=('Arial', 25), textvariable = SecondCount)
SecondColon = Label(font=('Arial', 25), textvariable = Period)
MilSecondLabel = Label(font=('Arial', 25), textvariable = MilSecondCount)

MinuteLabel.grid(column=0, row=3)
FirstColon.grid(column=1, row=3)
SecondLabel.grid(column=2, row=3)
SecondColon.grid(column=3, row=3)
MilSecondLabel.grid(column=4, row=3)

#Create Timer Logic
async def TimerStart():
    #Initialize local variables
    milsecond = 0
    second = 0
    minute = 0
    global TimerGoing
    global CurrentTime

    #Timer logic to display and count the milliseconds
    while TimerGoing:
        if milsecond <= 8:
            milsecond += 1
            MilSecondCount.set(f' {milsecond} ')
        else:
            if second <= 8:
                second += 1
                SecondCount.set(f' 0{second} ')
            else:
                second += 1
                SecondCount.set(f' {second} ')
            if second >= 60:
                if minute <= 8:
                    minute += 1
                    MinuteCount.set(f' 0{minute} ')
                else:
                    minute +=1
                    MinuteCount.set(f' {minute} ') 
                second = 0
                SecondCount.set(f' 0{second} ')
            milsecond = 0
            MilSecondCount.set(f' {milsecond} ')
        if milsecond % 3:
            window.configure(background="black")
        CurrentTime += 1
        window.update()
        await asyncio.sleep(.1)


#Create the image path, this will be changed later on to randomly select a file
path = "SheetMusicImages/C!.png"
img = ImageTk.PhotoImage(Image.open(path))

def FindNewNote():
    #Intialize variables
    path = "SheetMusicImages"
    ImageList = os.listdir(path)
    global NewImage
    global CurrentPath

    CurrentPath = os.path.basename(ImageList[random.randint(0, 27)])
    NewImage = ImageTk.PhotoImage(Image.open(path + "/" + CurrentPath))

    ImagePanel.configure(image=NewImage)
    window.update()

#Quit Button Function
def QuButPress():
    global TimerGoing
    global HighScore
    ScoreTable = ""
    Index = 10

    HighScoreHandler()
    HSFile = open("HighScores.txt","r")
    HighScoreList = HSFile.readlines()
    if len(HighScoreList) < 10:
        Index = len(HighScoreList)
    for x in range(Index):
        ScoreTable += HighScoreList[x] + "\n"

    messtring = "Your score: " + str(HighScore) + "\n\n" + "High Score Table:" + "\n" + ScoreTable
    tkinter.messagebox.showinfo("High Scores", messtring)
    TimerGoing = False
    window.destroy()

#Highscore text file hander
def HighScoreHandler():
    global HighScore
    global Name
    NameNotUsed = True

    try:
        (open("HighScores.txt","r+"))
    except:
        HSFile = open("HighScores.txt","w")
        HSFile.write(Name+": "+str(HighScore)+" points\n")
        HSFile.close()
    else:
        HSFile = open("HighScores.txt", "r")
        HSList = HSFile.readlines()
        HighScores = {}
        for x in range(len(HSList)):
            Line = HSList[x].split()
            for t in range(len(Line)):
                if t == 0:
                    HSName = Line[t]
                else:
                    if Line[t].isdigit():
                        HighScores[HSName] = Line[t]
        HSFile.close()
        
        HSFile = open("HighScores.txt","w")
        for key in HighScores:
            if NameNotUsed:
                if HighScore > int(HighScores[key]):
                    HSFile.write(Name+": "+str(HighScore)+" points\n")
                    HSFile.write(key+" "+str(HighScores[key])+" points\n")
                    NameNotUsed = False
                else:
                    HSFile.write(key+" "+str(HighScores[key])+" points\n")
            else:
                HSFile.write(key+" "+str(HighScores[key])+" points\n")
        HSFile.close()

#Create Quit button
QuitButton = Button(window, text="Quit", command=QuButPress)
QuitButton.grid(column=5, row=1)

#Insert a textbox for input
Input = Entry(window, width = 25)
Input.grid(column=5, row=2)

#Create window to hold the displayed image
ImagePanel = Label(window, image = img)
ImagePanel.grid(column=5, row=3)

#Create a method to retrieve the text from the input box
def Enter_Pressed(event):
    global CurrentTime
    global ScoreListIndex
    global FirstEnter
    global Name
    global TimerGoing
    global CurrentPath
    global LastTime
    global HighScore
    ScoreSum = 0
    CurrentGuess = Input.get()

    #First input is name for leaderboard use
    if FirstEnter:
        Name = CurrentGuess
        FirstEnter = False
        CurrentPath = "C.png"
        Input.delete("0", END)
        TimerGoing = True
        asyncio.run(TimerStart())
        return

    #Logic for checking if the guess is right
    CurrentGuess = CurrentGuess.lower()
    Note = CurrentPath[0].lower()
    if CurrentGuess == Note:
        Points = round((1 / (CurrentTime - LastTime)) * 500) #Change value later on a feeling basis later, or even include logic for a point slope
        LastTime = CurrentTime

        ScoreList[ScoreListIndex] = Points
        ScoreListIndex += 1

        if ScoreListIndex >= 25:
            ScoreListIndex = 0
        
        window.configure(background="green")
        ScoreSum = sum(ScoreList)
        if ScoreSum > HighScore:
            HighScore = ScoreSum
        print(ScoreSum)
        FindNewNote()
    else:
        window.configure(background="red")


    Input.delete('0', END)

window.bind("<Return>", Enter_Pressed)

window.mainloop()
