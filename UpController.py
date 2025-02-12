import pygame
import UpView
import UpModel
import threading
import time 
import random
from UpCPU import MinimaxMove

class Controller:
    def __init__(self, model, view, cpu):
        """
        Initialization function of the controller

        Args:
            model: instantiates a model object that the controller will use for the entirety fo the program
            view: instantiates a view object that the controller will use for the entirety fo the program

        List of variables:
            rulessetup (bool): used to see if the current screen is the rules setup screen
            threads (int): variable to initialise CheckAI func within a thread
            self.check_ai (bool): used for the running loop of CheckAI function
            self.one_player (bool): variable that tells the program if the user requests a single player game
            self.model (class): instantiates an instance of UpModel.py
            self.view (class): instantiates an instance of UpView.py
            self.running (bool): used for the event manager loop
            self.menu_screen (bool): tells the program if the user is currently on the menu screen
            self.rules_screen (bool): tells the program if the user is currently on the rules screen
            self.setup_screen (bool): tells the program if the user is currently on the game setup screen
            self.t1 (class): readies the t1 thread for initialisation 
        """
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
        pygame.init() #initialises pygame

    def event_manager(self):
        """
        primary function of the controller that uses the 'for event in pygame.event.get()' in order to constantly check for user input
        once a user input is detected, a lengthened if-elif statement is conducted to account for all valid inputs at a given time

        """

        for event in pygame.event.get(): #constantly checks for events for pygame to use
            if event.type == pygame.QUIT: #if the x in the top right of the window is pressed
                self.check_ai = False #end both loops which closes the window and ends the game
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.rulessetup == True:
                        self.rules_screen = False
                        self.menu_screen = True
                        self.rulessetup = False
                        self.view.DrawMenu() #sets the appropriate variables to true and false then redraws the main menu
                    elif self.setup_screen == True:
                        self.setup_screen_screen = False
                        self.menu_screen = True
                        self.view.DrawMenu() #sets the appropriate variables to true and false then redraws the main menu

                if event.key == pygame.K_SPACE and self.setup_screen: #if space is pressed on the game setup menu
                    self.model.GameStartLogic()
                    self.view.DrawBoard(pygame.mouse.get_pos())
                    self.rules_screen = False
                    self.menu_screen = False
                    self.setup_screen = False
                    if self.threads == 0:
                        self.t1.start() #initialises the t1 thread
                        self.threads = 1

            if pygame.mouse.get_pressed()[0] == True: #if mouse 1 is pressed
                if self.menu_screen:
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275: #if pressed in the bounds of the start button
                        self.view.DrawSetup()
                        self.setup_screen = True
                        self.menu_screen = False 
                        
                    elif 275 < pygame.mouse.get_pos()[1] < 412.5: # if pressed in the bounds of the rules button
                        self.menu_screen = False
                        self.setup_screen = True
                        self.rulessetup = True
                        self.view.DrawRulesSetup()

                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[1] < 550: #if pressed in bounds fo quit button
                        self.running = False

                elif self.rulessetup == True:
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] < 150: #One player game
                        self.view.DrawRulesForPlayer('1') 
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 150: #Two player game
                        self.view.DrawRulesForPlayer('2') 
                    if pygame.mouse.get_pos()[1] > 275 and pygame.mouse.get_pos()[1] < 412.5 and pygame.mouse.get_pos()[0] < 150: #Three player game
                        self.view.DrawRulesForPlayer('3')
                    if pygame.mouse.get_pos()[1] > 275 and pygame.mouse.get_pos()[1] < 412.5 and pygame.mouse.get_pos()[0] > 150: #Four player game
                        self.view.DrawRulesForPlayer('4')

                elif self.setup_screen == True:
                    """
                    redraw this entire menu screen -_-
                    """
                    if pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] < 75: #1 player game
                        self.model.playerCount = 1
                        self.one_player = True
                        self.view.black_bar = True
                        self.view.PasteImage(self.view.one_img, 0, 0, 300/380, 275/337) #highlight the clicked number
                        self.view.PasteImage(self.view.no_img, 0, 275, 300/382, 275/282) #highlight "N"
                    elif pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 75 and pygame.mouse.get_pos()[0] < 150: #2 player game
                        self.model.playerCount = 2
                        self.one_player = False
                        self.view.black_bar = False
                        self.view.PasteImage(self.view.two_img, 0, 0, 300/382, 275/330) #highlight the clicked number
                    elif pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 150 and pygame.mouse.get_pos()[0] < 225: #3 player game
                        self.model.playerCount = 3
                        self.one_player = False
                        self.view.black_bar = False
                        self.view.PasteImage(self.view.three_img, 0, 0, 300/380, 275/335) #highlight the clicked number
                    elif pygame.mouse.get_pos()[1] > 137.5 and pygame.mouse.get_pos()[1] < 275 and pygame.mouse.get_pos()[0] > 225: #4 player game
                        self.model.playerCount = 4
                        self.one_player = False
                        self.view.black_bar = False
                        self.view.PasteImage(self.view.four_img, 0, 0, 300/382, 275/331) #highlight the clicked number
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[0] < 150 and self.one_player == False: #"Y", include AI in the game
                        self.model.AiPlayer = True
                        self.view.PasteImage(self.view.yes_img, 0, 275, 300/381, 275/272) #highlight "Y"
                    elif pygame.mouse.get_pos()[1] > 412.5 and pygame.mouse.get_pos()[0] > 150: #"N", do not include AI in the game
                        self.model.AiPlayer = False
                        self.view.PasteImage(self.view.no_img, 0, 275, 300/382, 275/282) #highlight "N"

                else:
                    if self.model.game["END SCREEN"] == True: #if on the game over screen
                        self.view.DrawMenu() #return to the menu
                        self.model.game["END SCREEN"] = False
                        self.menu_screen = True
                    if self.model.PlayerIsHuman(): #if the current player's turn is a human player
                        self.model.Clicking(self.model.Board, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) #register a click
                        pygame.display.update()
                        if  self.menu_screen == False:
                            self.view.DrawBoard(pygame.mouse.get_pos()) #update the board so the player can see the highlighted tiles
                      

    def CheckAI(self):
        """
        Function used to check whether the game is over, 
        if a player's turn should be skipped, 
        and to check whether it is currently the AI player's turn, in which case, run AI
        """
        while self.check_ai:
            time.sleep(0.001) 
            if (self.model.NoLegalMoves(self.model.Board, "any")) or (self.model.TwoPiecesInScoringZone(self.model.Board)):
                time.sleep(1)
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
                time.sleep(0.1)
                self.RunAI()
                time.sleep(0.1)


    def RunAI(self):
        """
        Function that attempts to call minimax
        if minimax is uncallable, skip the current turn

        List of variables:
        InputX (int): the x (row) coordinate of the piece the minimax funtion wants to move
        InputY1 (int): the y coordinate of the piece the minimax funtion wants to move
        InputY2 (int): the y coordinate of the minimax function's chosen move

        """
        InputX, InputY1, InputY2 = None, None, None
        try:
            InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
            print("0")
            # self.model.Board = UpCPU.MakeMove(self.model.Board, InputX, InputY1, InputY2)
            self.model.Board = self.MakeMove(self.model.Board, InputX, InputY1, InputY2)
            print("4")
            self.CycleThruPlayerTurns()
            print(self.model.Board)
            self.model.CycleThruPlayerTurns()
            self.view.DrawBoard(pygame.mouse.get_pos())
            self.view.GreyCircle(InputX, InputY1)
        
        except:
            if InputX != 999:
                self.model.CycleThruPlayerTurns()
                self.view.DrawBoard(pygame.mouse.get_pos())
            else:
                self.view.DrawBoard(pygame.mouse.get_pos())

    def ConvertMinimaxToInputs(self):
        """
        Function used to actually call Minimax
        It mainly takes the minimax return values and turns them into values that can be used by the self.model.MakeMove() function 
        this allows the AI player to make their move on the actual game board


        Returns:
            returns InputX, InputY1, InputY2 if minimax has worked as intended
            returns nothing in case the minimax runs into an error
            returns 999, 999, 999 if it si not currently the AI players turn and the prior functions have ran into an error

        List of variables:
            InputX (int): the x (row) coordinate of the piece the minimax funtion wants to move
            InputY1 (int): the y coordinate of the piece the minimax funtion wants to move
            InputY2 (int): the y coordinate of the minimax function's chosen move
            evaluation (int): is the evaluation of the position that Minimax returns
            pos2 (list): pos2 is the position returned by the minimax function and is unused
            pos (list): pos is the best move presented by the minimax
        """
        InputX, InputY1, InputY2 = None, None, None
        self.model.positions = []
        if not self.model.PlayerIsHuman():
            #try:
            self.model.cpu.playercount = len(self.model.cpu.players)
            print("minimax attempted")
            evaluation, position = self.model.cpu.Minimax(self.model.Board, 10, True, 0, float('-inf'), float('inf'))
            print("minimax ended")
            for Rindex, row in enumerate(self.model.Board):
                for Eindex, element in enumerate(self.model.Board[Rindex]):
                    if self.model.Board[Rindex][Eindex] != position[Rindex][Eindex]:
                        if self.model.Board[Rindex][Eindex] == "":
                                InputY2, InputX = Rindex, Eindex
                                
                        elif self.model.Board[Rindex][Eindex] != "":
                            InputY1 = Rindex
            print(f"X: {InputX} -Y1: {InputY1} -Y2: {InputY2}")
            return InputX, InputY1, InputY2


            #except:
                #print("except")
                #return 
                
        else:
            return 999, 999, 999

    @MinimaxMove
    def MakeMove(self, board, InputX, InputY1, InputY2):
        pass




