import pygame
import UpView
import UpModel
import threading
import time 
import random

class Controller:
    def __init__(self, model, view):
        self.rulessetup = False
        self.threads = 0
        self.check_ai = True
        self.one_player = False
        self.model = model
        self.view = view
        self.running = True
        self.menu_screen = True
        self.rules_screen = False
        self.setup_screen = False
        self.t1 = threading.Thread(target=self.CheckAI)
        pygame.init()

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.check_ai = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to the menu
                    if self.rulessetup == True:
                        self.rules_screen = False
                        self.menu_screen = True
                        self.rulessetup = False
                        self.view.DrawMenu()
                    elif self.setup_screen == True:
                        self.setup_screen_screen = False
                        self.menu_screen = True
                        self.view.DrawMenu()

                if event.key == pygame.K_SPACE and self.setup_screen:
                    self.model.GameStartLogic()
                    self.view.DrawBoard(pygame.mouse.get_pos())
                    self.rules_screen = False
                    self.menu_screen = False
                    self.setup_screen = False
                    if self.threads == 0:
                        self.t1.start()
                        self.threads = 1

            if pygame.mouse.get_pressed()[0] == True:
                if self.menu_screen: # if on start screen
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275:
                        self.view.DrawSetup()
                        self.setup_screen = True
                        self.menu_screen = False 
                        
                    elif 275 < pygame.mouse.get_pos()[1] < 412.5: # rules
                        self.menu_screen = False
                        self.setup_screen = True
                        self.rulessetup = True
                        self.view.DrawRulesSetup()

                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[1] < 550:
                        self.running = False

                elif self.rulessetup == True:
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] < 150: #One
                        self.view.DrawRules('1')
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 150: #Two
                        self.view.DrawRules('2') 
                    if pygame.mouse.get_pos()[1] > 275 and pygame.mouse.get_pos()[1] < 412.5 and pygame.mouse.get_pos()[0] < 150: #Three
                        self.view.DrawRules('3')
                    if pygame.mouse.get_pos()[1] > 275 and pygame.mouse.get_pos()[1] < 412.5 and pygame.mouse.get_pos()[0] > 150: #Three
                        self.view.DrawRules('4')

                elif self.setup_screen == True:
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] < 75: #1
                        self.model.playerCount = 1
                        self.one_player = True
                        self.view.black_bar = True
                        self.view.PasteImage(self.view.one_img, 0, 0)
                        self.view.PasteImage(self.view.no_img, -1.3, 327)
                    elif pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 75 and pygame.mouse.get_pos()[0] < 150: #2
                        self.model.playerCount = 2
                        self.one_player = False
                        self.view.black_bar = False
                        self.view.PasteImage(self.view.two_img, -1, 0)
                    elif pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 150 and pygame.mouse.get_pos()[0] < 225: #3
                        self.model.playerCount = 3
                        self.one_player = False
                        self.view.black_bar = False
                        self.view.PasteImage(self.view.three_img, -1, 0)
                    elif pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 225: #4
                        self.model.playerCount = 4
                        self.one_player = False
                        self.view.black_bar = False
                        self.view.PasteImage(self.view.four_img, 0, 0)
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[0] < 150 and self.one_player == False: #Yes
                        self.model.AiPlayer = True
                        self.view.PasteImage(self.view.yes_img, 1.3, 333)
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[0] > 150: #No
                        self.model.AiPlayer = False
                        self.view.PasteImage(self.view.no_img, -1.3, 327)

                else:
                    if self.model.game["END SCREEN"] == True:
                        self.view.DrawMenu()
                        self.model.game["END SCREEN"] = False
                        self.menu_screen = True
                    if self.model.PlayerIsHuman():
                        self.model.Clicking(self.model.Board, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        pygame.display.update()
                        if self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                            self.model.CycleThruPlayerTurns()
                        if  self.menu_screen == False:
                            self.view.DrawBoard(pygame.mouse.get_pos())
                      

    def CheckAI(self):
        while self.check_ai:
            time.sleep(0.001)
            if (self.model.NoLegalMoves(self.model.Board, "any")) or (self.model.TwoPiecesInScoringZone(self.model.Board)):
                time.sleep(1)
                print("game over")
                self.model.game['GAMEOVER'] = True
                self.view.DrawGameOver() #if the game is over
                time.sleep(0.1)
                self.model.ResetBoard()
                time.sleep(0.1)
                self.model.game["END SCREEN"] = True
                time.sleep(0.1)

            elif self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                self.model.CycleThruPlayerTurns()
                
                self.view.DrawBoard(pygame.mouse.get_pos())

            elif not self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]) and not self.model.PlayerIsHuman() and (self.model.game['GAMEOVER'] == False):
                print("   IS THE GAME SUPPOSED TO BE OVER", self.model.NoLegalMoves(self.model.Board, "any"), self.model.TwoPiecesInScoringZone(self.model.Board))
                time.sleep(0.1)
                self.RunAI()
                time.sleep(0.1)


    def RunAI(self):
        InputX, InputY1, InputY2 = None, None, None
        try:
            InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
            self.model.MakeMove(InputX, InputY1, InputY2)
            self.view.DrawBoard(pygame.mouse.get_pos())
            self.view.GreyCircle(InputX, InputY1)
        
        except:
            if InputX != 999:
                self.model.CycleThruPlayerTurns()
                self.view.DrawBoard(pygame.mouse.get_pos())
            else:
                self.view.DrawBoard(pygame.mouse.get_pos())

    def ConvertMinimaxToInputs(self):
        
        InputX, InputY1, InputY2 = None, None, None
        if not self.model.PlayerIsHuman():
            try:
                evaluation, pos2 = self.model.Minimax(self.model.Board, 2, True, self.model.game['turn'], -999, 999, False)
                
                for i, char in enumerate(self.model.minimax_pos):
                    print(f"pos {i} == {self.model.minimax_pos[i]}")
                
                pos = self.model.minimax_pos[-1:][0]
                print("pos ", pos)
                for row_index, row in enumerate(self.model.Board):
                    for coloumn_index, coloumn in enumerate(self.model.Board[row_index]):
                        if self.model.Board[row_index][coloumn_index] != pos[row_index][coloumn_index]:
                            if self.model.Board[row_index][coloumn_index] == "":
                                InputY2, InputX = row_index, coloumn_index
                                
                            elif self.model.Board[row_index][coloumn_index] != "":
                                InputY1 = row_index
                                if self.model.Board[row_index][coloumn_index] != self.model.playerColour[self.model.game['turn']]: 
                                    if self.model.Board[row_index][coloumn_index] == 'G' and (self.model.GFree == True or self.model.TFree == True):
                                        InputY1 = row_index
                                        return InputX, InputY1, InputY2
                                    
                                    else:
                                        InputX, InputY2, InputY1 = None, None, None
                                      
                if not self.model.ColourAiPlayers[self.model.Board[InputY1][InputX]]:
                    return
                            
                return InputX, InputY1, InputY2
                
            except:
                return 
                
        else:
            return 999, 999, 999




