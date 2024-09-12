import pygame
import UpModel

run = True



pygame.init

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]

SCREEN_HEIGHT = 550
SCREEN_WIDTH = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class View:

  def __init__(self, model):
    self.model = model

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
    UpModel.UpThrustBoard.getBoard()
    for i in range(0, 5):
      y = SCREEN_HEIGHT - (i * SCREEN_HEIGHT/11 - SCREEN_HEIGHT/22)
      x = (i * SCREEN_WIDTH/4 - SCREEN_WIDTH/8)
      
      """circle(surface, color, center, radius)"""
      pygame.draw.circle(screen, red, (x, y), 5)

