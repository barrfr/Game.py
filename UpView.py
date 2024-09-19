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
    self.__x = x
    self.__y = y
    self.model = model
    self.SCREEN_HEIGHT = 550
    self.SCREEN_WIDTH = 300
    pygame.init()
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    self.start_img = pygame.image.load('Start_Button.PNG').convert_alpha()
    self.run = True
    self.invboard = UpThrustBoard().Board[::-1]
    

  def draw_board(self):
    self.drawGrid() 
    for i, character in enumerate(self.invboard):
      for j, char in enumerate(character[::-1]):
        self.__y = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT/11)*i + self.SCREEN_HEIGHT/22 - self.SCREEN_HEIGHT/11
        self.__x = self.SCREEN_WIDTH - (self.SCREEN_WIDTH/4)*j - self.SCREEN_WIDTH/8 
        self.draw_pieces(self.__x, self.__y, char)
        pygame.screen.update()
    

  def draw_menu(self):
    pygame.display.set_caption("Menu")
    self.screen.fill(white)
    start_button = Button(50, 50, self.start_img, 0.1, self.screen)
    
    pygame.display.update()

  def draw_pieces(self, x, y, character):
    self.__x = x
    self.__y = y

    """circle(surface, color, center, radius)"""
    if character == 'R':
      pygame.draw.circle(self.screen, red, (x, y), 10)

    elif character == 'G':
      pygame.draw.circle(self.screen, green, (x, y), 10)

    elif character == 'B':
      pygame.draw.circle(self.screen, blue, (x, y), 10)

    elif character == 'Y':
      pygame.draw.circle(self.screen, yellow, (x, y), 10)


  def get_y(self): 
    return self.__y
  def set_y(self, y):
    self.__y = y

  def get_x(self):
    return self.__x
  def set_x(self, x):
    self.__x = x

  def ConvertMouseLoc(self, location, row=0, coloumn=0):
    row = location[0] // (self.SCREEN_WIDTH // 4)
    coloumn = location[0] // (self.SCREEN_WIDTH // 11)

  def drawGrid(self):

    #drawing the rows
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(self.screen, black, (0, row * self.SCREEN_HEIGHT/11), (self.SCREEN_WIDTH, row * self.SCREEN_HEIGHT/11))
    
    
    #drawing the columns
    for column in range(1,4):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(self.screen, black, (column * self.SCREEN_WIDTH/4, 0), (column * self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT))

    self.screen.update()

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

        """
    def ClickedOn(self, surface):
        action = False
      
        if the position of the mouse is within the button, 
        and if the mouse button 1 (0 basically) is pressed,
        clicked = true
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicks = True
                print("CLICKED")
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action
        """

