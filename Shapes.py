import random
def shapeDictionary(): #Different range of shapes there are
    shapes = {
        "z_shape": [(0, 1), (0, 2), (1, 0), (1, 1)],
        "z_flipped": [(0, 0), (0, 1), (1, 1), (1, 2)],
        "s_shape": [(0, 0), (0, 1), (1, 1), (1, 2)],
        "s_flipped": [(0, 1), (0, 2), (1, 0), (1, 1)],
        "horizontal": [(0, y) for y in range(random.randint(1, 5))],
        "vertical": [(x, 0) for x in range(random.randint(1, 5))],
        "square": squareCoords(),
        "corner": cornerCoords()
    }
    return shapes

def squareCoords():
    length = random.randint(1,3)
    coordinates = []
    for i in range (length):
        for j in range (length):
            coordinates.append((i, j))
    return coordinates
            
def cornerCoords(): 
    #Give a random length and direction to each plane
    xLength = random.randint(1,3)
    yLength = random.randint(1,3)
    xDir = random.randint(0,1)
    yDir = random.randint(0,1)
    coordinates = []
    
    #Places a corner block in the array of a random length starting at (x,y)
    for loop in range(xLength):
        if xDir==0:
            coordinates.append((loop, 0))
        if xDir==1:
            coordinates.append((-loop, 0))
            
    for loop in range(1, yLength):
        if yDir == 0:
            coordinates.append((0, loop))
        else:
            coordinates.append((0, -loop))
    return coordinates

def getRandomShape(): #FR5: Generates random shape for user to place
    shapes = shapeDictionary()
    shapeNames = list(shapes.keys())
    chosenShape = (random.choices(shapeNames, weights = [5,5,5,5,10,10,15,30], k=1 )[0])
    coords = shapes[chosenShape]

    return coords
