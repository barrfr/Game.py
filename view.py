import pygame

black = [0, 0, 0]

class View(self):

  def __init__(self, x, y):
    SCREEN_HEIGHT = 550
    SCREEN_WIDTH = 300

  def drawBoard(self):
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (row * SCREEN_WIDTH/11, 0), (row * SCREEN_WIDTH/11, SCREEN_HEIGHT))
    
    for column in range(1,4):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (row * SCREEN_HEIGHT/11, 0), (row * SCREEN_HEIGHT/11, SCREEN_WIDTH))

    

  def game(self):
    pass

screen = pygame.Surface


