from typing import Tuple, List, Type, Set, Optional
import boards

Move = str # type alias for a move (really just a string representing a color)

class Solver:
    def __init__(self, player: int, maxdepth: int):
        self.player = player
        self.maxdepth = maxdepth
    
    def choose_move(self, board: boards.Board, depth: int) -> Tuple[Move, int]:
        best_value = None # instantiate best value
        best_move = None # instantiate best move
        potential_moves = board.get_potential_moves(player=self.player) # gather potential moves
        if not potential_moves: # if there aren't any potential moves
            potential_moves = list(board.get_legal_moves(player=self.player))[:1] # just get the first legal move
        if depth < self.maxdepth: # if we're still looking ahead
            for move in potential_moves:
                board_after_move = board.add_move(move=move, player=self.player) # make the move
                opponent = Solver(player=1-self.player, maxdepth=self.maxdepth) # spawn opponent
                opponent_move, opponent_value = opponent.choose_move(board=board_after_move, depth=depth+1) # find opponent's move (recurse)
                move_value = -opponent_value # value for this move is opposite of opponent's move
                if best_value is None or move_value > best_value: # if this beats our old best,
                    best_move, best_value = move, move_value # save it as the best move
        else: # if this is as far as we're looking ahead
            for move in potential_moves:
                board_after_move = board.add_move(move=move, player=self.player) # get the board after this move
                move_value = board.get_board_value(player=self.player) # evaluate move
                if best_value is None or move_value > best_value: # if this beats our old best,
                    best_move, best_value = move, move_value # save it as the best move
        return best_move, best_value