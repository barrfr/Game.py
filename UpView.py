import pygame
from UpModel import UpThrustBoard

run = True
invboard = UpThrustBoard().Board[::-1]

pygame.init
blue = [0, 0, 255]
green = [0, 255, 0]
yellow = [255, 255, 0]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]

SCREEN_HEIGHT = 550
SCREEN_WIDTH = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class View:

  def __init__(self, model, x=0, y=0):
    self.__x = x
    self.__y = y
    self.model = model
    self.draw_board()

  def draw_board(self): 
    self.drawBoard()
    for i, character in enumerate(invboard):
      for j, char in enumerate(character[::-1]):
        self.__y = SCREEN_HEIGHT - (SCREEN_HEIGHT/11)*i + SCREEN_HEIGHT/22 - SCREEN_HEIGHT/11
        self.__x = SCREEN_WIDTH - (SCREEN_WIDTH/4)*j - SCREEN_WIDTH/8 
        element = char
        self.draw_pieces(self.__x, self.__y, char) 

  def draw_pieces(self, x, y, character):
    self.__x = x
    self.__y = y

    """circle(surface, color, center, radius)"""
    if character == 'R':
      pygame.draw.circle(screen, red, (x, y), 10)

    elif character == 'G':
      pygame.draw.circle(screen, green, (x, y), 10)

    elif character == 'B':
      pygame.draw.circle(screen, blue, (x, y), 10)

    elif character == 'Y':
      pygame.draw.circle(screen, yellow, (x, y), 10)


  def get_y(self): 
    return self.__y
  def set_y(self, y):
    self.__y = y

  def get_x(self):
    return self.__x
  def set_x(self, x):
    self.__x = x

  def drawBoard(self):

    screen.fill(white)

    #drawing the rows
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (0, row * SCREEN_HEIGHT/11), (SCREEN_WIDTH, row * SCREEN_HEIGHT/11))
    
    
    #drawing the columns
    for column in range(1,4):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (column * SCREEN_WIDTH/4, 0), (column * SCREEN_WIDTH/4, SCREEN_HEIGHT))

    #drawing the pieces
    