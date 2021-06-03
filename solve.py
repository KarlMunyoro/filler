from typing import Tuple, List, Type, Set, Optional
import numpy as np
from copy import deepcopy
import boards

import importlib
importlib.reload(boards)

Move = str # type alias for a move (really just a string representing a color)

class Solver:
    def __init__(self, player: int, maxdepth: int, parent_tag: Optional[str] = ""): # TODO: remove parent_tag (just for debugging)
        self.player = player
        self.maxdepth = maxdepth
        self.tag = parent_tag + str(player)
    
    def choose_move(self, board: boards.Board, depth: int) -> Optional[Move]:
        best_value = None # instantiate best value
        best_move = None # instantiate best move
        potential_moves = board.get_potential_moves(player=self.player) # gather potential moves
        if not potential_moves: # if there aren't any potential moves
            potential_moves = list(board.get_legal_moves(player=self.player))[:1] # just get the first legal move
        if depth < self.maxdepth: # if we're still looking ahead
            for move in potential_moves:
                board_after_move = board.add_move(move=move, player=self.player) # make the move
                opponent = Solver(player=1-self.player, maxdepth=self.maxdepth, parent_tag=self.tag) # spawn opponent
                opponent_move = opponent.choose_move(board=board_after_move, depth=depth+1) # find opponent's move (recurse)
                board_after_opponent_move = board_after_move.add_move(move=opponent_move, player=1-self.player) # get board after opponent's move
                move_value = board_after_opponent_move.get_board_value(player=self.player) # evaluate move
                best_move, best_value = self.update_best_move(move, move_value, best_move, best_value) # update best move/value (if this one is better)
        else: # if this is as far as we're looking ahead
            for move in potential_moves:
                board_after_move = board.add_move(move=move, player=self.player) # get the board after this move
                move_value = board.get_board_value(player=self.player) # evaluate move
                best_move, best_value = self.update_best_move(move, move_value, best_move, best_value) # update best move/value (if this one is better)
        return best_move

    def update_best_move(self, move: Move, move_value: int, best_move: Optional[Move], best_value: Optional[int]) -> Tuple[Move, int]:
        if best_move is None or move_value > best_value: # if we don't have a best move or this move is better than ours
            return move, move_value # return the curernt move and its value
        else: # otherwise
            return best_move, best_value # return the old best move and its value