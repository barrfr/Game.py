import UpModel
import UpView
import UpController
import pygame
pygame.init
not_answered = True

if __name__ == "__main__":
    model = UpModel.UpThrustBoard()
    view = UpView.View(model)
    controller = UpController.Controller(model, view)
    view.draw_menu

while controller.running:
    controller.event_manager()








"""
    while controller.running:
        controller.event_manager()
        view
        pygame.display.update()
        not_answered = True
        while not_answered:
            #take inputs
            InputX = int(input('X Input: '))
            InputY1 = int(input('Y1 Input: '))
            InputY2 = int(input('Y2 Input: '))
            #calculate if the move is legal and hence make the move
            if model.legalmove(InputX, InputY1, InputY2):
                model.MakeMove(InputX, InputY1, InputY2)
                not_answered = False
        
        UpView.screen.fill([255, 255, 255])
        UpView.View(model).draw_board
        UpView.View(model).draw_pieces
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
"""

