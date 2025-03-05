from copy import deepcopy
from UpCPU import MinimaxMove
from UpCPU import LegalCheck

class UpThrustBoard():
    
    def __init__(self, cpu):
        self.cpu = cpu
        self.positions = []
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
        """
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
        self.Board = [["", "", "", ""], 
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "Y", "", "R"],
                      ["B", "", "R", ""],
                      ["", "", "", "B"], 
                      ["", "G", "Y", ""],
                      ["R", "", "G", ""],
                      ["Y", "", "", ""],
                      ["G", "R", "B", "Y"],
                      ["", "B", "", "G"]]

        
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
        self.BoardScore = [120*self.k**2, 
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

    def CycleThruPlayerTurns(self):
        if self.playerCount == 4:
            self.game['turn'] = (self.game['turn']+1)%4
                
        if self.playerCount == 3:
            self.game['turn'] = (self.game['turn']+1)%3
        
        if self.playerCount == 2:
            self.game['turn'] = (self.game['turn']+1)%2
            print(f"game turn {self.game['turn']}")

        if self.playerCount == 1:
            self.game['turn'] = 1

    def CycleThruMiniTurns(self, turn):
        '''
        This function cycles the player turn *within* the minimax function so that it knows which player's pieces it should simulate moving
        '''
        return (turn+1)%self.playerCount

    def SkipPlayerTurn(self):
        if self.NoLegalMoves(self.Board, self.playerColour[self.game['turn']]):
            self.CycleThruPlayerTurns()

    """ 
        MOVE MANAGEMENT 
    """

    @MinimaxMove
    def MakeMove(self, board, InputX, InputY1, InputY2):
        pass
    
    @LegalCheck
    def LegalityCheck(self, playerCount, InputX, InputY1, InputY2, board):
        pass

    def RetractMove(self, InputX, InputY1, InputY2):
        self.Board[self.moves[9][0]][self.moves[9][1]] = self.Board[self.moves[9][2]][self.moves[9][1]] 
        self.Board[self.moves[9][2]][self.moves[9][1]] = ""    

    """ 
        LEGALITY MANAGEMENT
    """
    
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
                        if self.LegalityCheck(self.playerCount, locus, index, self.cpu.FindY2(index, board), board) == True:
                            pass
                        else:
                            number_of_legal_moves -= 1
            
        else:
            number_of_legal_moves = self.player_count_for_legal_moves[self.playerCount]
            for index, line in enumerate(board):
                for locus, char in enumerate(line):
                    if self.IsPlayersPiece(locus, index):
                        if self.LegalityCheck(self.playerCount, locus, index, self.cpu.FindY2(index, board), board) == True:
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
                self.why_two = self.cpu.FindY2(row, board)
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


            elif self.LegalityCheck(self.playerCount, self.col, self.row, self.why_two, board) and self.PieceIsPlayers(row, col):
                self.Board = self.MakeMove(self.Board, self.col, self.row, self.why_two)
                self.CycleThruPlayerTurns()
                self.selected_coor = None
                self.selected_piece = None
                
    def PieceIsPlayers(self, row, col):
        if self.playerCount == 4:
            return (row == self.why_two and col == self.col and (self.Board[self.row][self.col] == self.playerColour[self.game['turn']]))
        if self.playerCount == 3:
            return (row == self.why_two and col == self.col and (self.Board[self.row][self.col] == self.playerColour[self.game['turn']] or self.Board[self.row][self.col] == 'G'))
        if self.playerCount == 2:
            print(f"self.game['turn'] {self.game['turn']}")
            print(f"self.playerColour[self.game['turn']] {self.playerColour[self.game['turn']]}")
            return (row == self.why_two and col == self.col and (self.Board[self.row][self.col] == self.playerColour[self.game['turn']] or self.Board[self.row][self.col] == self.cpu.twoplayers[self.game['turn']]))
        print("1playergame")
        return True
            #self.twoplayers = ["G", "B"]

        

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

    def ViewFindY2(self, InputY1, board):
        number_of_pieces_in_row = 0
        
        for char in board[InputY1]:
            if char != "":
                number_of_pieces_in_row += 1
        print(f"no of piecesin row {number_of_pieces_in_row}")
        print(f"inputY1 {InputY1}")
        return InputY1-number_of_pieces_in_row
 
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
            print("4 plyaers")
            self.cpu.players = ["Y", "R", "B", "G"]
            self.cpu.twoplayers = [None, None, None, None] 
            self.free_colours = {}
            if self.AiPlayer == True:
                print("AI PLAYER TRUE")
                self.AiPlayers = {1:False, 2:False, 3:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 2:False, 3:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':False}

        if self.playerCount == 3:
            self.cpu.players = ["Y", "R", "B"]
            self.cpu.twoplayers = ["G", None, None]         
            self.GFree = True
            if self.AiPlayer == True:
                self.AiPlayers = {1:False, 2:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'B':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 2:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'B':False, 'Y':False}
        
        if self.playerCount == 2:
            self.cpu.players = ["Y", "R"]
            self.cpu.twoplayers = ["G", "B"]
            self.cpu.playercount = 2
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
            
    def PositionPrint(self, primary_list):
        with open("output.txt", "w") as file:
            for secondary_list in primary_list:
                # Extract the integer and corresponding board
                integer = secondary_list[0]
                board = secondary_list[1]
                
                # Write the integer to the file
                file.write(f"Integer: {integer}\n")
                file.write("Board:\n")
                
                # Write each inner list of the board on a new line
                for row in board:
                    file.write(f"{row}\n")
                
                # Add a blank line between different secondary lists for readability
                file.write("\n")        