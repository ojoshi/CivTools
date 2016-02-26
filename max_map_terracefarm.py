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
    nodes = [[random.randint(0,1) for i in range(0,9)] for i in range(0,9)] # random
    # nodes = [[0 for i in range(0,9)] for i in range(0,9)] # all farms
    # nodes = [[1 for i in range(0,9)] for i in range(0,9)] # all mountains
    # nodes = [
    #     [0,0,0,0,       1, 0, 1, 1, 1], 
    #     [0,0,0,      1, 1, 1, 1, 1, 1],
    #     [0,0,     1, 1, 1, 1, 0, 1, 1],
    #     [0,    1, 1, 0, 1, 1, 1, 1, 0],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1   ],
    #     [0, 1, 1, 1, 1, 0, 1, 1,    0],
    #     [1, 1, 0, 1, 1, 1, 1,     0,0],
    #     [1, 1, 1, 1, 1, 1,      0,0,0],
    #     [1, 1, 1, 0, 1,       0,0,0,0]
    # ]
    nodes[4][4] = 0
    
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
            
            #Score the current map
            for x in range(1,8):
                ymin = 1
                ymax = 8
                if x <= 4:
                    ymin = 5 - x # ymax is 8
                else:
                    ymax = 12 - x # ymin is 1
                for y in range(ymin, ymax): # land is farm but not city center
                    if cur[x][y] == 0 and (x != 4 or y != 4):
                        bonus = cur[x+1][y] + cur[x-1][y] + cur[x][y-1] + cur[x][y+1] + cur[x+1][y-1] + cur[x-1][y+1]
                        netscore += (bonus + 1)
            
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
scored = [row[:] for row in winner[:]]
roller = 0
for x in range(1,8):
    ymin = 1
    ymax = 8
    if x <= 4:
        ymin = 5 - x # ymax is 8
    else:
        ymax = 12 - x # ymin is 1
    for y in range(ymin, ymax):
        if winner[x][y] == 0 and (x != 4 or y != 4): # location is land and not city center
            bonus = winner[x+1][y] + winner[x-1][y] + winner[x][y-1] + winner[x][y+1] + winner[x+1][y-1] + winner[x-1][y+1]
            scored[x][y] = bonus + 1
            roller += bonus + 1
        else:
            scored[x][y] = 0 # mountain or city centre
                
print "Score:", roller
printBoard(scored)
