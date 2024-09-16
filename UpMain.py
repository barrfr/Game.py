import UpModel
import UpView
import UpController
import pygame
not_answered = True

if __name__ == "__main__":
    model = UpModel.UpThrustBoard()
    view = UpView.View(model)
    controller = UpController.Controller()

    while controller.running:
        controller.event_manager()
            
        #take inputs
        pygame.display.update()
        InputX = int(input('X Input: '))
        InputY1 = int(input('Y1 Input: '))
        InputY2 = int(input('Y2 Input: '))
        #calculate if the move is legal and hence make the move
        if model.legalmove(InputX, InputY1, InputY2):
            model.MakeMove(InputX, InputY1, InputY2)
            UpView.View(model).draw_board()
            pygame.display.update()
        print(1)
        #makes it the next players turn
        model.CycleThruPlayerTurns()
pygame.quit()

