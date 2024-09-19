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
                    self.view.draw_board() #start the game
                    "Board drawn"
                    self.menu_screen = False 
                else:
                    if self.game["GAMEOVER"] == True: #if the game is over
                        self.model.ResetBoard() # reset the board and go back to start screen
                        self.menu_screen = True
                        self.view.draw_menu()
                    else:
                        if UpController.Clicked == False:
                            ClickOne(pygame.mouse.get_pos)
                        else:
                            if ClickTwo(pygame.mouse.get_pos) == True:
                                MakeMove(click_1_x, click_1_y, j)
