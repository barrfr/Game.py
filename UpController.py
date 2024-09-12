import pygame
import UpView
import UpModel


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame. QUIT:
                self.running = False