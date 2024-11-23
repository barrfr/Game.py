import pygame
import UpView
import UpModel
import threading
import time 
import random

class Controller:
    def __init__(self, model, view):
        t1 = threading.Thread(target=self.CheckAI)
        self.one_player = False
        self.model = model
        self.view = view
        self.running = True
        self.menu_screen = True
        self.rules_screen = False
        self.setup_screen = False
        pygame.init()
        t1.start()

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #print("quitted")
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.rules_screen:
                    # Return to the menu
                    self.rules_screen = False
                    self.menu_screen = True
                    self.view.DrawMenu()

                if event.key == pygame.K_SPACE and self.setup_screen:
                    self.model.GameStartLogic()
                    self.view.DrawBoard(pygame.mouse.get_pos())
                    self.rules_screen = False
                    self.menu_screen = False
                    self.setup_screen = False
                    print("game started")

            if pygame.mouse.get_pressed()[0] == True:
                self.model.GameOver(self.model.Board)

                if self.menu_screen: # if on start screen

                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275:
                        print("setyp clicked")
                        self.view.DrawSetup()
                        self.setup_screen = True
                        self.menu_screen = False 
                        
                    elif 275 < pygame.mouse.get_pos()[1] < 412.5: # rules
                        self.menu_screen = False
                        self.rules_screen = True
                        self.view.DrawRules()

                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[1] < 550:
                        self.running = False

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
                        self.view.PasteImage(self.view.four_img, -1, 0)
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[0] < 150 and self.one_player == False: #Yes
                        self.model.AiPlayer = True
                        self.view.PasteImage(self.view.yes_img, 1.3, 333)
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[0] > 150: #No
                        self.model.AiPlayer = False
                        self.view.PasteImage(self.view.no_img, -1.3, 327)

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
                        pygame.display.update()
                        if self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                            #print("turn before cycle: ", self.model.playerColour[self.model.game['turn']])
                            self.model.CycleThruPlayerTurns()
                            #print("turn after cycle: ", self.model.playerColour[self.model.game['turn']])
                            #print("Cycle 1 controller")
                        self.view.DrawBoard(pygame.mouse.get_pos())
                        #print("selected player:", self.model.selected_piece)
                     #if player isnt human and current palyer is an AI and game isnt over          

    def CheckAI(self):
        while True:
            if not self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]) and not self.model.PlayerIsHuman() and (self.model.game['GAMEOVER'] == False):
                #print("AI running and player turn is: ", self.model.game['turn'])
                time.sleep(0.1)
                #print("sleep ended")
                self.RunAI()

    def RunAI(self):
        #print("AI MOVE CALCULATING")

        try:
            InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
            self.model.MakeMove(InputX, InputY1, InputY2)
            self.view.DrawBoard(pygame.mouse.get_pos())
            self.view.GreyCircle(InputX, InputY1)
            #print("AI MOVE MADE")
        except:
            if InputX != 999:
                self.model.CycleThruPlayerTurns()
                ("Cycle 2 in controller")
                self.view.DrawBoard(pygame.mouse.get_pos())
                #print("AI has no move")
            else:
                self.view.DrawBoard(pygame.mouse.get_pos())
                #print("player is human")

            

    def ConvertMinimaxToInputs(self):
        
        InputX, InputY1, InputY2 = None, None, None
        if not self.model.PlayerIsHuman():
            try:
                evaluation, pos2 = self.model.Minimax(self.model.Board, 3, True, self.model.game['turn'])
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
                                
                if not self.model.ColourAiPlayers[self.model.Board[InputY1][InputX]]:
                    return
                                
                                
                #print(InputX, InputY1, InputY2)
                return InputX, InputY1, InputY2
            except:
                #print("the except in convertminimax to inputs")
                return
        else:
            #print("self.model.PlayerIsHuman() is true")
            return 999, 999, 999




