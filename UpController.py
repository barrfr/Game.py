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
            self.playercountdepth (dictionary): different playercounts take longer for minimax to process, this is used so that the optimal depth is used for each playercount according to processing time
        """
        self.rules_setup = False 
        self.threads = 0 
        self.check_ai = True
        self.one_player = False
        self.model = model
        self.view = view
        self.running = True
        self.menu_screen = True
        self.rules_screen = False 
        self.t1 = threading.Thread(target=self.CheckAI)
        self.playercountdepth = {
            1: 0, 
            2: 7, 
            3: 10, 
            4: 15
            }
        self.human_setup_screen = False
        self.ai_setup_screen = False
        pygame.init() #initialises pygame

    def event_manager(self):
        """
        primary function of the controller that uses the 'for event in pygame.event.get()' in order to constantly check for user input
        once a user input is detected, a lengthened if-elif statement is conducted to account for all inputs that invoke a response from the program at a given time

        """

        for event in pygame.event.get(): #constantly checks for events for pygame to use
            if event.type == pygame.QUIT: #if the x in the top right of the window is pressed
                self.check_ai = False #end both loops which closes the window and ends the game
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(f"main, human, ai, rules {self.menu_screen, self.human_setup_screen, self.ai_setup_screen, self.rules_setup == True}")
                    if self.rules_setup == True:
                        self.rules_screen = False
                        self.menu_screen = True
                        self.rules_setup = False
                        self.view.DrawMenu() #sets the appropriate variables to true and false then redraws the main menu
                    elif self.human_setup_screen == True:
                        self.human_setup_screen = False
                        self.menu_screen = True
                        self.view.DrawMenu() #sets the appropriate variables to true and false then redraws the main menu
                    elif self.ai_setup_screen == True:
                        self.ai_setup_screen = False
                        self.human_setup_screen = True
                        self.view.DrawHumanSetup()

            if pygame.mouse.get_pressed()[0] == True: #if mouse 1 is pressed
                if self.menu_screen and pygame.mouse.get_pos()[0] > (1/10)*self.view.SCREEN_WIDTH and pygame.mouse.get_pos()[0] < self.view.SCREEN_WIDTH - (1/10)*self.view.SCREEN_WIDTH:
                    print("click Menu bounds")
                    if pygame.mouse.get_pos()[1] > (86/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (293/594)*self.view.SCREEN_HEIGHT: #square 2
                        print("click Menu 2")
                        self.human_setup_screen = True
                        self.menu_screen = False 
                        self.view.DrawHumanSetup()

                    elif pygame.mouse.get_pos()[1] > (151/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (47/66)*self.view.SCREEN_HEIGHT: #square 3
                        print("click Menu 3")
                        self.menu_screen = False
                        self.rules_setup = True
                        self.view.DrawRulesSetup()

                    elif pygame.mouse.get_pos()[1] > (8/11)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (553/594)*self.view.SCREEN_HEIGHT: #square 4
                        print("click Menu 4")
                        self.running = False

                elif self.human_setup_screen == True and pygame.mouse.get_pos()[0] > (1/10)*self.view.SCREEN_WIDTH and pygame.mouse.get_pos()[0] < self.view.SCREEN_WIDTH - (1/10)*self.view.SCREEN_WIDTH:
                    print("human setup true")
                    '''
                    7/99 | (7/99) + (11/54) = 163/594
                    (163/594) + (1/66) = 86/297 | (86/297) + (11/54) = 293/594
                    (293/594) + (1/66) = 151/297 | (151/297) + (11/54) = 47/66
                    (47/66) + (1/66) = 8/11 | (8/11) + (11/54) = 553/594
                    '''
                    if pygame.mouse.get_pos()[1] > (7/99)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (163/594)*self.view.SCREEN_HEIGHT: #square 1
                        self.human_setup_screen = False
                        self.one_player = True
                        self.model.playerCount = 1
                        self.view.black_bar = True                   
                        self.model.AiPlayer = False
                        self.model.GameStartLogic()
                        self.view.DrawBoard(pygame.mouse.get_pos())
                        if self.threads == 0:
                            self.t1.start() #initialises the t1 thread
                            self.threads = 1
                    if pygame.mouse.get_pos()[1] > (86/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (293/594)*self.view.SCREEN_HEIGHT: #square 2
                        self.human_setup_screen = False
                        self.ai_setup_screen = True 
                        self.one_player = False
                        self.model.playerCount = 2
                        self.view.black_bar = False                    
                        self.view.DrawAiSetup()
                    if pygame.mouse.get_pos()[1] > (151/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (47/66)*self.view.SCREEN_HEIGHT: #square 3
                        self.human_setup_screen = False
                        self.ai_setup_screen = True 
                        self.one_player = False
                        self.model.playerCount = 3
                        self.view.black_bar = False                    
                        self.view.DrawAiSetup()
                    if pygame.mouse.get_pos()[1] > (8/11)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (553/594)*self.view.SCREEN_HEIGHT: #square 4
                        self.human_setup_screen = False
                        self.ai_setup_screen = True 
                        self.one_player = False
                        self.model.playerCount = 4
                        self.view.black_bar = False                    
                        self.view.DrawAiSetup()

                elif self.ai_setup_screen == True and pygame.mouse.get_pos()[0] > (1/10)*self.view.SCREEN_WIDTH and pygame.mouse.get_pos()[0] < self.view.SCREEN_WIDTH - (1/10)*self.view.SCREEN_WIDTH:
                    print("ai setup true")
                    if pygame.mouse.get_pos()[1] > (86/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (293/594)*self.view.SCREEN_HEIGHT: #square 2
                        self.ai_setup_screen = False
                        self.model.AiPlayer = True
                        self.model.GameStartLogic()
                        print("setted")
                        self.view.DrawBoard(pygame.mouse.get_pos())
                        if self.threads == 0:
                            self.t1.start() #initialises the t1 thread
                            self.threads = 1
                    if pygame.mouse.get_pos()[1] > (151/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (47/66)*self.view.SCREEN_HEIGHT: #square 3
                        self.ai_setup_screen = False
                        self.model.AiPlayer = False
                        self.model.GameStartLogic()
                        self.view.DrawBoard(pygame.mouse.get_pos())
                        if self.threads == 0:
                            self.t1.start() #initialises the t1 thread
                            self.threads = 1


                elif self.rules_setup == True and pygame.mouse.get_pos()[0] > (1/10)*self.view.SCREEN_WIDTH and pygame.mouse.get_pos()[0] < self.view.SCREEN_WIDTH - (1/10)*self.view.SCREEN_WIDTH:
                    print("rulessetup True")
                    if pygame.mouse.get_pos()[1] > (7/99)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (163/594)*self.view.SCREEN_HEIGHT: #square 1
                        self.view.DrawRulesForPlayer('1') 
                    if pygame.mouse.get_pos()[1] > (86/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (293/594)*self.view.SCREEN_HEIGHT: #square 2
                        self.view.DrawRulesForPlayer('2') 
                    if pygame.mouse.get_pos()[1] > (151/297)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (47/66)*self.view.SCREEN_HEIGHT: #square 3
                        self.view.DrawRulesForPlayer('3')
                    if pygame.mouse.get_pos()[1] > (8/11)*self.view.SCREEN_HEIGHT and pygame.mouse.get_pos()[1] < (553/594)*self.view.SCREEN_HEIGHT: #square 4
                        self.view.DrawRulesForPlayer('4')

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
        #try:
        InputX, InputY1, InputY2 = self.ConvertMinimaxToInputs() #calls minimax within the function and then puts the algorithms move into a trio of varialbes
        print("0")
        # self.model.Board = UpCPU.MakeMove(self.model.Board, InputX, InputY1, InputY2)
        self.model.Board = self.MakeMove(self.model.Board, InputX, InputY1, InputY2)
        print("4")
        self.model.CycleThruPlayerTurns()
        print(self.model.Board)
        self.view.DrawBoard(pygame.mouse.get_pos())
        self.view.GreyCircle(InputX, InputY1)
        
        #except:
            # if InputX != 999:
            #     self.model.CycleThruPlayerTurns()
            #     self.view.DrawBoard(pygame.mouse.get_pos())
            # else:
            #     self.view.DrawBoard(pygame.mouse.get_pos())

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
            print(f"minimax attempted {self.playercountdepth[self.model.playerCount]}")
            evaluation, position = self.model.cpu.Minimax(self.model.Board, self.playercountdepth[self.model.playerCount], True, 0, float('-inf'), float('inf'))
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




