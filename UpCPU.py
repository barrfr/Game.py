from copy import deepcopy
class Minimax():
    def __init__(self, players):
        with open("output.txt", "w") as f:
            f.write("")
        with open("outputChildren.txt", "w") as g:
            g.write("")
        with open("outputReturns.txt", "w") as h:
            h.write("")
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
        print(f"players {self.players}")
        print(f"len players {len(players)}")
        self.playercount = len(players)

    #@property
    #def playercount(self):
    #    return self.playercount
    
    #@playercount.setter
    #def playercount(self, count):
    #    self.playercount = count

    def Minimax(self, position, depth, maximisingPlayer, currentTurn, alpha, beta):
        print(f"minimax started DEPTH: {depth}")
        print(f"players {self.players}")
        self.PrintMinimax(depth, alpha, beta, currentTurn, maximisingPlayer, position, self.EvaluatePos(position))
        if depth == 0 or self.GameOver(position):
            print("depth == 0")
            return self.EvaluatePos(position), position
        print("1")
        if maximisingPlayer:
            max_eval = -999
            print("just before calculating children")
            children =  self.ChildPositions(position, currentTurn)
            print("after calcing children")
            if not children:
                print("if children empty, return")
                return self.EvaluatePos(position), position
            print("2")
            for child in children:
                print("for child in children")
                evaluation, z = self.Minimax(child, depth-1, False, self.cycleTurn(currentTurn), alpha, beta)
                print("evaluation, z =")
                
                if max_eval != max(max_eval, evaluation):
                    best_move = child
                    max_eval = max(max_eval, evaluation)
                
                print("after2")
                alpha = max(alpha, evaluation)
                print("after3")
                if beta <= alpha:
                    print("after4")
                    break
            self.PrintReturning(depth, alpha, beta, max_eval, evaluation)
            return max_eval, best_move

        else:
            print("3")
            min_eval = 999
            print("child abt tpo be calced min")
            children =  self.ChildPositions(position, currentTurn)
            print("child calced min")
            if not children:
                print("if children empty min")
                return self.EvaluatePos(position), position

            for child in children:
                evaluation, z = self.Minimax(child, depth-1, self.MaxingPlayer(currentTurn), self.cycleTurn(currentTurn), alpha, beta)
               
                if min_eval != min(min_eval, evaluation):
                    best_move = child
                    min_eval = min(min_eval, evaluation)

                best_move = child
                beta = min(beta, evaluation)
                print("beta min")
                if beta <= alpha:
                    print("beta <= alpja")
                    break
            self.PrintReturning(depth, alpha, beta, min_eval, evaluation)
            return min_eval, best_move
            
    def ChildPositions(self, position, current_turn):
        position_list = []
        for Rindex, row in enumerate(position):
            for Eindex, element in enumerate(row):
                if (element == self.players[current_turn] or element == self.twoplayers[current_turn]) and self.LegalMove(Eindex, Rindex, self.FindY2(Rindex, position), position):
                    #print(element)
                    moved_position = deepcopy(position)
                    moved_position = self.MakeMove(moved_position, Eindex, Rindex, self.FindY2(Rindex, moved_position)) #it should RETURN a NEW BOARD: you must do copy
                    position_list.append(moved_position)

        self.PrintChildren(position_list)
        return position_list

    def EvaluatePos(self, position):
        score = 0
        for Rindex, row in enumerate(position):
            for element in row:
                if self.playercount == 3 and element == "G":
                    print(f"self.BoardScore[Rindex]*3 {(self.BoardScore[Rindex])**3}")
                    score -= (self.BoardScore[Rindex])*3
                elif element == "Y" or (self.playercount == 2 and element == "G"):
                    score += self.BoardScore[Rindex]
                elif element in self.players:
                    score -= self.BoardScore[Rindex]
        return score

    def MaxingPlayer(self, currentTurn):
        print("maxing deez")
        next_turn = self.cycleTurn(currentTurn)
        print("deez what")
        print(f"players {self.players}")
        print(f"next_turn {next_turn}")
        if self.players[next_turn] == "Y":
            print("deez nuts true")
            return True
        print("deez nuts false")
        return False

    def cycleTurn(self, currentTurn):
        print(f"current turn {currentTurn}")
        print(f"self.playercount {self.playercount}")
        return (currentTurn+1)%self.playercount

    def GameOver(self, position):
        for Rindex, row in enumerate(position):
            for Eindex, element in enumerate(row):
                if element != "":
                    if self.LegalMove(Eindex, Rindex, self.FindY2(Rindex, position), position):
                        return False
        if not self.TwoPiecesInScoringZone(position):
            return False

        return True

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
        if InputY2 > 4 or self.playercount == 1: 
            for element in board[InputY2]:
                if element == char:
                    return False
                
        return True    

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

    def FindY2(self, InputY1, board):
        number_of_pieces_in_row = 0
        for char in board[InputY1]:
            if char != "":
                number_of_pieces_in_row += 1   
        return (max(InputY1 - number_of_pieces_in_row, 0))

                
    def MakeMove(self, board, InputX, InputY1, InputY2):
        board[InputY2][InputX] = board[InputY1][InputX]
        board[InputY1][InputX] = ""
        return board

    def PrintMinimax(self, depth, alpha, beta, turn, maximizing_player, position, score):
        with open("output.txt", "a") as f:  # Append to keep logs from multiple calls
            f.write(f"Depth: {depth}\n")
            f.write(f"Alpha: {alpha}, Beta: {beta}\n")
            f.write(f"Current Turn: {turn}\n")
            f.write(f"Maximizing Player: {maximizing_player}\n")
            f.write(f"Score == {score}")
            f.write("Position:\n")

            for row in position:
                f.write(str(row) + "\n")  # Directly writes the list format

            f.write("\n" + "-" * 30 + "\n\n")  # Add a separator for readability
    
    def PrintChildren(self, children):
        with open("outputChildren.txt", "a") as f:  # Append mode to keep previous logs
            f.write("Children Positions:\n")

            for i, position in enumerate(children):
                f.write(f"Child {i + 1}:\n")
                for row in position:
                    f.write(str(row) + "\n")  # Write each row as a list

                f.write("\n")  # Space between children for readability

            f.write("-" * 30 + "\n\n")  # Separator after all children

    def PrintReturning(self, depth: int, alpha: int, beta: int, max_eval: int, score):
        with open("outputReturns.txt", "a") as f:  # Append mode to keep previous logs
            f.write(f"Returning at Depth {depth}:\n")
            f.write(f"Alpha: {alpha}, Beta: {beta}\n")
            f.write(f"Max Eval: {max_eval}\n")
            f.write(f"Score: {score}\n")
            f.write("-" * 30 + "\n\n")  # Separator for readability
