import pygame
import UpModel

run = True

InvBoard = Board[::-1]

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

  def get_board(self): # for toher functions to get x and y, write a geta function as on topic 1 on the slides
    for i in range(len(InvBoard)):
      for j in range(len(i[::-1])):
        y = SCREEN_HEIGHT - (SCREEN_HEIGHT/11)*i + SCREEN_HEIGHT/22
        x = SCREEN_WIDTH - (SCREEN_WIDTH/4)*j - SCREEN_WIDTH/8

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
    
    for i in range(0, 5):
      y = SCREEN_HEIGHT - (i * SCREEN_HEIGHT/11 - SCREEN_HEIGHT/22)
      x = (i * SCREEN_WIDTH/4 - SCREEN_WIDTH/8)
      
      """circle(surface, color, center, radius)"""
      pygame.draw.circle(screen, red, (x, y), 5)

