import random

# Reads data in a board object and prints it to screen
def printBoard(board):
    print "         ", board[0][4:9], "    "
    print "      " , board[1][3:9], "   "
    print "    "  , board[2][2:9], "  "
    print "  "   , board[3][1:9], " "
    print         board[4]
    print "  "   , board[5][0:8], " "
    print "    "  , board[6][0:7], "  "
    print "      " , board[7][0:6], "   "
    print "         ", board[8][0:5], "    " 
    print ""

# Check neighboring tiles to see if they are coast and returns appropriate classification of water
def checkNeighbor(updated, x, y):
    if(updated[x - 1][y] != 'C' and updated[x + 1][y] != 'C' and updated[x][y - 1] != 'C' and updated[x][y + 1] != 'C' and updated[x - 1][y + 1] != 'C' and updated[x + 1][y - 1] != 'C'):
        return False
    else:
        return True

# Returns a score for position x,y by checking neighboring tiles
def scoreNeighbor(updated, x, y):
    if(updated[x - 1][y] != 'C' and updated[x + 1][y] != 'C' and updated[x][y - 1] != 'C' and updated[x][y + 1] != 'C' and updated[x - 1][y + 1] != 'C' and updated[x + 1][y - 1] != 'C'):
        return 0
    count = 0
    if(updated[x - 1][y] == 'M'):
        count += 1
    if(updated[x + 1][y] == 'M'):
        count += 1
    if(updated[x][y - 1] == 'M'):
        count += 1
    if(updated[x][y + 1] == 'M'):
        count += 1
    if(updated[x - 1][y + 1] == 'M'):
        count += 1
    if(updated[x + 1][y - 1] == 'M'):
        count += 1
    return count + 1 # additional +1 for the tile itself

# Classifies tiles (water and moai)
def classifyTile(board, updated, x, y, ring):
    if(ring == 4):
        if(board[x][y] == 1): # tile is land
            updated[x][y] = 'M'
        else: # board[x][y] == 0 so tile is water
            updated[x][y] = 'C'
    else: # tile is not in outer ring
        if(board[x][y] == 1):
            if(checkNeighbor(updated, x, y)): # contains neighboring coast
                updated[x][y] = 'M'
            else:
                updated[x][y] = 'B' # B for blank
        else:
            if(checkNeighbor(updated, x, y)): # contains neighboring coast
                updated[x][y] = 'C'
            else:
                updated[x][y] = 'L' # Lake since no neighbors

# Checks board starting from ring 4 in clockwise fashion to classify tiles
def updateTileDef(board):
    updated = [row[:] for row in board[:]]
    for ring in range(4, 0, -1):
        for i in range(2): # run twice to solve issues related to unknown next tile classification
            for tile in range(ring): # top side
                x = 4 - ring
                y = 4 + tile
                classifyTile(board, updated, x, y, ring)
            for tile in range(ring): # top right side
                x = tile + (4 - ring)
                y = 4 + ring
                classifyTile(board, updated, x, y, ring)
            for tile in range(ring): # bottom right side
                x = 4 + tile
                y = (4 + ring) - tile
                classifyTile(board, updated, x, y, ring)
            for tile in range(ring): # bottom side
                x = 4 + ring
                y = 4 - tile
                classifyTile(board, updated, x, y, ring)
            for tile in range(ring): # bottom left side
                x = (4 + ring) - tile
                y = 4 - ring
                classifyTile(board, updated, x, y, ring)
            for tile in range(ring): # top left side
                x = 4 - tile
                y = (4 - ring) + tile
                classifyTile(board, updated, x, y, ring)
    return updated

def scoreMap(updated):
    # scored = [row[:] for row in updated[:]] 
    total = 0
    for x in range(1,8):
        ymin = 1
        ymax = 8
        if x <= 4:
            ymin = 5 - x # ymax is 8
        else:
            ymax = 12 - x # ymin is 1
        for y in range(ymin, ymax): 
            if updated[x][y] == 'M': # land is moai
                score = scoreNeighbor(updated, x, y)
                # scored[x][y] = score
                total += score
    # printBoard(scored)
    return total
    
