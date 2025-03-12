import UpModel
import UpView
import UpController
import UpCPU
import pygame
pygame.init()

"""
Instantiates objects of necessary classes and draws the main menu screen, then initialises the controller in order to kickstart the game

List of variables:
cpu (object): instantiates a minimax object from upcpu to be passed into the controller. 
- parameter ["Y", "R", "B", "G"] as a placeholder for model.GameStartLogic
model (object): instantiates an UpThrustBoard object from UpModel to be passaed into the controller.
- parameter cpu so the model can access minimax and legality checking functions to control the CPU opponent and make moves
view (object): instantiates a view object from UpView to be passed into the controller.
- parameter model so that it can directly use model functions and game information from the model

"""

if __name__ == "__main__": #if UpMain.py is the executed file
    cpu = UpCPU.Minimax(["Y", "R", "B", "G"])
    model = UpModel.UpThrustBoard(cpu)
    view = UpView.View(model)
    controller = UpController.Controller(model, view, cpu)
    view.DrawMenu()

    while controller.running:
        controller.event_manager()