import chess
import chess.engine

def getEval(board):
    engine = chess.engine.SimpleEngine.popen_uci(r'D:\WebThings\PIIS\lab03\stockfish-11-win\Windows\stockfish_20011801_x64.exe')
    score = engine.analyse(board, chess.engine.Limit(time=0.01))['score'].black().score()
    engine.quit()
    return score
