from copy import deepcopy
from UpCPU import MinimaxMove
from UpCPU import LegalCheck

class UpThrustBoard():
    
    def __init__(self, cpu):
        """
        Initialisation of the UpThrustBoard class

        Args:
        cpu = instance of the Minimax class from UPCPU.py instance

        List of Variables:
        self.cpu (object): Minimax class from UpCPU.py instance
        self.player_count_for_legal_moves (dictionary): a dictionary that represents how many legal moves each player could have for a given playercount
        self.AiPlayer (bool): indicates whether the user has turned the CPU player on or off
        self.col (real): used to store the coloumn that the users click was made in
        self.row (real): used to store the row that the users click was made in
        self.why_two (real): used to store the second Y value of a click
        self.selected_piece (string): saves the type of piece that was clicked on
        self.selected_coor (coordinate): saves the coordinate of a click
        self.Clicked (bool): stores the boolean value of a click
        self.playerCount (int):stores active player count
        self.game (dictionary): stores relevant game information (i.e. gameover, current turn)
        self.playerColour (dictionary): stores the relation between a colour and the turn number it can move on
        self.AiPlayers (dictionary): stores the relation between the player number and whether they are a CPU opponent using a boolean value
        self.ColourAiPlayers (dictionary): stores the relation between the player colours and whether they are a CPU opponent using a boolean value
        self.Board (list): stores the primary board used in the representation of the UI
        self.final_score (list): a list that has the score of each row of the board according to the rulebook
        """

        self.cpu = cpu
        self.player_count_for_legal_moves = {1:16, 2:8, 3:8, 4:4}
        self.free_colours = []
        self.AiPlayer = False
        self.col = 0
        self.row = 0
        self.why_two = 0
        self.selected_piece = None
        self.selected_coor = None
        self.Clicked = False
        self.click_1_x = 0
        self.click_1_y = 0
        self.playerCount = 4
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

        self.Board = [["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["", "", "", ""],
                      ["", "", "", ""], 
                      ["B", "R", "G", "Y"], 
                      ["R", "G", "Y", "B"],
                      ["G", "Y", "B", "R"],
                      ["Y", "B", "R", "G"]]

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

    """ 
        TURN MANAGEMENT
    """

    #Goes onto the next turn by using (turn+1)%playercount
    def CycleThruPlayerTurns(self):
        if self.playerCount == 4:
            self.game['turn'] = (self.game['turn']+1)%4
                
        if self.playerCount == 3:
            self.game['turn'] = (self.game['turn']+1)%3
        
        if self.playerCount == 2:
            self.game['turn'] = (self.game['turn']+1)%2

        if self.playerCount == 1:
            self.game['turn'] = 1

    """ 
        MOVE & LEGALITY MANAGEMENT 
    """

    @MinimaxMove
    def MakeMove(self, board, InputX, InputY1, InputY2):
        pass
    
    @LegalCheck
    def LegalityCheck(self, playerCount, InputX, InputY1, InputY2, board):
        pass   

    def PlayerIsHuman(self):
        #if current player is AI
        if self.ColourAiPlayers[self.playerColour[self.game['turn']]] == False:
            return True
        return False 

    def IsPlayersPiece(self, InputX, InputY1):
        # checks if a piece at the given input is the same colour as the current player turn
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
        #checks entire board for if there are any legal moves remaining, for each piece that cant move, deduct from 16, if it never reaches 0, that measn that theres n available move, return false, game over

        number_of_legal_moves = 16

        #function can check the entire board for pieces of all colours if piece is "any"
        if piece == "any":
            for index, line in enumerate(board):
                for locus, char in enumerate(line):
                    if char != "":
                        if self.LegalityCheck(self.playerCount, locus, index, self.cpu.FindY2(index, board), board) == True:
                            pass
                        else:
                            number_of_legal_moves -= 1

        #if piece isnt "any", it will check for a specific piece  
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
        return False

    """ 
        CLICKING MANAGEMENT
    """

    def Clicking(self, board, posx, posy):
        """
        an initial if statement checks if a click has already been made (if this were true self.selected_piece != None).
        if there is a piece at the point of the click, then save the values of the click to 'self.' variables so that they can be accessed by UpView and other functions.
        if there is no piece simply ignore the click

        if there is a piece already selected,
        then check to see if the click was made in the same place as the selected piece [if row == self.row and col == self.col:]
        and if so, reset the necesary variables, effectively deselecting the piece
        if not, then check the legality of moving the piece at the original click, to the most recent click
        following this, make the move, cycle the player turn, and change the necesary variables

        Args:
        board (list): current board position
        posx (decimal): the x coordinate of the click designated by pygame
        posy (decimal): the y coordinate of the click designated by pygame

        List of variables:
        row (int): the board index of the x coordinate argument
        col (int): the board index of the y coordinate argument
        """
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
        """
        checks whether the piece at the index presented by the arguments, is of the same player as the current turn. Each playercount uses a different checking method
        4 players: (is the y index of the piece the same as the second Y index of the original click made) and (is the x index of the piece the same as the second Y index of the original click made) and is the piece at the original index the same as the current players turn
        3 players: in addition to the 4 player rules, the piece can also be 'G' as well as the current players piece
        2 players: in addition to the 4 player rules, the piece can also be the second colour that a given player commands (red also commands blue, and yellow also commands green)
        there is no need to check this for a single player game because all pieces are the player's
        
        Args:
        col (int): x board index of the piece
        row (int): y board index of the piece
        """
        if self.playerCount == 4:
            return (row == self.why_two and col == self.col and (self.Board[self.row][self.col] == self.playerColour[self.game['turn']]))
        if self.playerCount == 3:
            return (row == self.why_two and col == self.col and (self.Board[self.row][self.col] == self.playerColour[self.game['turn']] or self.Board[self.row][self.col] == 'G'))
        if self.playerCount == 2:
            return (row == self.why_two and col == self.col and (self.Board[self.row][self.col] == self.playerColour[self.game['turn']] or self.Board[self.row][self.col] == self.cpu.twoplayers[self.game['turn']]))
        return True
     
    """ 
        MISC
    """ 

    def ResetBoard(self):
        #used by the controller to reset the board to its original starting position
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
        #checks the board for certain coloured pieces given on the 'colour' argument
        # it returns these in a list that can be digested by the countscores function
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

    #creates a list of scores for each player in the game, which is then used by UpView.py
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

    #used by the controller to start a game 
    #important as different games have different variables (i.e. playercount or AI player)
    #when attempting to play multiple games consecutively, it is important as it wipes variables back to their default state
    def GameStartLogic(self):
        self.col = 0
        self.row = 0
        self.why_two = 0
        self.selected_piece = None
        self.selected_coor = None
        self.Clicked = False
        self.click_1_x = 0
        self.click_1_y = 0
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
            self.cpu.players = ["Y", "R", "B", "G"]
            self.cpu.twoplayers = [None, None, None, None] 
            if self.AiPlayer == True:
                self.AiPlayers = {1:False, 2:False, 3:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 2:False, 3:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'B':False, 'G':False, 'Y':False}

        if self.playerCount == 3:
            self.cpu.players = ["Y", "R", "B"]
            self.cpu.twoplayers = ["G", None, None]         
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
            if self.AiPlayer == True:
                self.AiPlayers = {1:False, 0:True}
                self.ColourAiPlayers = {'R':False, 'Y':True}

            else:
                self.AiPlayers = {1:False, 0:False}
                self.ColourAiPlayers = {'R':False, 'Y':False}

        if self.playerCount == 1:
            self.AiPlayers = {1:False}
            self.ColourAiPlayers = {'R':False}    