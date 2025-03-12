import pygame
import sys
import UpModel
import UpController
import multiprocessing

blue = [0, 0, 255]
green = [0, 255, 0]
yellow = [255, 255, 0]
black = [0, 0, 0]
white = [230, 230, 230]
red = [255, 0, 0]
grey = [255/2, 255/2, 255/2]



class View():

  def __init__(self, model, x=0, y=0):
    """
    List of variables:
      self.scaleheight (real): variable for the decimal that converts the original menu image's heights into the window size
      self.scalewidth (real): variable for the decimal that converts the original menu image's widths into the window size
      self.black_bar (bool): informs program if the board grid is black or not
      self.font (font): declares the font for the game over screen
      self.model (object): makes model a global variable
      self.SCREEN_HEIGHT (int): window length
      self.SCREEN_WIDTH (int): window width
      self.playerColour (dictionary): used to decide the colour of the grid lines of the board
      self.screen (window): the window used to present the GUI
    """
    self.scaleheight = 550/2245
    self.scalewidth = 300/1587
    self.black_bar = False
    self.font = pygame.font.Font(None, 74)
    self.model = model
    self.SCREEN_HEIGHT = 550
    self.SCREEN_WIDTH = 300
    pygame.init()
    self.playerColour = {
            1: red,
            2: blue,
            3: green,
            0: yellow
            }

    #represents png files
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    self.menu_img = pygame.image.load('MainMenu.PNG').convert_alpha()
    self.ai_menu_img = pygame.image.load('AiMenu.PNG').convert_alpha()
    self.rules_menu_img = pygame.image.load('RulesMenu.PNG').convert_alpha()
    self.rules1_img = pygame.image.load('OneRules.PNG').convert_alpha()
    self.rules2_img = pygame.image.load('TwoRules.PNG').convert_alpha()
    self.rules3_img = pygame.image.load('ThreeRules.PNG').convert_alpha()
    self.rules4_img = pygame.image.load('FourRules.PNG').convert_alpha()

  
  #determines colour of grid lines of board
  def BarColouration(self, color=0):
    if self.black_bar == False:
      color = self.playerColour[self.model.game['turn']]
      return color
    
    return black

  #draws the CPU opponent activation menu
  def DrawAiSetup(self):
    Img(0, 0, self.ai_menu_img, self.scalewidth, self.screen, self.scaleheight) 
    pygame.display.update()

  #draws the playercount menu
  def DrawHumanSetup(self):
    Img(0, 0, self.rules_menu_img, self.scalewidth, self.screen, self.scaleheight) 
    pygame.display.update()

  #draws the rules menu
  def DrawRulesSetup(self):
    Img(0, 0, self.rules_menu_img, self.scalewidth, self.screen, self.scaleheight)
    pygame.display.update()

  #used to draw the ruleset for a given player count
  def DrawRulesForPlayer(self, value):
    new_width = 700
    new_height = 662.5
    self.screen = pygame.display.set_mode((new_width, new_height))
    self.screen.fill((255, 255, 255))
    if value == '1':
      Img(0, 3, self.rules1_img, 0.8, self.screen)
    elif value == '2':
      Img(0, 3, self.rules2_img, 0.812, self.screen) 
    elif value == '3':
      Img(0, 3, self.rules3_img, 0.811, self.screen) 
    elif value == '4':
      Img(0, 3, self.rules4_img, 0.8, self.screen) 

    pygame.display.update()

  #draws the game board
  def DrawBoard(self, mauspos):
    self.screen.fill(white)
    self.DrawGrid() 
    for i, character in enumerate(self.model.Board[::-1]):
      for j, char in enumerate(character[::-1]):
        y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT/11)*i + self.SCREEN_HEIGHT/22 - self.SCREEN_HEIGHT/11
        x = self.SCREEN_WIDTH - (self.SCREEN_WIDTH/4)*j - self.SCREEN_WIDTH/8 

        self.DrawPieces(x, y, char, self.model.selected_coor, 10-i, 3-j)
    pygame.display.update()
    
  #used to draw board pieces
  def GreyCircle(self, n, l):
    self.screen.fill(white)
    self.DrawGrid() 
    for i, character in enumerate(self.model.Board[::-1]):
      for j, char in enumerate(character[::-1]):
        y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT/11)*i + self.SCREEN_HEIGHT/22 - self.SCREEN_HEIGHT/11
        x = self.SCREEN_WIDTH - (self.SCREEN_WIDTH/4)*j - self.SCREEN_WIDTH/8 

        self.DrawPieces(x, y, char, self.model.selected_coor, l, n)
    pygame.display.update()

  #Draws the main menu
  def DrawMenu(self):
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    pygame.display.set_caption("Menu")
    self.screen.fill(white)
    start_button = Img(0, 0, self.menu_img, self.scalewidth, self.screen, self.scaleheight)
    
    pygame.display.update()

  #highlights a piece and its possible move
  def DrawHighlighted(self, x, y, selected, i, j):
    if selected is None:
      pass
    elif selected[0] == i and selected[1] == j:
      pygame.draw.circle(self.screen, grey, (x, self.SCREEN_HEIGHT/22 + self.model.cpu.FindY2(i, self.model.Board)*self.SCREEN_HEIGHT/11), 20)
      pygame.draw.circle(self.screen, black, (x, self.SCREEN_HEIGHT/22 + self.model.cpu.FindY2(i, self.model.Board)*self.SCREEN_HEIGHT/11), 12)
      pygame.draw.circle(self.screen, grey, (x, self.SCREEN_HEIGHT/22 + self.model.cpu.FindY2(i, self.model.Board)*self.SCREEN_HEIGHT/11), 10)
      pygame.draw.circle(self.screen, grey, (x, y), 20)
      pygame.draw.circle(self.screen, black, (x, y), 12)
      pygame.display.update()

  #draws a piece
  def DrawPieces(self, x, y, character, selected, i, j):
    
    #circle(surface, color, center, radius)
    if character == 'R':
      pygame.draw.circle(self.screen, black, (x, y), 12)
      self.DrawHighlighted(x, y, selected, i, j)
      pygame.draw.circle(self.screen, red, (x, y), 10)

    elif character == 'G':
      pygame.draw.circle(self.screen, black, (x, y), 12)
      self.DrawHighlighted(x, y, selected, i, j)
      pygame.draw.circle(self.screen, green, (x, y), 10)

    elif character == 'B':
      pygame.draw.circle(self.screen, black, (x, y), 12)
      self.DrawHighlighted(x, y, selected, i, j)
      pygame.draw.circle(self.screen, blue, (x, y), 10)

    elif character == 'Y':
      pygame.draw.circle(self.screen, black, (x, y), 12)
      self.DrawHighlighted(x, y, selected, i, j)
      pygame.draw.circle(self.screen, yellow, (x, y), 10)

  #draws the game over state
  def DrawGameOver(self):
    """

    Creates a set of new surfaces in order to darken the game screen and give a leaderboard of each colour and their corresponding scores
    the CountScores function is used to build otu the list of sorted scores, and thenthe screen is updated

    List of variables: 
    dark_surface (surface): a semi-transparent overlay for the game over screen.
    scores (list): a list of tuples, sorted in descending order.
    game_over_text (surface): rendered text surface for the "GAME OVER" message.
    text_rect (rect): rectangle object for positioning the game over text.
    score_text (surface): rendered text surface for each player's score.
    score_rect (rect): rectangle object used to position each score.
    """
    dark_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    dark_surface.set_alpha(150)
    dark_surface.fill(black)
    self.screen.blit(dark_surface, (0, 0))
    
    scores = sorted(self.model.CountScores(), key=lambda x: x[0], reverse=True)

    game_over_text = self.font.render('GAME OVER', True, white)
    text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
    self.screen.blit(game_over_text, text_rect)
    
    y_offset = text_rect.bottom + 20
    for score, player_color in scores:
        score_text = self.font.render(f'{player_color}: {score}', True, white)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(score_text, score_rect)
        y_offset += 40
    pygame.display.update()

  #draws the board grid
  def DrawGrid(self):
    
    color = self.BarColouration()
    barwidth = 2
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(self.screen, color, (0, row * self.SCREEN_HEIGHT/11), (self.SCREEN_WIDTH, row * self.SCREEN_HEIGHT/11))
      pygame.draw.line(self.screen, black, (0, row * (self.SCREEN_HEIGHT/11)+1), (self.SCREEN_WIDTH, row * (self.SCREEN_HEIGHT/11)+1))
      
    
    #drawing the columns
    for column in range(1,4):
      pygame.draw.line(self.screen, color, (column * self.SCREEN_WIDTH/4, 0), (column * self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT))
      pygame.draw.line(self.screen, black, (column * (self.SCREEN_WIDTH/4)+1, 0), (column * (self.SCREEN_WIDTH/4)+1, self.SCREEN_HEIGHT))
    pygame.display.update()


class Img():
    def __init__(self, x, y, image, scaleX, surface, scaleY=0):
        """
        Class used to streamline the creation of an image by making it easy to adjust its size, location, relevant screen, and scale 
        
        Args:
        x (real): the x coordinate of the image to be rendered at
        y (real): the y coordinate of the image to be rendered at
        image (variable representing file): the image manipulated and blitted to the surface
        scaleX (real): the transform of the image width
        surface (surface): the surface the image will be blitted to
        scaleY (real): the transform of the image height, automatically equal to the width transform if not specified

        List of variables:
        width (real): the pixel width of the image fed into the function
        height (real): the pixel height of the image fed into the function
        """
        width = image.get_width()
        height = image.get_height()
        if scaleY == 0:
          scaleY = scaleX
        #controls the scale of the image
        #scale(surface, size, dest_surface=None)
        self.image = pygame.transform.scale(image, (int(width * scaleX), int(height * scaleY))) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        surface.blit(self.image, (x, y))