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
                print("mouse 1 pressed")
                if self.menu_screen: # if on start screen
                    print("ur on the menu screen")
                    self.view.DrawBoard() #start the game
                    "Board drawn"
                    self.menu_screen = False 
                else:
                    if self.model.game["GAMEOVER"] == True: #if the game is over
                        self.model.ResetBoard() # reset the board and go back to start screen
                        self.menu_screen = True
                        self.view.DrawMenu()
                    else:
                        if self.model.Clicked == False:
                            self.model.ClickOne(pygame.mouse.get_pos())
                        else:
                            print("hoo")
                            if self.model.PlayerIsHuman():
                                if self.model.IsClickTwoEqualToClickOne(pygame.mouse.get_pos()) == False: #if move is legal then make it
                                    self.model.Clicked = False
                                    self.model.MakeMove(self.model.click_1_x, self.model.click_1_y, self.model.j)
                                    self.view.DrawBoard()
                            elif self.model.AiPlayers[self.model.playerColour[self.model.game['turn']]] and self.model.game['GAMEOVER'] == False: #if player isnt human and current palyer is an AI and game isnt over
                                self.model.MakeMove(self.ConvertMinimaxToInputs()) #gets CPU move and makes it

    def ConvertMinimaxToInputs(self):
        InputX, InputY1, InputY2 = None, None, None
        evaluation, pos = self.model.Minimax(self.model.Board, 5, float ['-inf'], float ['inf'], False)
        for row in self.model.Board:
            for coloumn in self.model.Board[row]:
                if self.model.Board[row][coloumn] != pos[row][coloumn]:
                    if self.model.Board[row][coloumn] == "":
                        row, coloumn = InputY1, InputX
                    elif self.model.Board[row][coloumn] != "":
                        row = InputY2
        return InputX, InputY1, InputY2


