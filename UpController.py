import pygame
import UpView
import UpModel
import threading
import time 
import random

class Controller:
    def __init__(self, model, view):
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
                    #print("draw1")
                    self.view.DrawBoard(pygame.mouse.get_pos())
                    self.rules_screen = False
                    self.menu_screen = False
                    self.setup_screen = False
                    if self.threads == 0:
                        self.t1.start()
                        self.threads = 1
                    #self.check_ai = True
                    #print("game started")

            if pygame.mouse.get_pressed()[0] == True:
                #print("mouse pressed")
                if self.menu_screen: # if on start screen
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275:
                        #print("setyp clicked")
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
                    if self.model.game["END SCREEN"] == True:
                        #print("end screen is true")
                        self.view.DrawMenu()
                        self.model.game["END SCREEN"] = False
                        self.menu_screen = True
                    if self.model.PlayerIsHuman():
                        self.model.Clicking(self.model.Board, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        pygame.display.update()
                        if self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                            #print("turn before cycle: ", self.model.playerColour[self.model.game['turn']])
                            self.model.CycleThruPlayerTurns()
                            #print("turn after cycle: ", self.model.playerColour[self.model.game['turn']])
                            #print("Cycle 1 controller")
                        if  self.menu_screen == False:
                            #print("draw2")
                            self.view.DrawBoard(pygame.mouse.get_pos())
                            #print("selected player:", self.model.selected_piece)
                      

    def CheckAI(self):
        #print("AI being checked")
        while self.check_ai:
            #print("thread")
            # print("self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']])", self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]))
            # print("thingy is true? ", not self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]) and not self.model.PlayerIsHuman() and (self.model.game['GAMEOVER'] == False), self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]), self.model.NoLegalMoves(self.model.Board, "any"))
            if not self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]) and not self.model.PlayerIsHuman() and (self.model.game['GAMEOVER'] == False):
                #print("AI running and player turn is: ", self.model.game['turn'])
                time.sleep(0.1)
                #print("sleep ended")
                self.RunAI()
                time.sleep(0.1)

            elif (self.model.NoLegalMoves(self.model.Board, "any") or self.model.TwoPiecesInScoringZone(self.model.Board)):
                self.view.DrawGameOver() #if the game is over
                self.model.ResetBoard()
                self.model.game["END SCREEN"] = True
                #self.check_ai = False

            elif self.model.NoLegalMoves(self.model.Board, self.model.playerColour[self.model.game['turn']]):
                self.model.CycleThruPlayerTurns()
                #print("turn cycled")
                
                self.view.DrawBoard(pygame.mouse.get_pos())

    def RunAI(self):
        #print("AI MOVE CALCULATING")
        InputX, InputY1, InputY2 = None, None, None
        #print("trying1")
        try:
            #print("trying")
            InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
            #print("TRY - InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
            self.model.MakeMove(InputX, InputY1, InputY2)
            #print("makey move")
            self.view.DrawBoard(pygame.mouse.get_pos())
            #print("drawey board")
            self.view.GreyCircle(InputX, InputY1)
            #print("greyest of circlets")
            #print("AI MOVE MADE")
        
        except:
            #print("input X: ", InputX)
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
                #print("evaluation, pos2 = ", evaluation, pos2)
                pos = self.model.minimax_pos[-1:][0]
                #print("evaluation, pos2, pos = ", evaluation, pos2, pos)
                #print("converting minimax to inputs for MakeMove():")
                for row_index, row in enumerate(self.model.Board):
                    #print("1")
                    #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                    for coloumn_index, coloumn in enumerate(self.model.Board[row_index]):
                        #print("2")
                        #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                        if self.model.Board[row_index][coloumn_index] != pos[row_index][coloumn_index]:
                            #print("3")
                            #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                            if self.model.Board[row_index][coloumn_index] == "":
                                InputY2, InputX = row_index, coloumn_index
                                #print("4")
                                #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                                
                            elif self.model.Board[row_index][coloumn_index] != "":
                                #print("5")
                                #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                                InputY1 = row_index
                                if self.model.Board[row_index][coloumn_index] != self.model.playerColour[self.model.game['turn']]: 
                                    if self.model.Board[row_index][coloumn_index] in self.model.free_colours:
                                        InputY1 = row_index
                                        return InputX, InputY1, InputY2
                                        #print("5.5 - InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                                    else:
                                        #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                                        #print("board piece: ", self.model.Board[row_index][coloumn_index])
                                        #print("free colours: ", self.model.free_colours)
                                        #print("is it in the thingy: ", self.model.Board[row_index][coloumn_index] not in self.model.free_colours)
                                        InputX, InputY2, InputY1 = None, None, None
                                        #print("6")
                                      
                if not self.model.ColourAiPlayers[self.model.Board[InputY1][InputX]]:
                    #print("7")
                    return
                            
                #print("InputX, InputY1, InputY2: ", InputX, InputY1, InputY2)
                return InputX, InputY1, InputY2
                
            except:
                #print("the except in convertminimax to inputs")
                return 
                
        else:
            #print("self.model.PlayerIsHuman() is true", self.model.PlayerIsHuman(), self.model.currentTurn)
            return 999, 999, 999




