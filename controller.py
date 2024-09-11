import pygame
import view
import model


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame. QUIT:
                self.running = False