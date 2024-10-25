

#section d questions, they will be out of a certain number of marks, i suspect it will be a couple of section d type questions if its too hard it will be asingle 15 marker

    
        
"""
to find all the child positions of the current board position, you wanna have an "if move legal" function because:

for all (possible moves):
    IfMoveLegal():
        add to list of all possible moves 

    

then you make a second copy of the current position, and run all the moves from it

you can just take a board pos, search each element in the board for a piece, 
then calculate how far it should be moving according to the number of pieces in its lane
plug that into InputX InputY1 and InputY2
and then you can plug THAT into legalmove()

for i in board
    for index, j in enumerate(row)
        if j != ""
            if legalmove(indexJ, indexI, HowManyPiecesInRow(indexI2))
                availableMoves.append(THE ENTIRE BOARD WITH THE MakeMove[(indexJ, indexI, HowManyPiecesInRow(indexI2)])


for i in available moves
    pos = childBoard from the for statement above
    eval = minimax(pos, depth - 1, false)
    maxEval = max(maxEval, eval)
    return maxEval
"""

        
    # Darken the selected piece tile
    if self.selected_piece is not None:
        tile_width = 300 // 4
        tile_height = 550 // 11

        # Create a semi-transparent overlay (using RGBA where A is transparency)
        darken_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
        darken_surface.fill((0, 0, 0, 128))  # RGBA (black with 50% transparency)

        # Position the darken_surface on the selected tile
        posx = self.col * tile_width
        posy = self.row * tile_height

        # Blit the darkened surface onto the screen at the tile's position
        screen.blit(darken_surface, (posx, posy))

    pygame.display.update()
