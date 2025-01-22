from copy import deepcopy

class UpThrustBoard():
    
    def __init__(self):
        self.player_count_for_legal_moves = {1:16, 2:8, 3:8, 4:4}
        self.GFree = False
        self.TFree = False
        self.free_colours = []
        self.AiPlayer = False
        self.col = 0
        self.row = 0
        self.why_two = 0
        self.selected_piece = None
        self.selected_coor = None
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
            'END SCREEN' : False,
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
        """
        self.Board = [["Y", "G", "R", "B"], 
                      ["B", "R", "G", "Y"], 
                      ["G", "B", "Y", "R"],
                      ["", "", "", ""],
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "Y", "B", ""],
                      ["", "", "", ""],
                      ["R", "", "", "G"],
                      ["", "", "", ""],
                      ["", "", "", ""]]
        """

        
        self.final_score = [60,
                            40,
                            30,
                            20,
                            10,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0]
        self.k = 2
        self.BoardScore = [100*self.k**2, 
                      81*self.k**2,
                      64*self.k**2, 
                      49*self.k**2,
                      36*self.k**2, 
                      25*self.k**2,
                      16*self.k**2, 
                      9*self.k**2, 
                      4*self.k**2,
                      self.k**2,
                      0]

    """ 
        TURN MANAGEMENT
    """
    def CycleBackwardsPlayerTurns(self):
        if self.playerCount == 4:
            self.game['turn'] = (self.game['turn']-1)%4
                
        if self.playerCount == 3:
            self.game['turn'] = (self.game['turn']-1)%3
        
        if self.playerCount == 2:
            self.game['turn'] = (self.game['turn']-1)%2
        
        if self.playerCount == 1:
            self.game['turn'] = 1

    def CycleThruPlayerTurns(self):
        if self.playerCount == 4:
            self.game['turn'] = (self.game['turn']+1)%4
                
        if self.playerCount == 3:
            self.game['turn'] = (self.game['turn']+1)%3
        
        if self.playerCount == 2:
            self.game['turn'] = (self.game['turn']+1)%2

        if self.playerCount == 1:
            self.game['turn'] = 1

    def CycleThruMiniTurns(self, turn):
        '''
        This function cycles the player turn *within* the minimax function so that it knows which player's pieces it should simulate moving
        '''
        if self.playerCount == 4:
            turn = (turn+1)%4
                
        if self.playerCount == 3:
            turn = (turn+1)%3

        if self.playerCount == 2:
            turn = (turn+1)%2

        if self.playerCount == 1:
            turn = 1
        
        return turn

    def SkipPlayerTurn(self):
        if self.NoLegalMoves(self.Board, self.playerColour[self.game['turn']]):
            self.CycleThruPlayerTurns()

    """ 
        MOVE MANAGEMENT 
    """

    def MakeMove(self, InputX, InputY1, InputY2):
        if self.LegalMove(InputX, InputY1, InputY2, self.Board) and self.IsPlayersPiece(InputX, InputY1):
            '''
            self.moves is a list of the last 10 moves, and it allows the player to take a move back 10 times
            its not very good, as taking a move back in a 4 player game is strange, but I wrote the code ages ago and am keeping it around just in case
            '''
            
            self.moves.append([InputY1, InputX, InputY2])
            self.moves.pop(0)
            
            #makes the element at the start coordinates equal an empty tile, and puts the letter of the piece into the end coordinates
            self.Board[InputY2][InputX] = self.Board[InputY1][InputX]
            self.Board[InputY1][InputX] = ""
            self.CycleThruPlayerTurns()

    def RetractMove(self, InputX, InputY1, InputY2):
        self.Board[self.moves[9][0]][self.moves[9][1]] = self.Board[self.moves[9][2]][self.moves[9][1]] 
        self.Board[self.moves[9][2]][self.moves[9][1]] = ""    

    """ 
        LEGALITY MANAGEMENT
    """
    def LegalMove(self, InputX, InputY1, InputY2, board):
        
        """
        1. A piece must move exactly as how many space up as there are pieces in the horisontal row from which it departs. (Thus, if there are two pieces in a row, either piece may move up exactly two spaces, after one piece is moved, the other may only move up one space since it has become the solitary piece in the row)
        2. Only one piece may occupy a space, pieces may jump over other pieces, as long as they land on empty spaces
        3. The most advanced piece of a colour may not make a single space move. (Therefore a piece that is alone in a row cannot move if the other three pieces of the same colour are below it on the board).
        4. On any of the bottom six rows of the board, (the non scoring rows) two pieces of the same colour may NEVER be in the same row at the time. This restriction does not apply to the five scoring rows.
        """

        if (board[InputY2][InputX] == "" and 
            board[InputY1][InputX] != "" and 
            not self.FurthestForwardsAndMovingOnePlace(board[InputY1][InputX], InputX, InputY1, InputY2, board) and 
            self.NumberOfPiecesInLane(InputY1, board) == InputY1 - InputY2 and 
            self.MatchingColours(board[InputY1][InputX], InputX, InputY2, board)):

            return True
        else:
            return False


    
    def FurthestForwardsAndMovingOnePlace(self, char, InputX, InputY1, InputY2, board):
       #if (    moves one tile    ) and (     is the furthest piece forwads of its colour     )      
        if (InputY1 - InputY2 == 1) and (self.IsFurthestForwards(char, InputX, InputY1, board)):

            return True
        return False

    def IsFurthestForwards(self, char, InputX, InputY1, board, a=0):
        ''' 
        scans board for pieces of the same colour behind the current piece, if there are 3, return True
        '''
        for index, row in enumerate(board):
            for index2 in range(len(row)):
                if row[index2] == char and index2 != InputX and index > InputY1:
                    a += 1                 
        if a == 3:
            return True
        else:
            return False

    def NumberOfPiecesInLane(self, InputY1, board):
        counter = 4
        for char in board[InputY1]:
            if char == "":
                counter -= 1
        return counter

    def MatchingColours(self, char, InputX, InputY2, board):
        if InputY2 > 4 or self.playerCount == 1: 
            for element in board[InputY2]:
                if element == char:
                    return False
                
        return True

    def IsPlayersPiece(self, InputX, InputY1):
        if self.playerColour[self.game['turn']] == self.Board[InputY1][InputX]:
            return True
        elif (self.playerCount == 3) and self.Board[InputY1][InputX] == 'G':
            return True
        elif (self.playerCount == 2) and ((self.Board[InputY1][InputX] == 'G' and self.game['turn'] == 0) or (self.Board[InputY1][InputX] == 'B' and self.game['turn'] == 1)):
            return True
        elif (self.playerCount == 1) and (self.Board[InputY1][InputX] == 'G' or self.Board[InputY1][InputX] == 'B' or self.Board[InputY1][InputX] == 'Y'):
            return True
        else:
            return False
    

    def NoLegalMoves(self, board, piece):
        ''' 
        checks entire board for if there are any legal moves remaining, for each piece that cant move, deduct from 16, if it never reaches 0, that measn that theres n available move, return false, game over
        '''
        number_of_legal_moves = 16
        if piece == "any":
            for index, line in enumerate(board):
                for locus, char in enumerate(line):
                    if char != "":
                        if self.LegalMove(locus, index, self.FindY2(index, board), board) == True:
                            pass
                        else:
                            number_of_legal_moves -= 1
            
        else:
            number_of_legal_moves = self.player_count_for_legal_moves[self.playerCount]
            for index, line in enumerate(board):
                for locus, char in enumerate(line):
                    if self.IsPlayersPiece(locus, index):
                        if self.LegalMove(locus, index, self.FindY2(index, board), board) == True:
                            pass
                        else:
                            number_of_legal_moves -= 1
                    
        if number_of_legal_moves == 0:
            return True
        else:
            return False

    def TwoPiecesInScoringZone(self, board):
        ''' 
        a rule where if there are two pieces in the non-scoring zone, return True, game over
        '''
        pieces = 0
        for number, line in enumerate(board):
            if number > 4:
                for char in line:
                    if char != "":
                        pieces += 1
        if pieces < 3:
            return True
        else:
            return False

    """ 
        CLICKING MANAGEMENT
    """

    def Clicking(self, board, posx, posy):
        row = posy // (550 // 11)
        col = posx // (300 // 4)
        if self.selected_piece == None:
            if board[row][col] != "":
                self.col = posx // (300 // 4)
                self.row = posy // (550 // 11)
                self.why_two = self.FindY2(row, board)
                self.selected_piece = board[self.row][self.col]
                self.selected_coor = (self.row, self.col)
            else:
                pass
        else:
            
        # If user clicks the same piece again, deselect it
            if row == self.row and col == self.col:
                self.selected_piece = None
                self.row = None
                self.col = None
                self.selected_coor = None


            elif self.LegalMove(self.col, self.row, self.why_two, board) and row == self.why_two and col == self.col:
                self.MakeMove(self.col, self.row, self.why_two)
                self.selected_coor = None
                self.selected_piece = None
                


    def ClickOne(self, pos):
        ''' 
        splits board up into tiles and makes the click variables equal to whichever tile the click occured
        ''' 
        self.Clicked = True
        self.click_1_x = pos[0] // (300 // 4)
        self.click_1_y = pos[1] // (550 // 11)

    def IsClickTwoEqualToClickOne(self, pos):
        ''' 
        if the second click is equal to the first, return True and deselect the piece like on chess.com or something
        ''' 
        Clicked = False
        i = pos[0] // (300 // 4)
        self.j = pos[1] // (550 // 11)
        if i == self.click_1_x and self.j == self.click_1_y:
            return True

        return False

    """ 
        MINIMAX FUNCTIONS
    """

    def Minimax(self, position, depth, maximisingPlayer, currentTurn, alpha, beta, gameover):
        #print(f"{beta} {alpha}")
        if depth == 0 or gameover:
            #print(f"depth 0 = {depth}, gameover {gameover}")
            return self.evaluate(position), position
        if maximisingPlayer:
            max_eval = -999
            child_positions = self.GetChildren(position, currentTurn)
            if child_positions == []:
                minimax_eval, minimax_pos = self.Minimax(position, depth - 1, self.maximisingPlayer(currentTurn), self.CycleThruMiniTurns(currentTurn), alpha, beta, False)

            for child in child_positions:

                if child[-1] == "gameover":
                    print("gameover")
                    minimax_eval, minimax_pos = self.Minimax(position, depth - 1, self.maximisingPlayer(currentTurn), self.CycleThruMiniTurns(currentTurn), alpha, beta, True)

                minimax_eval, minimax_pos = 0, []
                minimax_eval, minimax_pos = self.Minimax(child[0], depth - 1, self.maximisingPlayer(currentTurn), self.CycleThruMiniTurns(currentTurn), alpha, beta, False)
                self.MinimaxPositionAppend(position, minimax_pos)
                #print("ONE ", alpha, minimax_eval)
                max_eval = max(max_eval, minimax_eval)
                #print(f"two- {alpha} - {max(max_eval, minimax_eval)}")
                alpha = max(alpha, minimax_eval)
                if beta <= alpha:
                    #print("beta < = alpha")
                    break
            return max_eval, position
        
        else:
            min_eval = 999
            child_positions = self.GetChildren(position, currentTurn)
            if child_positions == []:
                minimax_eval, minimax_pos = self.Minimax(position, depth - 1, self.maximisingPlayer(currentTurn), self.CycleThruMiniTurns(currentTurn), alpha, beta, False)
            for child in child_positions:

                if child[-1] == "gameover":
                    print("gameover")
                    minimax_eval, minimax_pos = self.Minimax(position, depth - 1, self.maximisingPlayer(currentTurn), self.CycleThruMiniTurns(currentTurn), alpha, beta, True)

                minimax_eval, minimax_pos = self.Minimax(child[0], depth - 1, self.maximisingPlayer(currentTurn), self.CycleThruMiniTurns(currentTurn), alpha, beta, False)
                self.MinimaxPositionAppend(position, minimax_pos)
                min_eval = min(min_eval, minimax_eval)
                beta = min(beta, minimax_eval)
                if beta <= alpha:
                    break
                    #print("beta < = alpha")
            return min_eval, position   

    def MinimaxPositionAppend(self, pos1, pos2):
        for row_index, row in enumerate(pos1):
                for coloumn_index, coloumn in enumerate(pos1[row_index]):

                    if pos1[row_index][coloumn_index] != pos2[row_index][coloumn_index]:

                        if pos1[row_index][coloumn_index] == "":
                            InputY2, InputX = row_index, coloumn_index

                        elif pos1[row_index][coloumn_index] != "":
                            InputY1 = row_index

        if self.LegalMove(InputX, InputY1, InputY2, pos1) == True:
            self.minimax_pos.append(pos2)
            


    def GetChildren(self, position, currentTurn):
        minimoves = []
        for index_row, row in enumerate(position):
            for index_element, element in enumerate(row):
                if self.IsPlayersPiece(index_element, index_row):
                    y2 = self.FindY2(index_row, position)
                    if self.LegalMove(index_element, index_row, y2, position):
                        Board2 = deepcopy(position) 
                        Board2 = self.MinimaxMove(index_element, index_row, y2, Board2)   
                        if self.NoLegalMoves(Board2, "any") or self.TwoPiecesInScoringZone(Board2):
                            print("gameover")
                            minimoves.append([Board2, "gameover"])
                        else: 
                            minimoves.append([Board2])                    

        return minimoves

    def FindY2(self, InputY1, board):
        number_of_pieces_in_row = 0
        
        for char in board[InputY1]:
            if char != "":
                number_of_pieces_in_row += 1
        
        return (max(InputY1 - number_of_pieces_in_row, 0))

    def ViewFindY2(self, InputY1, board):
        number_of_pieces_in_row = 0
        
        for char in board[InputY1]:
            if char != "":
                number_of_pieces_in_row += 1
        
        return (max(number_of_pieces_in_row, 0))

    def MinimaxMove(self, InputX, InputY1, InputY2, Board2):
        Board2[InputY2][InputX] = Board2[InputY1][InputX]
        Board2[InputY1][InputX] = ""
        return Board2

    def GetMaximisingPlayer(self):
        if self.game['turn']%2 == 0: #if turn is an even number
            return True

        return False
        
    def maximisingPlayer(self, prev_turn):

        if self.playerCount == 4:
            if prev_turn == 3:
                return True

        if self.playerCount == 3:
            if prev_turn == 2:
                return True

        if self.playerCount == 2:
            if prev_turn == 1:
                return True

        return False

    def evaluate(self, board, score=0):
        for index_row, row in enumerate(board):
            for index_char, char in enumerate(row):
                if char in self.ColourAiPlayers and char != self.playerColour[self.game['turn']]:
                    score -= self.BoardScore[index_row] - self.final_score[index_row]
                elif char == self.playerColour[self.game['turn']]:
                    score += self.BoardScore[index_row] + self.final_score[index_row]
        return score

