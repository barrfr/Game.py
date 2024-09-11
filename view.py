import pygame

black = [0, 0, 0]
white = [255, 255, 255]

class View():

  def __init__(self, x, y):
    SCREEN_HEIGHT = 550
    SCREEN_WIDTH = 300

  def drawBoard(self):

    #drawing the rows
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (row * SCREEN_WIDTH/11, 0), (row * SCREEN_WIDTH/11, SCREEN_HEIGHT))
    
    #drawing the columns
    for column in range(1,4):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (row * SCREEN_HEIGHT/4, 0), (row * SCREEN_HEIGHT/4, SCREEN_WIDTH))

    #drawing the pieces
    for i in range(6, 11):
      """circle(surface, color, center, radius)"""
      pygame.draw.circle(screen, white, ((i-0.5) * SCREEN_WIDTH/11, 0), ((i-0.5) * SCREEN_HEIGHT/4, SCREEN_WIDTH))

  def game(self):
    pass

screen = pygame.Surface
View.drawBoard()


