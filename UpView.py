import pygame
import sys
import UpModel
import UpController
import multiprocessing

blue = [0, 0, 255]
green = [0, 255, 0]
yellow = [255, 255, 0]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
grey = [255/2, 255/2, 255/2]

class View():

  def __init__(self, model, x=0, y=0):
    self.black_bar = False
    self.menu_scale = 0.82
    self.selected_coords = 0, 0
    self.font = pygame.font.Font(None, 74)
    self.blue = [0, 0, 255]
    self.green = [0, 255, 0]
    self.yellow = [255, 255, 0]
    self.black = [0, 0, 0]
    self.white = [255, 255, 255]
    self.red = [255, 0, 0]
    self.__x = x
    self.__y = y
    self.model = model
    self.SCREEN_HEIGHT = 550
    self.SCREEN_WIDTH = 300
    pygame.init()

    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    self.Black_Square = pygame.image.load('Black_Square.PNG').convert_alpha()
    self.rules_img = pygame.image.load('FourRules.PNG').convert_alpha()
    self.start_img = pygame.image.load('Upthrust start.PNG').convert_alpha()
    self.menu_img = pygame.image.load('Upthrust Menu.PNG').convert_alpha()
    self.one_img = pygame.image.load('One.PNG').convert_alpha()
    self.two_img = pygame.image.load('Two.PNG').convert_alpha()
    self.three_img = pygame.image.load('Three.PNG').convert_alpha()
    self.four_img = pygame.image.load('Four.PNG').convert_alpha()
    self.yes_img = pygame.image.load('Yes.PNG').convert_alpha()
    self.no_img = pygame.image.load('No.PNG').convert_alpha()

    self.run = True
    self.invboard = self.model.Board[::-1]
    self.playerColour = {
            1: red,
            2: blue,
            3: green,
            0: yellow
            }

  
  def BarColouration(self, color=0):
    if self.black_bar == False:
      color = self.playerColour[self.model.game['turn']]
      return color
    
    return black

  def DrawSetup(self):
    Img(0, 0, self.menu_img, self.menu_scale, self.screen)
    pygame.display.update()

  def PasteImage(self, filename, x, y):
    Img(x, y, filename, self.menu_scale, self.screen)
    pygame.display.update()

  def DrawMenu(self):
    #print("menu drawn")
    self.screen.fill((255, 255, 255))  # White background
    pygame.display.set_caption("Menu")
    pygame.draw.rect(self.screen, (200, 0, 0), (100, 275, 200, 50))  # Example button area
    pygame.display.update()

  def DrawRules(self):
    new_width = 800  
    new_height = 600 
    self.screen = pygame.display.set_mode((new_width, new_height))

    self.screen.fill((255, 255, 255))
    Img(0, 3, self.rules_img, 0.5, self.screen)
    pygame.display.update()

  def DrawBoard(self, mauspos):
    self.screen.fill(white)
    self.DrawGrid() 
    #self.BarAtTheTop()
    for i, character in enumerate(self.model.Board[::-1]):
      for j, char in enumerate(character[::-1]):
        y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT/11)*i + self.SCREEN_HEIGHT/22 - self.SCREEN_HEIGHT/11
        x = self.SCREEN_WIDTH - (self.SCREEN_WIDTH/4)*j - self.SCREEN_WIDTH/8 

        self.DrawPieces(x, y, char, self.model.selected_coor, 10-i, 3-j)
    pygame.display.update()
    #print("screen just updated boss")
    
  def GreyCircle(self, n, l):
    self.screen.fill(white)
    self.DrawGrid() 
    #self.BarAtTheTop()
    for i, character in enumerate(self.model.Board[::-1]):
      for j, char in enumerate(character[::-1]):
        y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT/11)*i + self.SCREEN_HEIGHT/22 - self.SCREEN_HEIGHT/11
        x = self.SCREEN_WIDTH - (self.SCREEN_WIDTH/4)*j - self.SCREEN_WIDTH/8 

        self.DrawPieces(x, y, char, self.model.selected_coor, l, n)
    pygame.display.update()
    #print("screen just updated boss")

  def DrawMenu(self):
    pygame.display.set_caption("Menu")
    self.screen.fill(white)
    start_button = Img(0, 0, self.start_img, 0.52, self.screen)
    
    pygame.display.update()

  def DrawPieces(self, x, y, character, selected, i, j):
    if selected is None:
      pass

    elif selected[0] == i and selected[1] == j:
      pygame.draw.rect(self.screen, grey, (x-self.SCREEN_WIDTH/8 + 1.5, y-self.SCREEN_HEIGHT/22 +1.5, self.SCREEN_WIDTH/4 - 1, self.SCREEN_HEIGHT/11 - 1), 30)
      pygame.draw.circle(self.screen, black, (x, y), 10)
      pygame.display.update()
      #print("circles drawn at:", (x, y))

    """circle(surface, color, center, radius)"""
    if character == 'R':
      pygame.draw.circle(self.screen, red, (x, y), 10)

    elif character == 'G':
      pygame.draw.circle(self.screen, green, (x, y), 10)

    elif character == 'B':
      pygame.draw.circle(self.screen, blue, (x, y), 10)

    elif character == 'Y':
      pygame.draw.circle(self.screen, yellow, (x, y), 10)


  def GetY(self): 
    return self.__y
  def SetY(self, y):
    self.__y = y

  def GetX(self):
    return self.__x
  def SetX(self, x):
    self.__x = x

  def ConvertMouseLoc(self, location, row=0, coloumn=0):
    row = location[0] // (self.SCREEN_WIDTH // 4)
    coloumn = location[0] // (self.SCREEN_WIDTH // 11)

  def DrawGameOver(self):
    dark_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    dark_surface.set_alpha(150)
    dark_surface.fill(black)
    self.screen.blit(dark_surface, (0, 0))

    scores = self.model.CountScores()
    #print(f"scores are {scores}")
    sorted_scores = sorted(scores, key=lambda x: x[0], reverse=True)

    game_over_text = self.font.render('GAME OVER', True, white)
    text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
    self.screen.blit(game_over_text, text_rect)
    
    y_offset = text_rect.bottom + 20
    for score, player_color in sorted_scores:
        score_text = self.font.render(f'{player_color}: {score}', True, white)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(score_text, score_rect)
        y_offset += 40

    pygame.display.update()



  def DrawGrid(self):
    color = self.BarColouration()

    #drawing the rows
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(self.screen, color, (0, row * self.SCREEN_HEIGHT/11), (self.SCREEN_WIDTH, row * self.SCREEN_HEIGHT/11))
    
    
    #drawing the columns
    for column in range(1,4):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(self.screen, color, (column * self.SCREEN_WIDTH/4, 0), (column * self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT))
    pygame.display.update()
      
    

class Img():
    def __init__(self, x, y, image, scale, surface):
        """
        creates a button at the x and y coordinates given,
        it puts the image you enter as a parameter as the button itself,
        and the scale allows you to tweak the size of the button as often, the images are of nonuniform size
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        surface.blit(self.image, (x, y))
