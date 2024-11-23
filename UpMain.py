import UpModel
import UpView
import UpController
import pygame
pygame.init()
not_answered = True

#stupid minimax is moving its own piece one tile up when the piece is the most advanced piece
#need to make it such that theres a new list that adds the untaken colour into each player's number

if __name__ == "__main__":
    #print("game ran")
    model = UpModel.UpThrustBoard()
    view = UpView.View(model)
    controller = UpController.Controller(model, view)
    view.DrawMenu()

    while controller.running:
        controller.event_manager()
