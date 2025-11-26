import cv2
import numpy as np
from PIL import Image
import time
import threading
from stockfish import Stockfish

stockfish = Stockfish(path="C:\\Users\\neong\\Downloads\\stockfish\\stockfish\\stockfish-windows-x86-64-avx2.exe", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})

{
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
    "Ponder": False,
    "Hash": 16, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": False,
    "UCI_LimitStrength": False,
    "UCI_Elo": 1350
}
stockfish.set_fen_position(stockfish.get_fen_position())

legal_moves = [m['Move'] for m in stockfish.get_top_moves(40)]  
print("Top moves:", legal_moves)

move = "e2e4"

if move in legal_moves:
    stockfish.make_moves_from_current_position([move])
    print(stockfish.get_board_visual())
else:
    print("Illegal move!")