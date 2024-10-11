import pygame
import UpView
import UpModel

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        self.menu_screen = True

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitted")
                self.running = False
            if pygame.mouse.get_pressed()[0] == True:
                if self.menu_screen: # if on start screen
                    self.view.DrawBoard() #start the game
                    "Board drawn"
                    self.menu_screen = False 
                else:
                    if self.model.game["GAMEOVER"] == True:
                        self.view.DrawGameOver #if the game is over
                        self.model.ResetBoard() # reset the board and go back to start screen
                        #self.menu_screen = True
                        #self.view.DrawMenu()
                    else:
                        if self.model.Clicked == False:
                            self.model.ClickOne(pygame.mouse.get_pos())
                        else:
                            if self.model.PlayerIsHuman():
                                print("Human player moving")
                                print("player turn: ", self.model.game['turn'])
                                if self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                                    print("no legal moves")
                                    self.model.CycleThruPlayerTurns()
                                    self.view.DrawBoard()
                                else:
                                    print("legal move for current piece")
                                    if self.model.IsClickTwoEqualToClickOne(pygame.mouse.get_pos()) == False: #if move is legal then make it
                                        self.model.Clicked = False
                                        self.model.MakeMove(self.model.click_1_x, self.model.click_1_y, self.model.j)
                                        self.view.DrawBoard()
                                        print("human move made")
                            elif self.model.PlayerIsHuman and self.model.game['GAMEOVER'] == False: #if player isnt human and current palyer is an AI and game isnt over
                                print("AI MOVE CALCULATING")
                                try:
                                    InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
                                    self.model.MakeMove(InputX, InputY1, InputY2)
                                    self.view.DrawBoard()
                                    print("AI MOVE MADE")
                                except:
                                    self.view.DrawBoard()
                                    print("AI has no move")

    def ConvertMinimaxToInputs(self):
        
        InputX, InputY1, InputY2 = None, None, None
        try:
            evaluation, pos2 = self.model.Minimax(self.model.Board, 2, True, self.model.game['turn'])
            pos = self.model.minimax_pos[-1:][0]
            print("converting minimax to inputs for MakeMove():")
            print("evaluation,minimax_pos[-1:][0]: ", evaluation, pos)
            print(pos2)
            print(self.model.Board)
            for row_index, row in enumerate(self.model.Board):
                for coloumn_index, coloumn in enumerate(self.model.Board[row_index]):

                    if self.model.Board[row_index][coloumn_index] != pos[row_index][coloumn_index]:
                        print("tile in minimax board not same as main board")

                        if self.model.Board[row_index][coloumn_index] == "":
                            InputY2, InputX = row_index, coloumn_index

                        elif self.model.Board[row_index][coloumn_index] != "":
                            InputY1 = row_index
                            
            print(InputX, InputY1, InputY2)
            return InputX, InputY1, InputY2
        except:
            return