def printScoredBoard(updated):
    scored = [row[:] for row in updated[:]] 
    total = 0
    for x in range(1,8):
        ymin = 1
        ymax = 8
        if x <= 4:
            ymin = 5 - x # ymax is 8
        else:
            ymax = 12 - x # ymin is 1
        for y in range(ymin, ymax): 
            if updated[x][y] == 'M': # land is moai
                score = scoreNeighbor(updated, x, y)
                scored[x][y] = str(score)
    printBoard(scored)

# Build list of tuples that need to be flipped
tuples = []
for a in range(0,9):
    bmin = 0
    bmax = 9
    if a <= 4:
        bmin = 4 - a # bmax is 9
    else:
        bmax = 13 - a # bmin is 0
    for b in range(bmin, bmax):
        tuples.append((a, b))
tuples.remove((4,4))

# Run 10,000 different searches
winningscore = 0
winner = [[]]

for iter in range(10000):
    # Initialize empty nodes
    nodes = [[random.randint(0,1) for i in range(0,9)] for i in range(0,9)] # random
    # nodes = [[0 for i in range(0,9)] for i in range(0,9)] # all water
    # nodes = [[1 for i in range(0,9)] for i in range(0,9)] # all moai
    # nodes = [
    #     [0,0,0,0,    1, 0, 1, 1, 1], 
    #     [0,0,0,   1, 0, 1, 1, 0, 0],
    #     [0,0,  1, 1, 0, 1, 0, 1, 1],
    #     [0, 0, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 1, 1, 1, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 0],
    #     [1, 1, 0, 1, 0, 1, 1,  0,0],
    #     [0, 0, 1, 1, 0, 1,   0,0,0],
    #     [1, 1, 1, 0, 1,    0,0,0,0]
    # ]
    nodes[4][4] = 'H' # H for home tile
   
    # Test a single board
    # updated = updateTileDef(nodes)
    # printBoard(updated)
    # print "Score", scoreMap(updated)
    # printScoredBoard(updated)
    # exit()
    
    # Iterate over options until score cannot be improved
    maxscore = 0
    while True: #for iter in range(0, 100):
        # Sweep all nodes in current state 
        next = [[]]
        tempscore = 0
        tupcopy = list(tuples)
        random.shuffle(tupcopy)
        for tup in tupcopy:
            cur = [row[:] for row in nodes[:]]
            cur[tup[0]][tup[1]] = 1 - cur[tup[0]][tup[1]] # flips the bit at (x,y)          
            netscore = 0
            
            # Score the current map
            updated = updateTileDef(cur)
            netscore = scoreMap(updated)
            
            # print "Position", tup[0], tup[1], "-", netscore
            # printScoredBoard(updated)

            # If this is current high score, save map
            if netscore >= tempscore:
                next = cur # points to copied memory of nodes that has been updated
                tempscore = netscore
        
        # Terminates run if current change doesn't improve maximum score for current run
        if tempscore <= maxscore:
            break
        else:
            maxscore = tempscore
            nodes = next
            #print "Iteration", iter, "-", maxscore
            # printBoard(nodes)
    
    # Update winner if latest run is better
    if maxscore > winningscore:
        winningscore = maxscore
        winner = nodes
        print "Winner", iter, "-", maxscore
        formatted = updateTileDef(winner)
        printBoard(formatted)
        printScoredBoard(formatted)
        
    # Progress updated
    if iter % 100 == 0 and iter != 0:
        print "Chunk complete -", iter/100

# Return winning map
updated = updateTileDef(winner)
netscore = scoreMap(updated)
print "Score:", netscore
printBoard(updated)
printScoredBoard(updated)
