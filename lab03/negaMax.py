import chess
from eval import getEval
# Сalls itself recursively, but the resulting value is negated each iteration
# In this way, it is distinguished in whose favor the score goes

def negaMax(depth, board):
    bestScore = float("-inf")
    if depth == 0:
        return -getEval(board)

    for move in board.legal_moves:
        board.push(move)
        score = -negaMax(depth - 1, board)

        if score > bestScore:
            bestScore = score

        board.pop()

    return -bestScore