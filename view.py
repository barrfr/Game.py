import pygame
import model

run = True

pygame.init

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]

SCREEN_HEIGHT = 550
SCREEN_WIDTH = 300

class View:

  def __init__(self, model):
    self.model = model

  def drawBoard(self):

    #drawing the rows
    for row in range(1, 11):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (0, row * SCREEN_HEIGHT/11), (SCREEN_WIDTH, row * SCREEN_HEIGHT/11))
    
    #drawing the columns
    for column in range(1,4):
      """line(surface, color, start_pos, end_pos)"""
      pygame.draw.line(screen, black, (column * SCREEN_HEIGHT/4, 0), (column * SCREEN_HEIGHT/4, SCREEN_WIDTH))

    #drawing the pieces
    for i in range(6, 11):
      y = ((i-0.5) * SCREEN_WIDTH/11, 0)
      x = ((i-0.5) * SCREEN_HEIGHT/4, SCREEN_WIDTH)
      """circle(surface, color, center, radius)"""
      pygame.draw.circle(screen, red, (200, 200), 5)

  def game(self):
    pass

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

View = View(model)
pygame.display.set_caption("Menu")

while run:
  pygame.display.update()
  screen.fill(red)
  view = View
  view.drawBoard()

