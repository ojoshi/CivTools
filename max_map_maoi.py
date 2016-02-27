import random

# Reads data in a board object and prints it to screen
def printBoard(board):
    print "    ", board[0][4:9], "    "
    print "   " , board[1][3:9], "   "
    print "  "  , board[2][2:9], "  "
    print " "   , board[3][1:9], " "
    print         board[4]
    print " "   , board[5][0:8], " "
    print "  "  , board[6][0:7], "  "
    print "   " , board[7][0:6], "   "
    print "    ", board[8][0:5], "    " 
    print ""

def checkNeighbor(board, updated, x, y):
    if(updated[x - 1][y] == 'C' or updated[x + 1][y] == 'C' or updated[x][y - 1] == 'C' or updated[x][y + 1] == 'C' or updated[x - 1][y + 1] == 'C' or updated[x + 1][y - 1] == 'C'):
        return 'C'
    else:
        return 'L'

def classifyTile(board, updated, x, y, ring):
    if(board[x][y] == 1):
        updated[x][y] = 'M'
    elif(ring == 4): # board[x][y] == 0 so tile is water
        updated[x][y] = 'C'
    else: # tile is water and not in outer so check if coast
        updated[x][y] = checkNeighbor(board, updated, x, y)

def updateTileDef(board):
    updated = [row[:] for row in board[:]]
    for ring in range(4, 0, -1):
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

for iter in range(100):
    # Initialize empty nodes
    # nodes = [[random.randint(0,1) for i in range(0,9)] for i in range(0,9)] # random
    # nodes = [[0 for i in range(0,9)] for i in range(0,9)] # all water
    # nodes = [[1 for i in range(0,9)] for i in range(0,9)] # all maois
    nodes = [
        [0,0,0,0,    1, 0, 1, 1, 1], 
        [0,0,0,   1, 1, 1, 1, 1, 1],
        [0,0,  1, 1, 1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 0, 1, 1, 0],
        [1, 1, 0, 1, 1, 1, 1,  0,0],
        [1, 1, 0, 1, 1, 1,   0,0,0],
        [1, 1, 0, 0, 1,    0,0,0,0]
    ]
    nodes[4][4] = 'H' # H for home tile
    printBoard(nodes)
    updated = updateTileDef(nodes)
    printBoard(updated)
    exit()
    
    # Iterate over states n times
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
            #---------------
            #---------------
            
            # print "Position", x, y, "-", netscore
            # printBoard(cur)

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
        # printBoard(winner)
        
    # Progress updated
    if iter % 100 == 0 and iter != 0:
        print "Chunk complete -", iter/100

# Return winning map
printBoard(winner)

# Build scoring map 
#---------------
#---------------
                
print "Score:", roller
printBoard(scored)
