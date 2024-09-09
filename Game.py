
class UpThrustBoard():
    
    def __init__(self):
        
        
        
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
        self.game = {
            'winner': None,
            'turn': 1
            }
        self.playerColour = {
            1: 'R',
            2: 'B',
            3: 'G',
            4: 'Y'
            }
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
    def CycleThruPlayerTurns(self):
        if self.playerCount == 4:
            if self.game['turn'] == 4:
                self.game['turn'] = 1
            else: 
                self.game['turn'] += 1
                
        if self.playerCount == 3:
            if self.game['turn'] == 3:
                self.game['turn'] = 1
            else: 
                self.game['turn'] += 1
        
        if self.playerCount == 2:
            self.game['turn'] = 3 - self.game['turn'] 

    def getBoard(self):
        return self.Board
    
    def numberOfPiecesInLane(self, InputX, InputY1, InputY2):
        counter = 4
        for char in self.Board[InputY1]:
            if char == "":
                counter -= 1
        return counter
    
    def matchingColours(self, char, InputX, InputY2):
        if InputY2 > 5:
            for element in self.Board[InputY2]:
                if element == char:
                    return False
                
        return True
        
    
    def isFurthestForwards(self, char, InputX, InputY1):
        a = 0
        for row in self.Board:
            for i in range(len(row)):
                if row[i] == char and i != InputX and i > InputY1:
                    a += 1
                else:
                    continue
                    
        if a == 3:
            return False  
        else:
            return True      
    
    #have something that checks the validity of a move (to be called upon later)
    def legalmove(self, InputX, InputY1, InputY2):
        if (self.Board[InputY2][InputX] == "" and 
            self.Board[InputY1][InputX] != "" and 
            self.isFurthestForwards(self.Board[InputY1][InputX], InputX, InputY1) and 
            self.numberOfPiecesInLane(InputX, InputY1, InputY2) == InputY1 - InputY2 and 
            self.matchingColours(self.Board[InputY1][InputX], InputX, InputY2) and 
            self.playerColour[self.game['turn']] == self.Board[InputY1][InputX]):
            
            print(2)
                
            
            return True
        else:
            return False


    #have something that makes moves 
    def MakeMove(self, InputX, InputY1, InputY2):
        if self.legalmove(InputX, InputY1, InputY2):
            
            print('MAKEMOVE')
            self.moves.append([InputY1, InputX, InputY2])
            self.moves.pop(0)
            print(self.moves)
            '''
            InputX -= 1
            InputY1 = 10 - InputY1
            InputY2 = 10 - InputY2
            '''
            self.Board[InputY2][InputX] = self.Board[InputY1][InputX]
            self.Board[InputY1][InputX] = ""

#have something that reverses moves
#have a list of moves, and draw upon the last move that was made
    def RetractMove(self, InputX, InputY1, InputY2):
        self.Board[self.moves[9][0]][self.moves[9][1]] = self.Board[self.moves[9][2]][self.moves[9][1]] 
        self.Board[self.moves[9][2]][self.moves[9][1]] = ""        
                
    def NoLegalMoves(self):
        number_of_legal_moves = 16
        for index, line in enumerate(self.Board):
            for locus, char in enumerate(line):
                if self.legalmove(locus, index, 4 - line.count("")) == True:
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
        
    def __repr__(self, Board):
        # return a nicely formatted string for displaying the board on the console
        s = ' '.join(map(str, range(Board.COLS))) + '\n'
        for row in self.__position[::-1]:
            outputrow = [Board.SYMBOLS[piece] for piece in row]
            s += ' '.join(outputrow) + '\n'
        return s
                
    def runGame(self, Board):
        run = True
        not_answered = True
        while run:
            not_answered = True
            #print current board state
            [print(row) for row in self.Board]
            #check if game is over
            if self.NoLegalMoves():
                break
            if self.TwoPiecesInScoringZone():
                break
           
            while not_answered:
                #take inputs
                InputX = int(input('X Input: '))
                InputY1 = int(input('Y1 Input: '))
                InputY2 = int(input('Y2 Input: '))
                #calculate if the move is legal and hence make the move
                if self.legalmove(InputX, InputY1, InputY2):
                    print(1)
                    self.MakeMove(InputX, InputY1, InputY2)
                    not_answered = False
            #makes it the next players turn
            self.CycleThruPlayerTurns()

game = UpThrustBoard()
game.runGame(game.Board)
            