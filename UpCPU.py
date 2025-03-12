from copy import deepcopy

def LegalCheck(func):
    def wrapper(self, playercount, InputX, InputY1, InputY2, board):
        islegal = Minimax.LegalMove(InputX, InputY1, InputY2, board, playercount)
        return islegal
    return wrapper

def MinimaxMove(func):
    def wrapper(self, board, InputX, InputY1, InputY2):
        board = Minimax.MakeMove(board, InputX, InputY1, InputY2)
        return board
    return wrapper


class Minimax():
    def __init__(self, players):
        """
        Initializer of the Minimax Class

        Args:
            players: list containing the players for a given game in the form ["Y", "R", "B", "G"]

        List of variables:
            self.k (int): adjustable variable for the heuristic function
            self.BoardScore (list): used by the heuristic function to value each row of the board
            self.twoplayers (list): used for finding the children of a position in a two player game
            self.players (list): self.players = players
            self.playercount (int): uses the player list to calculate the playercount
        """
        self.k = 2
        self.BoardScore = [120*self.k**2, 
                      81*self.k**2,
                      64*self.k**2, 
                      49*self.k**2,
                      36*self.k**2, 
                      25*self.k**2,
                      16*self.k**2, 
                      0, 
                      0,
                      0,
                      0]
        self.twoplayers = ["G", "B"]
        self.players = players #["Y", "R", "B", "G"]
        self.playercount = len(players)

    def Minimax(self, position, depth, maximisingPlayer, currentTurn, alpha, beta):
        """
        Actual Minimax function which builds a tree in order to find the best move, where it returns the move and evaluation

        Args:
            position (2Dlist): the current board state
            depth (int): represents how deep the minimax function is 
            maximisingPlayer (bool): True or False for if the current player is to be considered the maximising or minimising player
            currentTurn (int): number from 0-3 that tells the function what turn it is so it knows what pieces it can move when simulating a game
            alpha (real): value used for alpha beta pruning
            beta (real): value used for alpha beta pruning

        List of variables:
            best_move (list): stores the optimally scoring move that the minimax function simulates
            max_eval (int): used to store the evaluation of the highest scoring move
            children (list): stores the child positions of any given board
            evaluation (int): represents the evaluation value of a nested minimax function
            z (list): unused variable that stores the position of the evaluation
            min_eval (int) used to store the evaluation of the lowest scoring move
        """

        #game over or depth 0 check
        if depth == 0 or self.GameOver(position):
            return self.EvaluatePos(position), position

        if maximisingPlayer:
            best_move = None
            max_eval = float('-inf')
            children =  self.ChildPositions(position, currentTurn)

            #if there are no child positions
            if not children: 
                return self.EvaluatePos(position), position

            #iteration function for each child
            for child in children:
                evaluation, z = self.Minimax(child, depth-1, False, self.cycleTurn(currentTurn), alpha, beta)
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = child
                
                #prune unnecesary branches
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move

        #if not maximising player
        else:
            best_move = None
            min_eval = float('inf')
            children =  self.ChildPositions(position, currentTurn)

            #if there are no child positions
            if not children:
                return self.EvaluatePos(position), position

            #iteration function for each child
            for child in children:
                evaluation, z = self.Minimax(child, depth-1, self.MaxingPlayer(currentTurn), self.cycleTurn(currentTurn), alpha, beta)
               
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = child

                #prune unnecesary branches
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move
            
    #finds the child positions of a board in the minimax function
    def ChildPositions(self, position, current_turn):
        position_list = []
        for Rindex, row in enumerate(position):
            for Eindex, element in enumerate(row):
               #if (  current piece is the player's piece  ) and (the pieces available move is legal):
                if (element == self.players[current_turn] or element == self.twoplayers[current_turn]) and self.IsLegalMove(self.playercount, Eindex, Rindex, self.FindY2(Rindex, position), position):
                    #make a copy of the board to simulate a move on
                    moved_position = deepcopy(position)
                    moved_position = self.MakeMove(moved_position, Eindex, Rindex, self.FindY2(Rindex, moved_position)) #it should RETURN a NEW BOARD: you must do copy
                    #add move to the list of all the child positions
                    position_list.append(moved_position)

        return position_list

    #evaluates a position
    def EvaluatePos(self, position):
        score = 0
        for Rindex, row in enumerate(position):
            for element in row:

                #deducts green pieces from the total to discourage developing green pieces
                if self.playercount == 3 and element == "G":
                    score -= (self.BoardScore[Rindex])*3

                #adds Y or G pieces in 2 player games
                elif element == "Y" or (self.playercount == 2 and element == "G"):
                    score += self.BoardScore[Rindex]
                
                #if any other piece, deduct score
                elif element in self.players:
                    score -= self.BoardScore[Rindex]

        return score

    #deduces if the current turn is a maximiser's turn or a minimiser's
    def MaxingPlayer(self, currentTurn):
        next_turn = self.cycleTurn(currentTurn)
        if self.players[next_turn] == "Y":
            return True
        return False

    def cycleTurn(self, currentTurn):
        return (currentTurn+1)%self.playercount

    #checks whether the position argument is a completed game
    def GameOver(self, position):
        if not self.TwoPiecesInScoringZone(position):
            return False
            
        for Rindex, row in enumerate(position):
            for Eindex, element in enumerate(row):

                #if element is a piece and can make a move
                if element != "" and self.IsLegalMove(self.playercount, Eindex, Rindex, self.FindY2(Rindex, position), position):
                    return False

        return True


    def FurthestForwardsAndMovingOnePlace(char, InputX, InputY1, InputY2, board, a=0):
        for index, row in enumerate(board):
            for index2 in range(len(row)):
                #if (the piece is the same colour as char) and (it is not in the same coloumn as char) and (its further back than char)
                if row[index2] == char and index2 != InputX and index > InputY1:
                    a += 1   

        if a == 3:
            is_piece_the_furthest_forwards = True
        else:
           return False

       #if (    moves one tile    ) and (is the furthest piece forwads of its colour)      
        if (InputY1 - InputY2 == 1) and (is_piece_the_furthest_forwards):
            return True
        return False

    #returns an int of how many pieces are in the given Y value of a board
    def NumberOfPiecesInLane(InputY1, board):
        counter = 4

        for char in board[InputY1]:
            if char == "":
                counter -= 1
        return counter

    #checks if there are matching colours in the same row of the board in the non scoring rows
    def MatchingColours(playercount, char, InputX, InputY2, board):
        if InputY2 > 4 or playercount == 1: 
            for element in board[InputY2]:
                if element == char:
                    return False
                
        return True    

    def TwoPiecesInScoringZone(self, board):
        #a rule where if there are two pieces in the non-scoring zone, return True, game over
        pieces = 0
        for number, line in enumerate(board):
            if number > 4:
                for char in line:
                    if char != "":
                        pieces += 1
        if pieces < 3:
            return True
        return False

    #finds the Y position of a move 
    def FindY2(self, InputY1, board):
        counter = 4

        for char in board[InputY1]:
            if char == "":
                counter -= 1
        return (max(InputY1 - counter, 0))

    #moves whatever is in the first YX value into the second Y2X value and then clears the YX
    @staticmethod           
    def MakeMove(board, InputX, InputY1, InputY2):
        board[InputY2][InputX] = board[InputY1][InputX]
        board[InputY1][InputX] = ""
        return board
    
    @staticmethod  
    def LegalMove(InputX, InputY1, InputY2, board, playercount):   
        """
        1. A piece must move exactly as how many space up as there are pieces in the horisontal row from which it departs. (Thus, if there are two pieces in a row, either piece may move up exactly two spaces, after one piece is moved, the other may only move up one space since it has become the solitary piece in the row)
        2. Only one piece may occupy a space, pieces may jump over other pieces, as long as they land on empty spaces
        3. The most advanced piece of a colour may not make a single space move. (Therefore a piece that is alone in a row cannot move if the other three pieces of the same colour are below it on the board).
        4. On any of the bottom six rows of the board, (the non scoring rows) two pieces of the same colour may NEVER be in the same row at the time. This restriction does not apply to the five scoring rows.
        """
        if (board[InputY2][InputX] == "" and 
            board[InputY1][InputX] != "" and 
            not Minimax.FurthestForwardsAndMovingOnePlace(board[InputY1][InputX], InputX, InputY1, InputY2, board) and 
            Minimax.NumberOfPiecesInLane(InputY1, board) == InputY1 - InputY2 and 
            Minimax.MatchingColours(playercount, board[InputY1][InputX], InputX, InputY2, board)):
            return True
        return False

    @LegalCheck
    def IsLegalMove(self, playercount, InputX, InputY1, InputY2, board):
        pass
