import pygame
import UpView
import UpModel

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        self.menu_screen = True
        pygame.init()

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitted")
                self.running = False
            if pygame.mouse.get_pressed()[0] == True:
                self.model.GameOver(self.model.Board)

                if self.menu_screen: # if on start screen

                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275:
                        self.view.DrawBoard() #start the game
                        self.menu_screen = False 
                        print("game started")
                    elif pygame.mouse.get_pos()[1] > 275 and pygame.mouse.get_pos()[1] < 412.5:
                        self.view.RulesWindow()
                        print("rules window windowed")
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[1] < 550:
                        self.running = False

                else:
                    if self.model.game["GAMEOVER"] == True:
                        self.model.ResetBoard()
                        self.view.DrawGameOver() #if the game is over
                        self.model.game["GAMEOVER"] = False

                    elif self.model.game["END SCREEN"] == True:
                        self.view.DrawMenu()
                        self.model.game["END SCREEN"] = False
                        self.menu_screen = True
                    elif self.model.PlayerIsHuman():
                        self.model.Clicking(self.model.Board, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.view.DimTile(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        pygame.display.update()
                        if self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                            self.model.CycleThruPlayerTurns()
                        self.view.DrawBoard()
                        print("selected player:", self.model.selected_piece)
                    elif not self.model.PlayerIsHuman() and (self.model.game['GAMEOVER'] == False): #if player isnt human and current palyer is an AI and game isnt over
                            print("AI MOVE CALCULATING")
                            try:
                                InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
                                self.model.MakeMove(InputX, InputY1, InputY2)
                                self.view.DrawBoard()
                                print("AI MOVE MADE")
                            except:
                                self.model.CycleThruPlayerTurns()
                                self.view.DrawBoard()
                                print("AI has no move")

    def ConvertMinimaxToInputs(self):
        
        InputX, InputY1, InputY2 = None, None, None
        try:
            evaluation, pos2 = self.model.Minimax(self.model.Board, 5, True, self.model.game['turn'])
            pos = self.model.minimax_pos[-1:][0]
            #print("converting minimax to inputs for MakeMove():")
            for row_index, row in enumerate(self.model.Board):
                for coloumn_index, coloumn in enumerate(self.model.Board[row_index]):

                    if self.model.Board[row_index][coloumn_index] != pos[row_index][coloumn_index]:

                        if self.model.Board[row_index][coloumn_index] == "":
                            InputY2, InputX = row_index, coloumn_index

                        elif self.model.Board[row_index][coloumn_index] != "":

                            InputY1 = row_index
                            if self.model.Board[row_index][coloumn_index] != self.model.playerColour[self.model.game['turn']]:
                                InputX, InputY2, InputY1 = None, None, None
                            
                            
                            
            print(InputX, InputY1, InputY2)
            return InputX, InputY1, InputY2
        except:
            return


