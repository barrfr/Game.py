import UpModel
import UpView
import UpController
import UpCPU
import pygame
pygame.init()
not_answered = True

if __name__ == "__main__":
    cpu = UpCPU.Minimax(["Y", "R", "B", "G"])
    model = UpModel.UpThrustBoard(cpu)
    view = UpView.View(model)
    controller = UpController.Controller(model, view)
    view.DrawMenu()

    while controller.running:
        controller.event_manager()
