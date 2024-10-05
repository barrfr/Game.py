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
                            if self.model.IsClickTwoEqualToClickOne(pygame.mouse.get_pos()) == False:
                                self.model.Clicked = False
                                self.model.MakeMove(self.model.click_1_x, self.model.click_1_y, self.model.j)
                                self.view.DrawBoard()

                                model.game['turn']

