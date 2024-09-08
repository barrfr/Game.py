
class UpThrustBoard():
    
    def __init__(self, Board, row, coloumn, playerCount):
        
        self.row = row
        self.coloumn = coloumn
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
        self.Board1 = [["", "", "", ""], 
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
    def sideToMove(self):
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
    
    def isFurthestForwads(self, char, InputX, InputY1):
        a = 0
        for row in self.Board1:
            for i in range(len(row)):
                if row[i] == char and i != InputX and row > InputY1:
                    a += 1
                else:
                    continue
                    
        if a == 3:
            return False  
        else:
            return True      
    
    #have something that checks the validity of a move (to be called upon later)
    def legalmove(self, InputX, InputY1, InputY2):
        if self.Board1[InputY2][InputX] == "" and self.Board1[InputY1][InputX] != "" and self.isFurthestForwards(self.Board1[InputY1][InputX], InputX, InputY1) and self.playerColour[self.game['turn']] == self.Board1[InputY1][InputX]:
                return True
        else:
            return False


    #have something that makes moves 
    def MakeMove(self, InputX, InputY1, InputY2):
        if self.legalmove(InputX, InputY1, InputY2):
            self.moves.append([InputY1, InputX, InputY2])
            self.moves.pop(0)
            InputX -= 1
            InputY1 = 10 - InputY1
            InputY2 = 10 - InputY2
            self.Board1[InputY2][InputX] = self.Board1[InputY1][InputX]
            self.Board1[InputY1][InputX] = ""

#have something that reverses moves
#have a list of moves, and draw upon the last move that was made
    def RetractMove(self, InputX, InputY1, InputY2):
        self.Board1[self.moves[9][0]][self.moves[9][1]] = self.Board1[self.moves[9][2]][self.moves[9][1]] 
        self.Board1[self.moves[9][2]][self.moves[9][1]] = ""
        


#have something that calculates the scores at the end of the game
    
#and a __repr__
 def __repr__(self):
        # return a nicely formatted string for displaying the board on the console
        s = ' '.join(map(str, range(Board.COLS))) + '\n'
        for row in self.__position[::-1]:
            outputrow = [Board.SYMBOLS[piece] for piece in row]
            s += ' '.join(outputrow) + '\n'
        return s        