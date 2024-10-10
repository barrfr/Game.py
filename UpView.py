import pygame

from UpModel import UpThrustBoard



blue = [0, 0, 255]
green = [0, 255, 0]
yellow = [255, 255, 0]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]

class View():

  def __init__(self, model, x=0, y=0):
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
    self.start_img = pygame.image.load('UpThrust start.PNG').convert_alpha()
    self.run = True
    self.invboard = model.Board[::-1]
    self.playerColour = {
            1: red,
            2: blue,
            3: green,
            0: yellow
            }

  
  def BarColouration(self, color=0):
    color = self.playerColour[self.model.game['turn']]
    return color

  """ 
  def BarAtTheTop(self):
    color = self.BarColouration()
    "rect(surface, color, pos)"
    pygame.draw.polygon(self.screen, color, [(0, 0), (300, 0), (300, 25), (0, 25)])
  """

  def DrawBoard(self):
    self.screen.fill(white)
    self.DrawGrid() 
    #self.BarAtTheTop()
    for i, character in enumerate(self.invboard):
      for j, char in enumerate(character[::-1]):
        y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT/11)*i + self.SCREEN_HEIGHT/22 - self.SCREEN_HEIGHT/11
        x = self.SCREEN_WIDTH - (self.SCREEN_WIDTH/4)*j - self.SCREEN_WIDTH/8 
        self.DrawPieces(x, y, char)
    pygame.display.update()
        
    print("screen just updated boss")
    

  def DrawMenu(self):
    pygame.display.set_caption("Menu")
    self.screen.fill(white)
    start_button = Button(0, 0, self.start_img, 0.4, self.screen)
    
    pygame.display.update()

  def DrawPieces(self, x, y, character):

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
      
    

class Button():
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
        self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
