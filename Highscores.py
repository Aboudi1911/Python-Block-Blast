#Initialise values
from dataclasses import dataclass
from WebInput import *
@dataclass
class highscores:
    user: str = None
    score: int = 0
    
def readFile(): #FR11: Retrieve scores from CSV file
    scoresArray = [highscores()]
    #Will attempt to open the file
    try:
        readfile = open ("scores.csv", "r")
        line = readfile.readline().rstrip('\n')
        while line:
            items = line.split(",")
            current_score = highscores(user=items[0], score=int(items[1]))
            scoresArray.append(current_score)
            line = readfile.readline().rstrip('\n')

    #If file isn't found, it creates a new file
    except FileNotFoundError:
        open("scores.csv", "w").close()
    
    return scoresArray

def saveFile(scoresArray): #FR11: Store scores in CSV file
    #FR12: Only keep the top 10 scores
    if len(scoresArray) > 10:
        scoresArray = scoresArray[:10] 
    else:
        scoresArray
        
    with open("scores.csv", "w") as writefile:
        for score in scoresArray:
            if score.user != None:
                writefile.write(f"{score.user},{score.score}\n")

def insertionSort(scoresArray): #FR10: Sort high scores using insertion sort
    n = len(scoresArray)
    if n <= 1:
        return scoresArray
    for loop in range(1, n):
        key = scoresArray[loop]
        pos = loop-1
        while pos >= 0 and key.score > scoresArray[pos].score:
            scoresArray[pos+1] = scoresArray[pos]
            pos -= 1
        scoresArray[pos+1] = key
    return scoresArray

def webMain(): #FR13: Opens web browser to display list
    array = readFile()
    viewWeb(array)

def checkDuplicates(scoresArray, name, points): #If current name is greater than
    #old name, delete old name, otherwise, return false.
    valid = "True"
    foundGreater = False
    for loop in range(len(scoresArray)):
        if scoresArray[loop].user == name:
            if scoresArray[loop].score > points:
                valid = "False"
            else:
                foundGreater = True
                duplicateIndex = loop

    if foundGreater:
        scoresArray.pop(duplicateIndex)
    return valid, scoresArray

def highscoresMain(name, points): #Main procedure
    scoresArray = readFile()
    duplicate, scoresArray = checkDuplicates(scoresArray, name, points)
    #If the name isn't a duplicate then add it to the file
    if duplicate != "False":
        currentRecord = highscores(user=str(name), score=int(points))
        scoresArray.append(currentRecord)
        scoresArray = insertionSort(scoresArray)
        saveFile(scoresArray)
    webMain()

