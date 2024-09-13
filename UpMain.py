import UpModel
import UpView
import UpController
import pygame


if __name__ == "__main__":
    model = UpModel.UpThrustBoard()
    view = UpView.View(model)
    controller = UpController.Controller(model, view)
    

    while controller.running:
        controller.event_manager()
        view
        pygame.display.update()


