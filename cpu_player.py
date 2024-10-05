



    
        
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

        

