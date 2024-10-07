from copy import deepcopy

class UpThrustBoard():
    
    def __init__(self):
        self.minimax_pos = []
        self.minimax_turn = 1
        self.ListOfMoves = [] #2D list that holds all the moves minimax has made do they can be called upon later
        self.maxScore = 0
        self.minScore = 0
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
        self.AiPlayers = {1:False, 2:False, 3:False, 0:True}
        self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':True}


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

        self.BoardScore = [140, 
                      120,
                      100, 
                      80,
                      60, 
                      40,
                      20, 
                      0, 
                      -10,
                      -20,
                      -20]
    def CycleThruPlayerTurns(self):
        if self.playerCount == 4:
            self.game['turn'] = (self.game['turn']+1)%4
            self.minimax_turn = self.game['turn']
            print("player turn: ", self.game['turn'])
                
        if self.playerCount == 3:
            self.game['turn'] = (self.game['turn']+1)%3
            self.minimax_turn = self.game['turn']
        
        if self.playerCount == 2:
            self.game['turn'] = (self.game['turn']+1)%2
            self.minimax_turn = self.game['turn']

    def GetMaximisingPlayer(self):
        if self.game['turn']%2 == 0: #if turn is an even number
            return True

        return False
        
    def GetBoard(self):
        return self.Board
    
    def NumberOfPiecesInLane(self, InputX, InputY1, InputY2, board):
        counter = 4
        for char in board[InputY1]:
            if char == "":
                counter -= 1
        return counter
    
    def MatchingColours(self, char, InputX, InputY2, board):
        if InputY2 > 5:
            for element in board[InputY2]:
                if element == char:
                    return False
                
        return True
        
    def FarForwards(self, char, InputX, InputY1, InputY2, board):
        if (InputY1 - InputY2 == 1) & (self.IsFurthestForwards(char, InputX, InputY1, board)):
            return False
        return True

    def IsFurthestForwards(self, char, InputX, InputY1, board, a=0):
        for index, row in enumerate(board):
            for i in range(len(row)):
                if row[i] == char and i != InputX and index >= InputY1:
                    a += 1                 
        if a == 3:
            return True
        else:
            
            return False
                
    #have something that checks the validity of a move (to be called upon later)
    def LegalMove(self, InputX, InputY1, InputY2, board):
        
        if (board[InputY2][InputX] == "" and 
            board[InputY1][InputX] != "" and 
            self.FarForwards(board[InputY1][InputX], InputX, InputY1, InputY2, board) and 
            self.NumberOfPiecesInLane(InputX, InputY1, InputY2, board) == InputY1 - InputY2 and 
            self.MatchingColours(board[InputY1][InputX], InputX, InputY2, board) and 
            (self.playerColour[self.game['turn']] == board[InputY1][InputX] or self.playerColour[self.minimax_turn] == board[InputY1][InputX])):
            return True
        else:
            return False


    #have something that makes moves 
    def MakeMove(self, InputX, InputY1, InputY2):
        if self.LegalMove(InputX, InputY1, InputY2, self.Board):
            
            
            self.moves.append([InputY1, InputX, InputY2])
            self.moves.pop(0)
            
            '''
            InputX -= 1
            InputY1 = 10 - InputY1
            InputY2 = 10 - InputY2
            '''
            self.Board[InputY2][InputX] = self.Board[InputY1][InputX]
            self.Board[InputY1][InputX] = ""
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
                if self.LegalMove(locus, index, 4 - line.count(""), self.Board) == True:
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
        self.Clicked = True
        self.click_1_x = pos[0] // (300 // 4)
        self.click_1_y = pos[1] // (550 // 11)

    def IsClickTwoEqualToClickOne(self, pos):
        Clicked = False
        i = pos[0] // (300 // 4)
        self.j = pos[1] // (550 // 11)
        if i == self.click_1_x and self.j == self.click_1_y:
            return True

        return False

    def FindY2(self, InputY1, board):
        number_of_pieces_in_row = 0
        for char in board[InputY1]:
            if char != "":
                number_of_pieces_in_row += 1
        return (InputY1 - number_of_pieces_in_row)

    def GetChildren(self, position):
        print("getting children")
        minimoves = []
        for index_row, row in enumerate(position):
            for index_element, element in enumerate(row):
                print("minimax turn: ", self.minimax_turn)
                if element == self.playerColour[self.minimax_turn]:
                    print("element == player colour", self.playerColour[self.minimax_turn])
                    y2 = self.FindY2(index_row, position)
                    if self.LegalMove(index_element, index_row, y2, position):
                        print("move is legal")
                        Board2 = deepcopy(position) 
                        Board2 = self.MinimaxMove(index_element, index_row, y2, Board2)
                        minimoves.append(Board2)
        print("minimoves: ", minimoves)
        return minimoves

    def MinimaxMove(self, InputX, InputY1, InputY2, Board2):
        Board2[InputY2][InputX] = Board2[InputY1][InputX]
        Board2[InputY1][InputX] = ""
        return Board2

    def Minimax(self, position, depth, alpha, beta, maximisingPlayer):
        print("minimax has been called")
        print("position: ", position)
        #print("maximising player: ", maximisingPlayer)
        print("minimax depth: ", depth)
        if depth == 0 or self.game['GAMEOVER']:
        #    print("HIT DEPTH 0")
            return self.evaluate(position), position
        if maximisingPlayer:
            max_eval = -999
            for child in self.GetChildren(position):
                print("child: ", child)
                minimax_eval, minimax_pos = self.Minimax(child, depth - 1, -999, 999, self.MaximisingPlayer())
                self.minimax_pos.append(minimax_pos)
                print("minimax_pos: ", minimax_pos)
                max_eval = max(max_eval, minimax_eval)
                alpha = max(alpha, minimax_eval)
                if beta <= alpha:
                    break
            return max_eval, position
        
        else:
            min_eval = 999
            for child in self.GetChildren(position):
                minimax_eval, minimax_pos = self.Minimax(child, depth - 1, -999, 999, self.MaximisingPlayer())
                self.minimax_pos.append(minimax_pos)
                print("child: ", child)
                min_eval = min(min_eval, minimax_eval)
                beta = max(beta, minimax_eval)
                if beta <= alpha:
                    break
            return min_eval, position

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
        for index_row, row in enumerate(board):
            for index_char, char in enumerate(row):
                if char != "" and char != "Y":
                    score -= self.BoardScore[index_row]
                elif char == "Y":
                    score += self.BoardScore[index_row]
        return score

    def MaximisingPlayer(self):

        if self.minimax_turn == 4:
            self.minimax_turn = (self.minimax_turn+1)%4
            return True

        self.minimax_turn = (self.minimax_turn+1)%4
        return False


    def PlayerIsHuman(self):
        if self.ColourAiPlayers[self.playerColour[self.game['turn']]] == False: #if current player is AI
            print("Player is AI: ", self.ColourAiPlayers[self.playerColour[self.game['turn']]])
            return True
        return False
        
        

                        

'''
eval:
    if you take the score of the scoring positions, reduce it -
    deduct the opposing pieces in the scoring zones from your own pieces in scoring zones - 
    the number of enemy pieces
'''