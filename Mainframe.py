#Initialise variables
import tkinter as tk
from tkinter import messagebox, simpledialog
from Shapes import *
from Highscores import *
gameGrid = []
buttons = []
points = 0
currentShape = []
lastHover = None

def getShapeCoords(x, y): #FR2: Get the coordinates of the unplaced shape inside the grid
    #Find dimensions of shape
    min_x = min(coord[0] for coord in currentShape)
    max_x = max(coord[0] for coord in currentShape)
    min_y = min(coord[1] for coord in currentShape)
    max_y = max(coord[1] for coord in currentShape)
    
    #Calculate offsets to center the shape around clicked position
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    offset_x = x - (width // 2)
    offset_y = y - (height // 2)
    
    #Check if all cells are valid and empty and append to an array of grid coordinates
    gridPositions = []
    for coord in currentShape:
        dx = offset_x + (coord[0] - min_x)
        dy = offset_y + (coord[1] - min_y)
        gridPositions.append((dx, dy))

    return gridPositions

def placementValidation(gridPositions): #FR3: Validate whether the shape can be entered in the grid
    for dx, dy in gridPositions:
        #Check if coordinate is within grid bounds
        if not (0 <= dx < len(gameGrid) and 0 <= dy < len(gameGrid)):
            return False
            
            
        #Check if cell is already occupied
        if gameGrid[dx][dy] == "X":
            return False
        
    return True

def checkGameOver(): #FR8:  Check which cells the shape can fit in. If none, return false
    for x in range(len(gameGrid)):
        for y in range(len(gameGrid)):
            gridPositions = getShapeCoords(x, y)
            if placementValidation(gridPositions):
                return False
    
    return True

def placeShape(x, y): #FR2, EU2: Place shape in the grid with validation and
    global currentShape
    
    #Get grid positions for shape
    gridPositions = getShapeCoords(x, y)
    
    #FR4: If valid, place the shape
    if placementValidation(gridPositions):
        for dx, dy in gridPositions:
            gameGrid[dx][dy] = "X"
            buttons[dx][dy].config(bg="blue")
        
        #Generate a new shape for preview
        updatePreview(prevGrid, prevBtns)

        #Removes any hover effects from the grid of buttons
        clearHover()
        
        #Check for completed rows/columns
        rowScan()

        #Check if there are no remaining places to enter the shape
        if checkGameOver():
            messagebox.showinfo("Game Over", "No more valid placements available!")
            highscoresMain(name, points)
            
def onEnter(x,y): #EU4: Shows you what a shape will look like when placed in a cell
    global lastHover, currentShape

    if lastHover == (x, y) or not currentShape:
        return

    lastHover = (x, y)

    clearHover()


    gridPositions = getShapeCoords(x, y)
    valid = placementValidation(gridPositions)
    hover_color = "lightblue" if valid else "pink"
    #Iterate for each coordinate of the shape
    for dx, dy in gridPositions:
        if 0 <= dx < len(gameGrid) and 0 <= dy < len(gameGrid):
            if gameGrid[dx][dy] == "":
                buttons[dx][dy].config(bg=hover_color)
    
def clearHover(): #EU4: Clear hover to prevent the grid from remaining highlighted
    for x in range(len(gameGrid)):
        for y in range(len(gameGrid)):
            if gameGrid[x][y] == "":
                buttons[x][y].config(bg="white")
            else:
                buttons[x][y].config(bg="blue")
                
def rowScan(): #FR7: Scan the rows for valid matches and add points, updating the label
    global points
    toClear = [["" for _ in range(len(gameGrid))] for _ in range(len(gameGrid))]
    
    #Check rows and append points
    for x in range(len(gameGrid)):
        completion = 0
        for y in range(len(gameGrid)):
            if gameGrid[x][y] == "X":
                completion += 1
        if completion == (len(gameGrid)):
            points += 100
            for y in range(len(gameGrid)):
                toClear[x][y] = "O"
                
    #Check cols and append points
    for y in range(len(gameGrid)):
        completion = 0
        for x in range(len(gameGrid)):
            if gameGrid[x][y] == "X":
                completion += 1
        if completion == (len(gameGrid)):
            points += 100
            for x in range(len(gameGrid)):
                toClear[x][y] = "O"
                
    #Clear marked cells
    for x in range(len(gameGrid)):
        for y in range(len(gameGrid)):
            if toClear[x][y] == "O":
                gameGrid[x][y] = ""
                buttons[x][y].config(bg="white")
    
    pointsLabel.config(text=f"Points: {points}")
    
def createGameGrid(size=8): #FR1: Initialise 8x8 grid as 2D array, one for buttons, and one for the value attached to them
    global gameGrid, buttons
    gameGrid = [["" for _ in range(size)] for _ in range(size)]
    buttons = [[None for _ in range(size)] for _ in range(size)]

def createMainGrid(root, size=8): #Display the main grid of buttons and the point counter 
    global pointsLabel
    pointsLabel = tk.Label(root, text=f"Points: {points}", font=("Arial", 16))
    pointsLabel.pack(pady=5)
    mainFrame = tk.Frame(root)
    mainFrame.pack(padx=10, pady=10)

    #Make an array of buttons
    for x in range(size):
        for y in range(size):
            btn = tk.Button(
                mainFrame,
                width=4,
                height=2,
                bg="white",
                command=lambda i=x, j=y: placeShape(i, j)
            )
            btn.grid(row=x, column=y, padx=2, pady=2)
            buttons[x][y] = btn
            #EU4: When mouse enters/leaves cells, the projected placement appears/disappears 
            btn.bind("<Enter>", lambda event, i=x, j=y: onEnter(i, j))
            btn.bind("<Leave>", lambda event: clearHover())
    return mainFrame

def createPreviewGrid(root, size=5):#FR6, EU3: Generate visual grid of buttons to preview the shape to be placed
    preview_label = tk.Label(root, text="Current Shape:")
    preview_label.pack(pady=(2, 2))
    previewFrame = tk.Frame(root)
    previewFrame.pack(padx=10, pady=5)
    previewButtons = [[None for _ in range(size)] for _ in range(size)]
    previewGrid = [["" for _ in range(size)] for _ in range(size)]

    #Make an array of buttons that can't be clicked
    for x in range(size):
        for y in range(size):
            btn = tk.Button(
                previewFrame,
                width=2,
                height=1,
                bg="white",
                state=tk.DISABLED
            )
            btn.grid(row=x, column=y, padx=2, pady=2)
            previewButtons[x][y] = btn
    return previewFrame, previewGrid, previewButtons

def updatePreview(previewGrid, previewButtons): #FR5, FR6: Generate a new shape and enter it into preview array
    global currentShape
    ArraySize = (len(previewGrid))
    #Clear the preview grid
    for i in range(ArraySize):
        for j in range(ArraySize):
            previewGrid[i][j] = ""
            previewButtons[i][j].config(bg="white", text="")

    currentShape = getRandomShape()

    min_x = min(coord[0] for coord in currentShape)
    max_x = max(coord[0] for coord in currentShape)
    min_y = min(coord[1] for coord in currentShape)
    max_y = max(coord[1] for coord in currentShape)

    # Calculate shape center
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    start_x = (ArraySize - width) // 2
    start_y = (ArraySize - height) // 2
    
    # Place the shape in the preview grid and validate
    for coord in currentShape:
        dx = start_x + (coord[0] - min_x)
        dy = start_y + (coord[1] - min_y)
        if 0<= dx < ArraySize and 0 <= dy < ArraySize:
            previewGrid[dx][dy] = "X"
            previewButtons[dx][dy].config(bg="blue")

def getName(): #FR9, EU5: Prompts the user to enter their name with validation 
    root = tk.Tk()
    root.title("Enter your name")
    nameVar=tk.StringVar()
    errorVar=tk.StringVar()
    #Input validation
    def submit():
        input_name = nameVar.get()
        
        if not input_name:
            errorVar.set("Name cannot be empty")
            return
        elif len(input_name) > 6:
            errorVar.set("Name must be at most 6 characters long")
            return
        else:
            global name
            name = input_name
            root.destroy()

    def onClose():
        messagebox.showinfo("", "Please enter a valid name and use the Submit button")

    #Override close button behaviour    
    root.protocol("WM_DELETE_WINDOW", onClose) 
        
    nameLabel = tk.Label(root, text = "Enter your name here", font=('Arial',10))
    nameEntry = tk.Entry(root,textvariable = nameVar, font=('Arial',10))
    errorLabel = tk.Label(root, textvariable=errorVar, font=('Arial', 9), fg='red')
    submitBtn = tk.Button(root, text = 'Submit', command = submit)

    #Arrange UI elements
    nameLabel.pack(pady=10, padx=5)
    nameEntry.pack(pady=10, padx=5)
    submitBtn.pack(pady=10, padx=5)
    errorLabel.pack(pady=10, padx=5)

    root.mainloop()
    
def main():
    global prevGrid, prevBtns
    getName()
    root = tk.Tk()
    root.title("Aboudi Blast")
    
    createGameGrid(8)
    createMainGrid(root)
    prevFrame, prevGrid, prevBtns = createPreviewGrid(root)
    updatePreview(prevGrid, prevBtns)
    
main()
