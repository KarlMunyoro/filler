from typing import Tuple, List, Type, Set, Optional
from copy import deepcopy
import numpy as np

Move = str # type alias for a move (really just a string representing a color)

class Board:
    def __init__(self, ncols = 8, nrows = 7):
        self.ncols = ncols
        self.nrows = nrows
        self.board = list() # instantiate the board. Filled in with create_random()
        self.tiles = {'r','g','y','b','p','w'} # the "tiles", represented by their colors 
        self.tiles_to_colors = {'r':'🟥','g':'🟩','y':'🟨','b':'🟦','p':'🟪','w':'⬜️'} # for printing the board

    def create_random(self, seed: Optional[int] = None):
        """Create a random board"""
        # Add colors to the board
        np.random.seed(seed)
        for i in range(self.nrows):
            row = list()
            for j in range(self.ncols):
                forbidden_tiles = set()
                if i > 0:
                    forbidden_tiles.add(self.board[-1][j]) # forbid the color of the above tile
                if j > 0:
                    forbidden_tiles.add(row[-1]) # forbid the color of the leftward tile
                eligible_tiles = self.tiles - forbidden_tiles # the rest of the tiles are eligible
                row.append(np.random.choice(list(eligible_tiles))) # add this color
            self.board.append(row) # add this row to the board

        # Assign corner tiles to players
        self.player_board = [[None for j in range(self.ncols)] for i in range(self.nrows)] # instantiate player board
        self.player_board[-1][0] = 0 # bottom left is player 0
        self.player_board[0][-1] = 1 # top right is player 1

    def add_move(self, move: str, player: int):
        """Returns a new board with a move made by a given player"""
        new_board = Board()
        new_board.board = deepcopy(self.board) # add_move is called for all potential moves. Don't want to affect original board
        new_board.player_board = deepcopy(self.player_board) # see above
        for i in range(self.nrows):
            for j in range(self.ncols):
                if new_board.player_board[i][j] == player: # if this tile is controlled by the player
                    new_board.board[i][j] = move # set the tile's color equal to the color of the move
                    if i > 0 and new_board.player_board[i-1][j] is None and new_board.board[i-1][j] == move: # usurp above tile  
                        new_board.player_board[i-1][j] = player
                    if i+1 < self.nrows and new_board.player_board[i+1][j] is None and new_board.board[i+1][j] == move: # usurp below tile  
                        new_board.player_board[i+1][j] = player
                    if j > 0 and new_board.player_board[i][j-1] is None and new_board.board[i][j-1] == move: # usurp leftward tile  
                        new_board.player_board[i][j-1] = player
                    if j+1 < self.ncols and new_board.player_board[i][j+1] is None and new_board.board[i][j+1] == move: # usurp rightward tile  
                        new_board.player_board[i][j+1] = player    
        return new_board

    def get_player_tiles(self) -> str:
        """Returns player0 and player1 tiles"""
        if self.player_board[-1][0] == 0: # if player 0 is bottom left
            return self.board[-1][0], self.board[0][-1]
        else: # if player 0 is top right
            return self.board[0][-1], self.board[-1][0]

    def get_board_value(self, player: int) -> int:
        """Returns the value of the board for a given player"""
        player_value = sum(self.player_board[i].count(player) for i in range(self.nrows))
        opponent_value = sum(self.player_board[i].count(1-player) for i in range(self.nrows))
        return player_value - opponent_value

    def moves_remaining(self, player: int, player_0_tile: str, player_1_tile: str) -> bool: # TODO: needed? already have get_potential_moves
        """Checks whether there are any remaining moves for a given player"""
        player_tiles = {player_0_tile, player_1_tile}
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.player_board[i][j] == player:
                    if i > 0 and self.player_board[i-1][j] is None and self.board[i-1][j] not in player_tiles:
                        return True
                    if i+1 < self.nrows and self.player_board[i+1][j] is None and self.board[i+1][j] not in player_tiles:
                        return True
                    if j > 0 and self.player_board[i][j-1] is None and self.board[i][j-1] not in player_tiles:
                        return True
                    if j+1 < self.ncols and self.player_board[i][j+1] is None and self.board[i][j+1] not in player_tiles:
                        return True
        return False

    def get_potential_moves(self, player: int) -> Set[str]: 
        """Returns the set of potential moves for the given player.
           NOTE: this only includes moves that would add at least 1 tile"""
        potential_moves = set()
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.player_board[i][j] == player: # if this tile is controlled by the player
                                                      # add adjacent tiles not already controlled 
                    if i > 0 and self.player_board[i-1][j] is None:
                        potential_moves.add(self.board[i-1][j])
                    if i+1< self.nrows and self.player_board[i+1][j] is None:
                        potential_moves.add(self.board[i+1][j])
                    if j > 0 and self.player_board[i][j-1] is None:
                        potential_moves.add(self.board[i][j-1])
                    if j+1 < self.ncols and self.player_board[i][j+1] is None:
                        potential_moves.add(self.board[i][j+1])
        player_0_tile, player_1_tile = self.get_player_tiles() # subtract tiles the players currently have
        return potential_moves - {player_0_tile, player_1_tile}

    def get_legal_moves(self, player: int) -> Set[str]:
        """Returns moves the player could legally make
           NOTE: this is called if there aren't any 'potential moves'—
           moves that would add at least 1 tile"""
        player_0_tile, player_1_tile = self.get_player_tiles()
        return self.tiles - {player_0_tile, player_1_tile} # return all tiles other than the current ones

    def game_over(self) -> bool:
        """Returns whether or not game is over (all player_board positions filled)"""
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.player_board[i][j] is None:
                    return False
        return True

    def print_board(self):
        """Prints the board"""
        for row in self.board:
            for i, tile in enumerate(row):
                print(f"{self.tiles_to_colors[tile]}", end = "")
                if i + 1 < self.ncols:
                    print(" ", end = "")
            print("")

    def print_score(self):
        """Prints the current score"""
        p0_score = sum(self.player_board[i].count(0) for i in range(self.nrows))
        p1_score = sum(self.player_board[i].count(1) for i in range(self.nrows))
        print(f"{p0_score} to {p1_score}")