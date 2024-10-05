
class UpThrustBoard():
    
    def __init__(self):
        self.ListOfMoves = [] #2D list that holds all the moves minimax has made do they can be called upon later
        self.maxScore = 0
        self.minScore = 0
        self.max_pieces = ["R", "G"]
        self.Clicked = False
        self.click_1_x = 0
        self.click_1_y = 0
        self.j = 0
        self.playerCount = 4
        self.moves = [[0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0]]
        self.minimoves = []
        self.game = {
            'GAMEOVER' : False,
            'winner': None,
            'turn': 1
            }
        self.playerColour = {
            1: 'R',
            2: 'B',
            3: 'G',
            0: 'Y'
            }
        
        #row = ['' for i in range(4)]
        #board = [row for i in range(7)]
        #board += [lst[:i] + lst[i:] for i in range(4)]
        AiPlayers = {1:False, 2:False, 3:False, 4:False}

        self.Board = [["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["B", "Y", "G", "R"], 
                      ["Y", "G", "R", "B"],
                      ["G", "R", "B", "Y"],
                      ["R", "B", "Y", "G"]]

        self.Board2 = [["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["B", "Y", "G", "R"], 
                      ["Y", "G", "R", "B"],
                      ["G", "R", "B", "Y"],
                      ["R", "B", "Y", "G"]]

        self.BoardScore = [[140], 
                      [120],
                      [100], 
                      [80],
                      [60], 
                      [40],
                      [20], 
                      [0], 
                      [-10],
                      [-20],
                      [-20]]
    def CycleThruPlayerTurns(self):
        if self.playerCount == 4:
            self.game['turn'] = (self.game['turn']+1)%4
            print(self.game['turn'])
                
        if self.playerCount == 3:
            self.game['turn'] = (self.game['turn']+1)%3
        
        if self.playerCount == 2:
            self.game['turn'] = (self.game['turn']+1)%2

    def GetMaximisingPlayer(self):
        if self.game['turn']%2 == 0: #if turn is an even number
            return True

        return False
        
    def GetBoard(self):
        return self.Board
    
    def NumberOfPiecesInLane(self, InputX, InputY1, InputY2):
        counter = 4
        for char in self.Board[InputY1]:
            if char == "":
                counter -= 1
        return counter
    
    def MatchingColours(self, char, InputX, InputY2):
        if InputY2 > 5:
            for element in self.Board[InputY2]:
                if element == char:
                    return False
                
        return True
        
    def FarForwards(self, char, InputX, InputY1, InputY2):
        if (InputY1 - InputY2 == 1) & (self.IsFurthestForwards(char, InputX, InputY1)):
            print("not far")
            return False
        print("far")
        return True

    def IsFurthestForwards(self, char, InputX, InputY1, a=0):
        for index, row in enumerate(self.Board):
            for i in range(len(row)):
                if row[i] == char and i != InputX and index >= InputY1:
                    a += 1                 
        if a == 3:
            print("is furth:True")
            return True
        else:
            print("is furthFalse")
            return False
                
    
    #have something that checks the validity of a move (to be called upon later)
    def LegalMove(self, InputX, InputY1, InputY2):
        if (self.Board[InputY2][InputX] == "" and 
            self.Board[InputY1][InputX] != "" and 
            self.FarForwards(self.Board[InputY1][InputX], InputX, InputY1, InputY2) and 
            self.NumberOfPiecesInLane(InputX, InputY1, InputY2) == InputY1 - InputY2 and 
            self.MatchingColours(self.Board[InputY1][InputX], InputX, InputY2) and 
            self.playerColour[self.game['turn']] == self.Board[InputY1][InputX]):
            return True
        else:
            return False


    #have something that makes moves 
    def MakeMove(self, InputX, InputY1, InputY2):
        if self.LegalMove(InputX, InputY1, InputY2):
            
            
            self.moves.append([InputY1, InputX, InputY2])
            self.moves.pop(0)
            
            '''
            InputX -= 1
            InputY1 = 10 - InputY1
            InputY2 = 10 - InputY2
            '''
            self.Board[InputY2][InputX] = self.Board[InputY1][InputX]
            self.Board[InputY1][InputX] = ""
            print(self.Board)
            self.CycleThruPlayerTurns()

#have something that reverses moves
#have a list of moves, and draw upon the last move that was made
    def RetractMove(self, InputX, InputY1, InputY2):
        self.Board[self.moves[9][0]][self.moves[9][1]] = self.Board[self.moves[9][2]][self.moves[9][1]] 
        self.Board[self.moves[9][2]][self.moves[9][1]] = ""        
                
    def NoLegalMoves(self):
        number_of_legal_moves = 16
        for index, line in enumerate(self.Board):
            for locus, char in enumerate(line):
                if self.LegalMove(locus, index, 4 - line.count("")) == True:
                    continue
                else:
                    number_of_legal_moves -= 1
                    
        if number_of_legal_moves == 0:
            return True
        else:
            return False
        
    def TwoPiecesInScoringZone(self):
        pieces = 0
        for number, line in enumerate(self.Board):
            if number > 4:
                for char in line:
                    if char != "":
                        pieces += 1
        if pieces < 3:
            return True
        else:
            return False
        
    def ClickOne(self, pos):
        print("woo")
        self.Clicked = True
        self.click_1_x = pos[0] // (300 // 4)
        self.click_1_y = pos[1] // (550 // 11)
        print(pos)
        print(self.click_1_x, self.click_1_y)
        print(self.Clicked)

    def IsClickTwoEqualToClickOne(self, pos):
        Clicked = False
        i = pos[0] // (300 // 4)
        self.j = pos[1] // (550 // 11)
        if i == self.click_1_x and self.j == self.click_1_y:
            return True

        return False

    def FindY2(self, InputX, InputY1):
        number_of_pieces_in_row = 0
        for char in Board[InputY1]:
            if char != "":
                number_of_pieces_in_row += 1
        return (InputY1 - number_of_pieces_in_row)

    def GetChildren(self, position):
        minimoves = []
        for row in self.Board:
            for element in row:
                y2 = self.FindY2(element, row)
                if self.LegalMove(element, row, y2):
                    Board2 = position
                    #checks if everythings legal
                    Board2 = self.MinimaxMove(element, row, y2, self.Board2)
                    minimoves.append(Board2)
        return minimoves

    def MinimaxMove(self, InputX, InputY1, InputY2, position):
        self.Board2[InputY2][InputX] == self.Board2[InputY1][InputX]
        self.Board2[InputY1][InputX] == ""

    def Minimax(self, position, depth, alpha, beta, maximisingPlayer):
        if depth == 0 or model.GameOver():
            return self.evaluate(position), position
            
#where is the point in here where the best move is stored so that I can pull it
        if maximisingPlayer:
            maxEval = -999
            for child in self.GetChildren(position):
                eval = self.Minimax(child, depth - 1, float ['-inf'], float ['inf'], False)[0]
                max_eval = max(max_eval, eval) #because it isnt self.max_eval, isnt maxeval just -999 every single time because max eval is local
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return [max_eval, position]
        
        else:
            minEval = 999
            for child in self.GetChildren(position):
                eval = self.Minimax(child, depth - 1, float ['-inf'], float ['inf'], True)[0]
                min_eval = min(min_eval, eval)
                beta = max(beta, eval)
                if beta <= alpha:
                    break
            return [min_eval, position]

    def PositionValue(self, position, score=0):
        for row in position:
            for char in row:
                if char == MaxPiece:
                    score += BoardScore[row][char]
                elif char == MinPiece:
                    score -= BoardScore[row][char]
        
        return score

    def ResetBoard(self):
        self.Board = [["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["B", "Y", "G", "R"], 
                      ["Y", "G", "R", "B"],
                      ["G", "R", "B", "Y"],
                      ["R", "B", "Y", "G"]]

    def evaluate(self, board, score=0):
        for row in Board:
            for char in row:
                if char == "R" or char== "G":
                    score += self.BoardScore[row]
                elif char == "B" or char== "Y":
                    score -= self.BoardScore[row]
    
    def ReturnBestMove(self):
        return self.Minimax(self.Board, depth - 1, float ['-inf'], float ['inf'], self.GetMaximisingPlayer)
        

                        

'''
eval:
    if you take the score of the scoring positions, reduce it -
    deduct the opposing pieces in the scoring zones from your own pieces in scoring zones - 
    the number of enemy pieces
'''