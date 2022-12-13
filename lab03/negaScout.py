import chess
from eval import getEval
# NegaScout is a variant of negamax that takes pre-found values ​​into account
# Alpha and beta "limits" for finding the best move

# There are three event options:
# 1. there is a move that is weaker than alpha - the move is worse than the ones that already exist, so it will be ignored
# 2. there is a movement that is stronger than alpha and weaker than beta - it is necessary to continue the search
# 3. there is a movement that is stronger than beta - the movement is the best found

# Negascout also uses such a principle as zero window
# This window reduces the number of possible options that will fall under the option of the development of events #2
# This allows you to find a better move faster (cut tree branches faster)

def negaScout(depth, board, alpha, beta):
    bestScore = float("-inf")
    b = beta
    if depth == 0:
        return -getEval(board)

    for move in board.legal_moves:
        board.push(move)
        score = -negaScout(depth - 1, board, -b, -alpha)

        if score > bestScore:
            if alpha < score < beta:
                bestScore = max(score, bestScore)
            else:
                bestScore = -negaScout(depth - 1, board, -beta, -score)

        board.pop()
        alpha = max(score, alpha)
        if alpha > beta:
            return alpha
        b = alpha + 1

    return bestScore
