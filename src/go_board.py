# -*- coding: utf-8 -*-
# Go Game Board Implementation
import numpy as np
from typing import List, Tuple, Optional, Set
from enum import Enum

class Stone(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class GoBoard:
    def __init__(self, size: int = 19):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.captured_black = 0
        self.captured_white = 0
        self.move_history = []
        self.ko_position = None
        
    def is_valid_move(self, row: int, col: int, stone: Stone) -> bool:
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.board[row, col] != Stone.EMPTY.value:
            return False
        if (row, col) == self.ko_position:
            return False
        return True
    
    def place_stone(self, row: int, col: int, stone: Stone) -> bool:
        if not self.is_valid_move(row, col, stone):
            return False
        self.board[row, col] = stone.value
        self.move_history.append((row, col, stone))
        return True
    
    def get_board_state(self) -> np.ndarray:
        return self.board.copy()
