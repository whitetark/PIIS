import chess
from eval import getEval
# The difference between pvs and negascout is how they are set up search in script #2
# Pvs - has two separate procedures for finding a window and for a null window
# NegaScout - has a single procedure for both cases

def PVS(depth, board, alpha, beta):
    bestScore = float("-inf")
    b = beta
    if depth == 0:
        return -getEval(board)

    for move in board.legal_moves:
        board.push(move)
        score = -PVS(depth - 1, board, -b, -alpha)
        
        if score > bestScore:
            if alpha < score < beta:
                bestScore = max(score, bestScore)
            else:
                bestScore = -PVS(depth - 1, board, -beta, -score)

        board.pop()

        if alpha > beta:
            return alpha
        b = alpha + 1

    return bestScore
