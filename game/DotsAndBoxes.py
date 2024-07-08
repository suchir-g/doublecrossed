class DotsAndBoxes:
    def __init__(self, height, width, startingPlayer=0):
        # height and width are both in dot counts
        self.height = height
        self.width = width

        self.verticalLines = [
            [0 for i in range(width)] for j in range(height - 1)]
        self.horizontalLines = [
            [0 for i in range(width - 1)] for j in range(height)]

        self.boxes = [[-1 for i in range(width - 1)]
                      for j in range(height - 1)]

        # human player is player 0, AI player is player 1
        self.boxCounts = [0, 0]

        self.playerTurn = startingPlayer

    def displayGrid(self):
        print("\nGrid:\n")
        for i in range(self.height):
            # display horizontal lines and dots
            for j in range(self.width):
                if j < self.width - 1:
                    print('o', end='') 
                    if self.horizontalLines[i][j] == 1:
                        print('---', end='') 
                    else:
                        print('   ', end='')
                else:
                    print('o') 

            if i < self.height - 1:
                for j in range(self.width):
                    if j < self.width - 1:
                        if self.verticalLines[i][j] == 1:
                            print('|', end='')  
                        else:
                            print(' ', end='') 

                        if self.boxes[i][j] == -1:
                            print('   ', end='')  
                        elif self.boxes[i][j] == 0:
                            print(' 0 ', end='')  # human box
                        else:
                            print(' 1 ', end='')  # AI box
                    else:
                        if self.verticalLines[i][j] == 1:
                            print('|')  
                        else:
                            print(' ')  

    # these are just helper functions to facilitate conversion if i do decide to link to a website

    def exportToString(self):
        # the string will look like this:
        # height/width/turn/verticalLines/horizontalLines/boxes
        # 3/5/0/010,010.../01,01,01.../01,01,01...

        return f"{self.height}/{self.width}/{','.join(''.join([str(f) for f in self.verticalLines]))}/{','.join(''.join([str(f) for f in self.horizontalLines]))}/{','.join(''.join([str(f) for f in self.boxes]))}"

    def importFromString(self, string):
        # the string will look like this:
        # height/width/turn/verticalLines/horizontalLines/boxes
        # 3/5/0/010,010.../01,01,01.../01,01,01...

        parts = dataString.split('/')
        self.height = int(parts[0])
        self.width = int(parts[1])
        self.playerTurn = int(parts[2])

        verticalLinesStrings = parts[3].split(',')
        self.verticalLines = [[int(x) for x in line]
                              for line in verticalLinesStrings]

        horizontalLinesStrings = parts[4].split(',')
        self.horizontalLines = [[int(x) for x in line]
                                for line in horizontalLinesStrings]

        boxesStrings = parts[5].split(',')
        self.boxes = [[int(x) for x in line] for line in boxesStrings]

    def playMove(self, lineType, vPos, hPos, player):
        # this will return a value representing if we complete any boxes with this move
        if lineType == "v":
            if 0 <= hPos < len(self.verticalLines[0]) and 0 <= vPos < len(self.verticalLines):
                if self.verticalLines[vPos][hPos] == 0:
                    self.verticalLines[vPos][hPos] = 1
                else:
                    print("Move already played")
                    return False
            else:
                print("Move out of bounds")
                return False
        elif lineType == "h":
            if 0 <= hPos < len(self.horizontalLines[0]) and 0 <= vPos < len(self.horizontalLines):
                if self.horizontalLines[vPos][hPos] == 0:
                    self.horizontalLines[vPos][hPos] = 1
                else:
                    print("Move already played")
                    return False
            else:
                print("Move out of bounds")
                return False

        # detect if any boxes were completed by this move by using the predetermined function
        boxesCompleted = self.countBoxesCompleted(lineType, vPos, hPos)
        if boxesCompleted > 0:
            self.detectBoxesAndAddPoints(player) # adds points since it's still a move we have to add to the game state
        return boxesCompleted > 0

    def detectBoxesAndAddPoints(self, player):
        for i in range(self.height - 1):
            for j in range(self.width - 1):

                # this will loop through all the "boxes" - each box will be accounted for here.
                # looking at the indexes, the line above will be in horizontalLines[i][j], the line below will be at horizontalLines[i+1, j]
                # and similarly for vertical lines at [i, j] and [i, j+1]
                # if all of these are 1, then we have a box

                boxCount = 0

                if self.horizontalLines[i][j] == self.horizontalLines[i+1][j] == 1:
                    if self.verticalLines[i][j] == self.verticalLines[i][j+1] == 1:
                        if self.boxes[i][j] == -1:
                            self.boxes[i][j] = player
                            self.boxCounts[player] += 1

    def countLongChains(self):

        # this is essentially a count of all connected components if you treat this grid as a graph!
        # so we can use a dfs algorithm to do this

        # we have to be careful though in the fact that a long chain has 3 or more components

        visited = set()
        totalChainCount = 0

        def recurse(position):
            if position in visited:
                return 0
            visited.add(position)

            chainLength = 1

            # up
            if position[0] > 0 and self.horizontalLines[position[0]][position[1]] == 0:
                chainLength += recurse((position[0] - 1, position[1]))

            # down
            if position[0] < self.height - 2 and self.horizontalLines[position[0] + 1][position[1]] == 0:
                chainLength += recurse((position[0] + 1, position[1]))

            # left
            if position[1] > 0 and self.verticalLines[position[0]][position[1]] == 0:
                chainLength += recurse((position[0], position[1] - 1))

            # right
            if position[1] < self.width - 2 and self.verticalLines[position[0]][position[1] + 1] == 0:
                chainLength += recurse((position[0], position[1] + 1))

            return chainLength

        for i in range(self.height - 1):
            for j in range(self.width - 1):
                if (i, j) not in visited:
                    chainLength = recurse((i, j))
                    if chainLength >= 3:
                        totalChainCount += 1

        return totalChainCount

    def inCriticalPosition(self):

        # a critical position is a position we have defined such that any move made in this position would cause the opponent to gain a box (or many)
        # so we essentially simulate all the moves and check if they lead to completion of boxes

        for i in range(self.height):
            for j in range(self.width - 1):
                if self.horizontalLines[i][j] == 0:
                    if self.countBoxesCompleted("h", i, j) == 0:
                        return False

        for i in range(self.height - 1):
            for j in range(self.width):
                if self.verticalLines[i][j] == 0:
                    if self.countBoxesCompleted("v", i, j) == 0:
                        return False

        return True

    def canStartLongChain(self):
        # this method will check if the current player can complete a long chain with one move

        # again, this uses a dfs algorithm to check for long chains

        def recurse(position, visited):
            if position in visited:
                return 0
            visited.add(position)
            chainLength = 1
            if position[0] > 0 and self.horizontalLines[position[0]][position[1]] == 0:
                chainLength += recurse((position[0] - 1, position[1]), visited)
            if position[0] < self.height - 2 and self.horizontalLines[position[0] + 1][position[1]] == 0:
                chainLength += recurse((position[0] + 1, position[1]), visited)
            if position[1] > 0 and self.verticalLines[position[0]][position[1]] == 0:
                chainLength += recurse((position[0], position[1] - 1), visited)
            if position[1] < self.width - 2 and self.verticalLines[position[0]][position[1] + 1] == 0:
                chainLength += recurse((position[0], position[1] + 1), visited)
            return chainLength

        for i in range(self.height - 1):
            for j in range(self.width - 1):
                visited = set()
                if recurse((i, j), visited) >= 3:
                    return True
        return False

    def countBoxesCompleted(self, lineType, vPos, hPos):
        completedBoxes = 0

        # essentially here we are simulating "placing" a line in, and then checking if there are any boxes complete
        # in order to save time, we only check the lines "connecting" to the line placed in a box, so it's just a load of cases
        # if you draw a box out and label the indices this becomes a lot easier to visualise especially with the indexing

        if lineType == "v":
            if (hPos > 0 and self.horizontalLines[vPos][hPos - 1] == 1 and
                self.horizontalLines[vPos + 1][hPos - 1] == 1 and
                    self.verticalLines[vPos][hPos - 1] == 1):
                completedBoxes += 1
            if (hPos < self.width - 1 and self.horizontalLines[vPos][hPos] == 1 and
                self.horizontalLines[vPos + 1][hPos] == 1 and
                    self.verticalLines[vPos][hPos + 1] == 1):
                completedBoxes += 1
        elif lineType == "h":
            if (vPos > 0 and self.verticalLines[vPos - 1][hPos] == 1 and
                self.verticalLines[vPos - 1][hPos + 1] == 1 and
                    self.horizontalLines[vPos - 1][hPos] == 1):
                completedBoxes += 1
            if (vPos < self.height - 1 and self.verticalLines[vPos][hPos] == 1 and
                self.verticalLines[vPos][hPos + 1] == 1 and
                    self.horizontalLines[vPos + 1][hPos] == 1):
                completedBoxes += 1
        return completedBoxes

    def evaluatePosition(self):
        # if the position is critical, if the player can complete a long chain, they are winning else they are losing
        # this is because they can complete a long chain and then make a double dealing move at the end, keeping control
        # if the position is critical and the player can't complete a long chain (e.g. are forced to start a long chain), then they are losing

        # if the position isn't critical, we want to adhere to the long chain rule
        # the starting player wants to make the number of dots (width * height) + number of long chains even, and the second player wants to make this odd

        # we also want to take into account the number of squares each player has right now

        # all this is implemented in our evaluate position function, which is used for the minimax algorithm

        critical_position = self.inCriticalPosition()

        long_chain_count = self.countLongChains()

        total_dots = self.height * self.width

        player_0_score = self.boxCounts[0]
        player_1_score = self.boxCounts[1]

        metric_sum = long_chain_count + total_dots
        is_even = metric_sum % 2 == 0

        can_complete_long_chain = self.canStartLongChain()

        can_complete_two_boxes = any(
            (self.countBoxesCompleted("v", i, j) > 2) for i in range(self.height - 1) for j in range(self.width)
        ) or any(
            (self.countBoxesCompleted("h", i, j) > 2) for i in range(self.height) for j in range(self.width - 1)
        )

        # evaluate position based on the parity and critical position
        if critical_position:
            if can_complete_long_chain:
                # favorable for the current player to complete a long chain
                score = 100
            elif can_complete_two_boxes:
                # unfavorable if the move completes two boxes
                score = -100
            else:
                # unfavorable if forced to concede long chains
                score = -50
        else:
            if is_even:
                if self.playerTurn == 0:
                    score = 50 + (player_0_score - player_1_score) * 10
                else:
                    score = -50 + (player_0_score - player_1_score) * 10
            else:
                if self.playerTurn == 0:
                    score = -50 + (player_0_score - player_1_score) * 10
                else:
                    score = 50 + (player_0_score - player_1_score) * 10

        return score

    def minimax(self, depth, alpha, beta, maximizingPlayer):

        # this is a simple minimax algorithm with alpha beta pruning
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/ 
        # we need to also remember in this minimax that when you get a box, you get an extra turn, something which isn't there in most turn based games

        if depth == 0 or self.isGameOver():
            return self.evaluatePosition()

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.generateMoves():
                self.applyMove(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.undoMove(move)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in self.generateMoves():
                self.applyMove(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.undoMove(move)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def generateMoves(self):

        # simply loops through all the possible moves and generates a list

        moves = []
        for i in range(self.height):
            for j in range(self.width - 1):
                if self.horizontalLines[i][j] == 0:
                    moves.append(("h", i, j))
        for i in range(self.height - 1):
            for j in range(self.width):
                if self.verticalLines[i][j] == 0:
                    moves.append(("v", i, j))
        return moves

    # the 2 functions below are for simulating moves in the minimax algorithm's recursion
    # apply move and undomove are opposites of each other

    def applyMove(self, move):
        lineType, vPos, hPos = move
        if lineType == "v":
            self.verticalLines[vPos][hPos] = 1
        elif lineType == "h":
            self.horizontalLines[vPos][hPos] = 1
        self.playerTurn = 1 - self.playerTurn

    def undoMove(self, move):
        lineType, vPos, hPos = move
        if lineType == "v":
            self.verticalLines[vPos][hPos] = 0
        elif lineType == "h":
            self.horizontalLines[vPos][hPos] = 0
        self.playerTurn = 1 - self.playerTurn

    # to check if we've reached the terminal state, we can just check if every line has been filled. 
    # if every line has been filled, then we have grounds to stop the game

    def isGameOver(self):
        for i in range(self.height):
            for j in range(self.width - 1):
                if self.horizontalLines[i][j] == 0:
                    return False
        for i in range(self.height - 1):
            for j in range(self.width):
                if self.verticalLines[i][j] == 0:
                    return False
        return True

    def countChainLength(self):
        # this method will count the length of chains in the current position
        # again, this uses a dfs algorithm with recursion, but this time counts the longest chain length
        visited = set()

        def recurse(position):
            if position in visited:
                return 0
            visited.add(position)
            chainLength = 1
            if position[0] > 0 and self.horizontalLines[position[0]][position[1]] == 0:
                chainLength += recurse((position[0] - 1, position[1]))
            if position[0] < self.height - 2 and self.horizontalLines[position[0] + 1][position[1]] == 0:
                chainLength += recurse((position[0] + 1, position[1]))
            if position[1] > 0 and self.verticalLines[position[0]][position[1]] == 0:
                chainLength += recurse((position[0], position[1] - 1))
            if position[1] < self.width - 2 and self.verticalLines[position[0]][position[1] + 1] == 0:
                chainLength += recurse((position[0], position[1] + 1))
            return chainLength

        maxChainLength = 0
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                if (i, j) not in visited:
                    chainLength = recurse((i, j))
                    if chainLength > maxChainLength:
                        maxChainLength = chainLength

        return maxChainLength

    def makeMove(self):

        # this function makes the AI move, and it has a lot of factors affecting it

        critical_position = self.inCriticalPosition()

        if critical_position:
            bestMove = None
            maxLength = 0
            for move in self.generateMoves():
                lineType, vPos, hPos = move
                self.applyMove(move)
                chain_length = self.countChainLength()
                self.undoMove(move)
                if chain_length > maxLength:
                    maxLength = chain_length
                    bestMove = move
            return bestMove
        else:
            # check for moves that complete a box and then allow for a safe second move
            safe_moves = []
            for move in self.generateMoves():
                lineType, vPos, hPos = move
                if self.countBoxesCompleted(lineType, vPos, hPos) > 0:
                    self.applyMove(move)
                    second_move_safe = False
                    for next_move in self.generateMoves():
                        next_lineType, next_vPos, next_hPos = next_move
                        if self.countBoxesCompleted(next_lineType, next_vPos, next_hPos) == 0:
                            self.applyMove(next_move)
                            opponent_moves = self.generateMoves()
                            opponent_can_complete_box = False
                            for op_move in opponent_moves:
                                op_lineType, op_vPos, op_hPos = op_move
                                if self.countBoxesCompleted(op_lineType, op_vPos, op_hPos) > 0:
                                    opponent_can_complete_box = True
                                    break
                            self.undoMove(next_move)
                            if not opponent_can_complete_box:
                                second_move_safe = True
                                break
                    self.undoMove(move)
                    if second_move_safe:
                        safe_moves.append(move)

            if safe_moves:
                return safe_moves[0]

            # check for moves that do not allow the opponent to create a box
            safe_moves_from_opponent = []
            for move in self.generateMoves():
                self.applyMove(move)
                opponent_can_complete_box = False
                for op_move in self.generateMoves():
                    op_lineType, op_vPos, op_hPos = op_move
                    if self.countBoxesCompleted(op_lineType, op_vPos, op_hPos) > 0:
                        opponent_can_complete_box = True
                        break
                self.undoMove(move)
                if not opponent_can_complete_box:
                    safe_moves_from_opponent.append(move)

            if safe_moves_from_opponent:
                print(f"Safe moves from opponent available: {
                    safe_moves_from_opponent}")  # Debugging line
                return safe_moves_from_opponent[0]

            # if no such move, proceed with minimax evaluation
            bestMove = None
            bestValue = float('-inf') if self.playerTurn == 0 else float('inf')
            for move in self.generateMoves():
                lineType, vPos, hPos = move
                self.applyMove(move)
                boardValue = self.minimax(
                    3, float('-inf'), float('inf'), self.playerTurn == 1)
                self.undoMove(move)
                if (self.playerTurn == 0 and boardValue > bestValue) or (self.playerTurn == 1 and boardValue < bestValue):
                    bestValue = boardValue
                    bestMove = move
            return bestMove
