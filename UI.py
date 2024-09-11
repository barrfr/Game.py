from pdb import run
from textwrap import fill
from turtle import update
import pygame
import random
pygame.init() 


class Button():
    def __init__(self, x, y, image, scale):
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
        
    def ClickedOn(self, surface):
        action = False
        """
        if the position of the mouse is within the button, 
        and if the mouse button 1 (0 basically) is pressed,
        clicked = true
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("CLICKED")
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
    
class Photo():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        pygame.Surface.blit(screen, self.image, (x, y))
        

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("holiday work")
background = (255, 255, 255)

x, y = pygame.mouse.get_pos()

run = True

active_box = None
boxes = []

screen.fill((background))

start_img_circle = pygame.image.load("Start_Button_Circle.png").convert_alpha()

grey_img = pygame.image.load("Grey_Square.png").convert_alpha()

#menu sprites
menu_start_img = pygame.image.load("Start_Button.png").convert_alpha()
menu_exit_img = pygame.image.load("Exit_Button.png").convert_alpha()

#play sprites
play_start_img = pygame.image.load("Saw_Icon.png").convert_alpha()
play_exit_img = pygame.image.load("Small Exit.png").convert_alpha()
play_saw_img = pygame.image.load("Saw_Icon.png").convert_alpha()


def play():
    global run
    pygame.display.set_caption("Play")
    
    small_exit_button = Button(0, 500, play_exit_img, 0.2)
    pygame.Surface.blit(screen, grey_img, (0, 0))
    saw_photo = Photo(250, 100, play_saw_img, 0.2)
    
    #programming the exit button
    while run:
        pygame.display.update()
        for event in pygame.event.get():
             if small_exit_button.ClickedOn(screen) == True:
                    print("EXIT")
                    main_menu()
    

def main_menu():
    global active_box
    global run
    pygame.Surface.blit(screen, grey_img, (0, 0))
    pygame.display.set_caption("Menu")
    
    start_button = Button(250, 100, menu_start_img, 0.2)
    exit_button = Button(250, 300, menu_exit_img, 0.5)

    while run:
        pygame.display.update()
        
        if start_button.ClickedOn(screen) == True:
            print("START")
            play()

        if exit_button.ClickedOn(screen) == True:
            print("EXIT")
            run = False
    #CLICK
        for event in pygame.event.get():
            #gets coordinates of a click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                
                if event.button == 1:
                    for num, box in enumerate(boxes):
                        if box.collidepoint(event.pos):
                            active_box = num
                            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_box = None
                        
            if event.type == pygame.MOUSEMOTION:
                if active_box != None:
                    boxes[active_box].move_ip(event.rel)
            if event.type == pygame.QUIT:
                pygame.display.update()
                run = False
    pygame.quit()
    

main_menu()