#self.ColourAiPlayers[self.playerColour[self.game['turn']]] == True when it shouldnt 
    def PlayerIsHuman(self):
        if self.ColourAiPlayers[self.playerColour[self.game['turn']]] == False: #if current player is AI
            return True
        return False    

    """ 
        MISC
    """ 

    def GetBoard(self):
        return self.Board

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

    def CountColour(self, colour):
        score = 0
        if colour == 'T1':
            for loc, i in enumerate(self.Board):
                for j, char in enumerate(i):
                    if char == 'R' or char == 'B':
                        score += self.final_score[loc]
            return [score, 'R']

        elif colour == 'T2':
            for loc, i in enumerate(self.Board):
                for j, char in enumerate(i):
                    if char == 'G' or char == 'Y':
                        score += self.final_score[loc]
            return [score, 'Y']
        
        elif self.playerCount == 1:
            for loc, i in enumerate(self.Board):
                for j, char in enumerate(i):
                    if char != "":
                        score += self.final_score[loc]
            return [score, 'Score']

        for loc, i in enumerate(self.Board):
            for j, char in enumerate(i):
                if char == colour:
                    score += self.final_score[loc]

        return [score, colour]

    def CountScores(self):
        scores = []
        for i in self.ColourAiPlayers:

            if i == 'R' and self.playerCount == 2:
                scores.append(self.CountColour('T1'))
            elif i == 'Y' and self.playerCount == 2:
                scores.append(self.CountColour('T2'))
            else:
                scores.append(self.CountColour(i))

        return scores



    def GameStartLogic(self):
        self.GFree = False
        self.TFree = False
        self.col = 0
        self.row = 0
        self.why_two = 0
        self.selected_piece = None
        self.selected_coor = None
        self.minimax_pos = []
        self.Clicked = False
        self.click_1_x = 0
        self.click_1_y = 0
        self.j = 0
        self.minimoves = []
        self.game = {
            'GAMEOVER' : False,
            'END SCREEN' : False,
            'winner': None,
            'turn': 1
            }
        self.playerColour = {
            1: 'R',
            2: 'B',
            3: 'G',
            0: 'Y'
            }

        self.AiPlayers = {1:False, 2:False, 3:False, 0:True}
        self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':True}

        lst = ["R", "B", "G", "Y"]
        row = ['' for i in range(4)]
        self.board = [row for i in range(7)]
        self.board += [lst[:i] + lst[i:] for i in range(4)]

        if self.playerCount == 4:
            self.free_colours = {}
            if self.AiPlayer == True:
                self.AiPlayers = {1:False, 2:False, 3:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 2:False, 3:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':False}

        if self.playerCount == 3:
            self.GFree = True
            if self.AiPlayer == True:
                self.AiPlayers = {1:False, 2:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'B':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 2:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'B':False, 'Y':False}
        
        if self.playerCount == 2:
            self.TFree = True
            if self.AiPlayer == True:
                self.AiPlayers = {1:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'Y':False}

        if self.playerCount == 1:
            self.free_colours = {1:'B', 1:'G', 1:'Y'}
            self.AiPlayers = {1:False}
            self.ColourAiPlayers = {'R':False}

            
        
      