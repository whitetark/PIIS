import chess
import chess.svg
from negaMax import negaMax
from negaScout import negaScout
from PVS import PVS
from eval import getEval
import sys, getopt

board = chess.Board()

INFINITY = 1000000


def calculateBestMove(depth, board, searchFunc):
    legalMoves = board.legal_moves
    bestMove = None

    maxScore = -INFINITY

    for move in legalMoves:
        board.push(move)
        if searchFunc == 'negamax':
            score = negaMax(depth - 1, board)
        elif searchFunc == 'negascout':
            score = negaScout(depth - 1, board, -INFINITY, INFINITY)
        elif searchFunc == 'pvs':
            score = PVS(depth - 1, board, -INFINITY, INFINITY)
        #print()
        #print(board)
        board.pop()
        if score >= maxScore:
            print('New good move! ' + str(move.uci()) + ' with score of ' + str(score))
            maxScore = score
            bestMove = move
    return bestMove

def main(argv):
    board = chess.Board()
    searchFunc = 'pvs'

    while 1:
        cpuMove = calculateBestMove(2, board, searchFunc)
        print('CPU played ' + board.san(cpuMove))
        board.push(cpuMove)
        print(board)
        print('\na b c d e f g h')
        svg = chess.svg.board(board)
        with open('board.svg', 'w') as file:
            file.write(svg)

        move = input("Enter a move:")
        if str(move) == 'score':
            print('Current score: ' + str(getEval(board)))
            move = input("Enter a move:")
        board.push_san(str(move))

if __name__ == "__main__":
   main(sys.argv[1:])