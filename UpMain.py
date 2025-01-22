import UpModel
import UpView
import UpController
import pygame
pygame.init()
not_answered = True

if __name__ == "__main__":
    model = UpModel.UpThrustBoard()
    view = UpView.View(model)
    controller = UpController.Controller(model, view)
    view.DrawMenu()

    while controller.running:
        controller.event_manager()
