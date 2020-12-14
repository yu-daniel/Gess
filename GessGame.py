# Author: Daniel Yu
# Date: 06/03/2020
# Description: a simulation of the board game - Gess, a Chess/Go variant.


class GessGame:
    """
    The GessGame class is the 'engine' of the game.

    The responsibilities of this class includes:
    1. initializes the (empty) game board
    2. add starting stones (black & white) to the board
    3. keeps track of player turns (i.e. whose turn it is..)
    4. keeps track of the game state (i.e. on-going, black wins, white wins, etc.)
    5. this class also has a method (make-move) that acts like a console 'controller'.
       it takes in move requests from the player and communicates with the
       Piece class to make a move on the board.
    6. keeps track of player lives (i.e. rings)

    The GessGame interacts with the Piece class. The GessGame checks the
    player's move inputs and if there are valid moves, then the Piece
    class will return the new coordinates for the board to be updated.
    """

    def __init__(self):
        """
        The init method initializes some of the basic components
        of the game, such as the game board itself, starting stones,
        setting initial game state (unfinished), and player starting
        color.
        """
        game_board = []

        self._game_state = "UNFINISHED"  # other options: "BLACK", "WHITE"
        self._game_board = game_board
        self._game_turn = "BLACK"  # new game's default always "BLACK"
        self._char_set = "ABCDEFGHIJKLMNOPQRST"  # possible columns (A-T)
        self._black_rings = ['L3']
        self._white_rings = ['L18']

        # initialize empty game board
        for rows in range(20):
            game_board.append([])
            for columns in range(20):
                game_board[rows].append(".")

        # initialize black and white stones to the empty game board
        num = 2
        for x in range(3):
            game_board[6][num] = 'B'
            game_board[6][-num - 1] = 'B'
            game_board[13][num] = 'W'
            game_board[13][-num - 1] = 'W'
            num += 3

        num = 2
        for x in range(3):
            game_board[1][num] = 'B'
            game_board[3][num] = 'B'
            game_board[1][-num - 1] = 'B'
            game_board[3][-num - 1] = 'B'
            game_board[16][num] = 'W'
            game_board[18][num] = 'W'
            game_board[16][-num - 1] = 'W'
            game_board[18][-num - 1] = 'W'
            num += 2

            if num == 6:
                for y in range(3):
                    game_board[1][num] = 'B'
                    game_board[3][num] = 'B'
                    game_board[1][-num - 1] = 'B'
                    game_board[3][-num - 1] = 'B'
                    game_board[16][num] = 'W'
                    game_board[18][num] = 'W'
                    game_board[16][-num - 1] = 'W'
                    game_board[18][-num - 1] = 'W'
                    num += 1

        num = 1
        for x in range(4):
            game_board[2][num] = 'B'
            game_board[2][-num - 1] = 'B'
            game_board[17][num] = 'W'
            game_board[17][-num - 1] = 'W'
            num += 1
            if x == 2:
                num += 1
            elif x == 3:
                num += 1
                for y in range(4):
                    game_board[2][num] = 'B'
                    game_board[17][num] = 'W'
                    if y == 3:
                        game_board[2][num + 2] = 'B'
                        game_board[17][num + 2] = 'W'
                    num += 1

    def get_game_state(self):
        """
        Returns the current game state.
        Mainly used for debugging in end stages of development,
        to see if methods update the game_state correctly.
        No parameters
        Returns:
            "UNFINISHED", "BLACK_WON", OR "WHITE_WON"
        """
        return self._game_state

    def get_game_board(self):
        """
        Returns the current game board.
        Used for printing the game board and seeing
        the movement of each stone.
        No parameters.
        Returns:
            the current game board
        """
        return self._game_board

    def get_game_turn(self):
        """
        Returns the current turn's player color.
        No parameters.
        Returns:
            current turn's player color
        """
        return self._game_turn

    def set_game_board(self, current_row, current_column, new_row, new_column):
        """
        Replaces the new position's content (stones) with the selected (current) content.
        Afterwards, the current position's content is emptied.
        Parameters:
            current_row = the selected Piece's row
            current_column = the selected Piece's column
            new_row = the new center's row
            new_column = the new center's column
        Returns:
            none
        """
        self._game_board[new_row][new_column] = self._game_board[current_row][current_column]
        self._game_board[current_row][current_column] = "."

    def update_game_board(self, new_board):
        """
        Receives the updated coordinates from the Piece class and set
        current game_board to new_board.
        Parameters:
            new_board = new game board with updated coordinates
        Returns:
            none
        """
        self._game_board = new_board

    def toggle_game_turn(self):
        """
        Manually switches the game's player turn to the opposite color.
        This method is mainly a tool used during debugging, to
        test functions on both player colors without needing to
        make a move to change player.
        Returns:
            none
        """
        if self._game_turn == 'BLACK':
            self._game_turn = "WHITE"

        elif self._game_turn == "WHITE":
            self._game_turn = "BLACK"

    def resign_game(self):
        """
        While the game is on-going, the current turn's player (color)
        will forfeit the match, if this function is called.
        The opposite color player will be set as winner.
        No parameters.
        Returns:
            none
        """
        if self._game_state == 'UNFINISHED':
            if self._game_turn == 'WHITE':
                self._game_state = 'BLACK_WON'
            self._game_state = 'WHITE_WON'

    def clear_edges(self):
        """
        The make-move method or the Piece's move methods don't account
        for the game's edge rules (e.g. no pieces in columns A, or T).
        This method would be added after each make-move call to
        remove all stones (if any) on the perimeter (edges) of the board.
        No parameters.
        Returns:
            none
        """
        num = 0

        for x in range(2):
            for y in range(20):
                row, num = y, num
                self.set_game_board(row, num, 0, 0)
                self.set_game_board(num, y, 0, 0)
            num += 19

    def make_move(self, current, new):
        """
        This method accepts the move inputs from each player color.
        The inputs are validated to be sure it is a legal move.
        If the move is legal, the moves' coordinates are passed to
        the Piece class' corresponding move methods to update
        the new center's footprint with the current center's footprint.
        Parameters:
            current = player's Piece's location that he/she wants to move
            new = the new location that player wants the Piece to relocate
        Returns:
            False if the player's inputs are not valid. Otherwise
            the board will update the requested stone relocation.
        """

        one = Piece(self._game_board)  # initializes the Piece class to access its set of move methods

        new_column = ord(new[0].upper()) - 64
        current_column = ord(current[0].upper()) - 64

        new_row = int(new[1:])
        current_row = int(current[1:])

        vertical_distance = int(new[1:]) - int(current[1:])  # number of tiles between the closest edge of the
        horizontal_distance = abs(new_column) - current_column

        player_turn = self._game_turn
        current_surrounding = self.list_center_stones(current)
        current_center = self._game_board[current_row - 1][current_column - 1]

        # ****************
        # Move Validations
        # ****************

        # invalid columns
        if current[0].upper() not in self._char_set or new[0].upper() not in self._char_set:
            return False

        # invalid columns
        elif current[0].upper() == 'A' or new[0].upper() == 'A':
            return False

        # invalid columns
        elif current[0].upper() == 'T' or new[0].upper() == 'T':
            return False

        # invalid rows
        elif current_row >= 20 or new_row >= 20:
            return False

        # invalid rows
        elif current_row < 2 or new_row < 2:
            return False

        # no stone for the particular direction
        elif self.direction_check(current, new) == '.':
            return False

        elif self._game_state != "UNFINISHED":
            return False

        # check if player's last ring will be broken by the move
        elif len(self._black_rings) == 1 or len(self._white_rings) == 1:
            if not self.last_ring(current, new):
                return False

        if current.upper() == new.upper():
            return False

        # prevent player from using opponent's stones
        if player_turn == 'BLACK':
            if 'W' in current_surrounding:
                return False

        elif player_turn == 'WHITE':
            if 'B' in current_surrounding:
                return False

        # disables 3x3 area if both stone colors in the area
        elif 'B' in current_surrounding and 'W' in current_surrounding:
            return False

        # selected Piece has no center stone & move is > 3 tiles
        if current_center == ".":
            if abs(vertical_distance) > 3:
                return False

            elif abs(horizontal_distance) > 3:
                return False

        # move to new center has stones preventing the path
        if not self.path_clear(current, new):
            return False

        # ****************
        # Piece Movements
        # ****************

        if current[0] == new[0]:  # vertical movement if columns are same
            if current_row < new_row:
                self.update_game_board(one.move_vertical_1(current, vertical_distance))
            elif current_row > new_row:
                self.update_game_board(one.move_vertical_2(current, vertical_distance))

        elif current[1:] == new[1:]:  # horizontal movement if rows are same
            if current_column < new_column:
                self.update_game_board(one.move_right(current, horizontal_distance))
            elif current_column > new_column:
                self.update_game_board(one.move_left(current, horizontal_distance))

        else:  # diagonal movement otherwise
            self.update_game_board(one.move_diagonal_up(current, new, horizontal_distance))

        self.toggle_game_turn()  # switch to next player color's turn
        self.clear_edges()  # clear edges around screen
        return self.ring_check()

    def direction_check(self, current, new):
        """
        This method works with make_move method to
         check if a Piece has the 'directional
        ability' to move to the new center.
        Parameters:
            current - the center to be relocated
            new - the new center for the Piece
        Returns:
        'B', 'W', or '.' of a tile
        """
        directions = self.list_center_stones(current)
        current_column = (ord(current[0].upper()) - 64) - 1
        current_row = int(current[1:].upper()) - 1

        new_column = (ord(new[0].upper()) - 64) - 1
        new_row = int(new[1:].upper()) - 1

        # directions = [NW, N, NE, E, SE, S, SW, W, centerx]

        # diagonal, bottom right
        if new_row > current_row and new_column > current_column:
            return directions[4]
        # diagonal, bottom left
        elif new_row > current_row and new_column < current_column:
            return directions[6]
        # diagonal, top right
        elif new_row < current_row and new_column > current_column:
            return directions[2]
        # diagonal, top left
        elif new_row < current_row and new_column < current_column:
            return directions[0]
        # horizontal, left
        elif new_row == current_row and new_column < current_column:
            return directions[7]
        # horizontal, right
        elif new_row == current_row and new_column > current_column:
            return directions[3]
        # vertical, up
        elif new_row < current_row and new_column == current_column:
            return directions[1]
        # vertical, down
        elif new_row > current_row and new_column == current_column:
            return directions[5]

    def ring_check(self):
        """
        Scans the board to check for player rings.
        Add newly generated ring(s) to player(s) ring total.
        Updates the game state if one player has 0 rings.
        No parameters.
        Returns:
            True
        """
        new_black_rings = self._black_rings
        new_white_rings = self._white_rings
        black_rings = []
        white_rings = []

        total_black = 0  # keep track of total rings each round
        total_white = 0
        for x in range(19):
            for y in range(20):
                surroundings = self.list_center_stones(chr(x + 65) + str(y))

                black_stones = surroundings.count('B')
                white_stones = surroundings.count('W')
                center = chr(x + 65) + str(y)
                if black_stones == 8 and surroundings[8] == '.':
                    total_black += 1
                    black_rings.append(center)
                    if center not in self._black_rings:
                        new_black_rings.append(center)
                if white_stones == 8 and surroundings[8] == '.':
                    total_white += 1
                    white_rings.append(center)
                    if center not in self._white_rings:
                        new_white_rings.append(center)

        self._black_rings = black_rings
        self._white_rings = white_rings

        # if no rings detected at end of each round, a player loses the game
        if total_black == 0:
            self._game_state = 'WHITE_WON'

        elif total_white == 0:
            self._game_state = 'BLACK_WON'

        elif not self._black_rings:
            self._game_state = 'WHITE_WON'

        elif not self._white_rings:
            self._game_state = 'BLACK_WON'

        return True

    def last_ring(self, current, new):
        """
        While the player has only one life remaining,
        this method prevent moves that break ones' own
        ring.
        Parameters:
            current - center to be relocated.
            new - the new center to move to.
        """
        new_column = new[0].upper()
        new_row = int(new[1:])

        last_black_ring = self._black_rings[0]
        last_white_ring = self._white_rings[0]

        new_surrounding = self.search_surrounding2(new)
        current_surrounding = self.search_surrounding2(current)
        black_surrounding = self.search_surrounding2(last_black_ring)
        white_surrounding = self.search_surrounding2(last_white_ring)
        overlaps = set()

        # checks if the new center's footprint overlaps with the last ring
        # prevent moves where the overlapped tiles become empty (i.e. breaks the ring)

        area = None
        last_ring = None
        for x in new_surrounding:
            if self._game_turn == 'WHITE':
                area = white_surrounding
                last_ring = last_white_ring
            elif self._game_turn == 'BLACK':
                area = black_surrounding
                last_ring = last_black_ring

        if current.upper() != last_ring:
            if x in area:
                for index, x in enumerate(new_surrounding):
                    if x in area:
                        overlaps.add(index)
                        for y in overlaps:
                            row = current_surrounding[y][0] + 1
                            column = chr(current_surrounding[y][1] + 65)
                            content = self.scan(column + str(row))
                            if content == '.':
                                return False
        # prevents last ring from moving outside of the game board
        if current.upper() in self._black_rings:
            if new_column == 'B' or new_column == 'S':
                return False
        if current.upper() in self._black_rings:
            if new_row == 2 or new_row == 19:
                return False
        if current.upper() in self._white_rings:
            if new_column == 'B' or new_column == 'S':
                return False
        if current.upper() in self._white_rings:
            if new_row == 2 or new_row == 19:
                return False

        return True

    def list_center_stones(self, center):
        """
        Takes center as the Piece center and check
        the footprint's contents (i.e. 'B', 'W', or 'empty')
        and return the results in a list.
        Parameter:
            center = the center to check for contents
        Returns:
            surrounding = a list of the footprint's content
        """

        current_column = (ord(center[0].upper()) - 64) - 1
        current_row = int(center[1:].upper()) - 1

        # calculations to get coordinates of other tiles in the
        # footprint revolves around center's (row, column)
        centerx = self._game_board[current_row][current_column]
        NW = self._game_board[current_row - 1][current_column - 1]
        N = self._game_board[current_row - 1][current_column]
        NE = self._game_board[current_row - 1][current_column + 1]
        E = self._game_board[current_row][current_column + 1]
        SE = self._game_board[current_row + 1][current_column + 1]
        S = self._game_board[current_row + 1][current_column]
        SW = self._game_board[current_row + 1][current_column - 1]
        W = self._game_board[current_row][current_column - 1]

        surrounding = [NW, N, NE, E, SE, S, SW, W, centerx]

        return surrounding

    def search_surrounding2(self, center):
        """
        Find the (row, column) indexes that circle around the selected center.
        Used in conjunction with the 'path_clear' method to search for
        obstacles between the current center's footprint and the new center.
        Parameters:
            center = player's requested Piece center location
        Returns:
             surroundings2 = a list of the coordinates (row, column)
        """
        column = ord(center[0].upper()) - 64
        row = int(center[1:])

        NorthWest = row - 2, column - 2
        North = row - 2, column - 1
        NorthEast = row - 2, column
        East = row - 1, column
        SouthEast = row, column
        South = row, column - 1
        SouthWest = row, column - 2
        West = row - 1, column - 2
        Centerx = row - 1, column - 1

        surroundings2 = [SouthWest, South, SouthEast, West, Centerx, East, NorthWest, North, NorthEast]

        return surroundings2

    def path_clear(self, current, new):
        """
        Check for stones in the movement path from 'current center' to 'new center'.
        Uses the search_surroundings2 method to find the current center's footprint
        and finds the path based on the 'difference' between current center and the
        new center.
        Parameters:
            current = current center's location
            new = new center's location
        Returns:
             True if no stones in the way, else returns False.
        """
        container = []

        new_row = int(new[1:])
        current_row = int(current[1:])

        new_column = ord(new[0].upper()) - 64
        current_column = ord(current[0].upper()) - 64

        distance = new_row - current_row
        horizontal_distance = abs(new_column) - int(current_column)
        current_surrounding = self.search_surrounding2(current)

        # vertical movements
        if current_column == new_column:

            if self._game_turn == "BLACK":
                for x in range(3):
                    num = 0
                    for y in range(1, distance):
                        row = current_surrounding[x][0] + num + 1
                        column = current_surrounding[x][1]
                        num += 1
                        if not self._game_board[row][column] == ".":
                            container.append(self._game_board[row][column])

            elif self._game_turn == "WHITE":
                for x in range(6, 9):
                    num = 1
                    for y in range(abs(distance), 1, -1):
                        row = current_surrounding[x][0] + num - 2
                        column = current_surrounding[x][1]
                        num -= 1
                        if not self._game_board[row][column] == ".":
                            container.append(self._game_board[row][column])

        # for horizontal movement
        elif current_row == new_row:
            num = -1
            for x in range(abs(horizontal_distance) - 1):

                for y in range(3):
                    row = current_surrounding[4][0] + num
                    if current_column > new_column:
                        column = current_surrounding[4][1] - horizontal_distance
                    else:
                        column = current_surrounding[4][1] + horizontal_distance
                    container.append(self._game_board[row][column])
                    num += 1
                num = -1
                horizontal_distance -= 1

        # diagonal movements
        elif current_column != new_column and current_row != new_row:
            # tiles of the footprint in the direction facing the new center
            up_right = [6, 7, 8, 5, 2]
            up_left = [8, 7, 6, 3, 0]
            down_right = [8, 5, 2, 1, 0]
            down_left = [6, 3, 0, 1, 2]
            num = 1

            # checks if the involved tiles above are obstructed by other
            # stones in the move path
            for x in range(5):
                for y in range(horizontal_distance - 1):
                    # diagonal, moving top right
                    if current_column < new_column and new_row < current_row:
                        row = current_surrounding[up_right[x]][0] - num
                        column = current_surrounding[up_right[x]][1] + num
                        container.append(self._game_board[row][column])

                    # diagonal, moving top left
                    elif current_column > new_column and new_row < current_row:
                        row = current_surrounding[up_left[x]][0] - num
                        column = current_surrounding[up_left[x]][1] - num
                        container.append(self._game_board[row][column])

                    # diagonal, moving bottom right
                    elif current_column < new_column and new_row > current_row:
                        row = current_surrounding[down_right[x]][0] + num
                        column = current_surrounding[down_right[x]][1] + num
                        container.append(self._game_board[row][column])

                    # diagonal, moving bottom left
                    elif current_column > new_column and new_row > current_row:
                        row = current_surrounding[down_left[x]][0] + num
                        column = current_surrounding[down_left[x]][1] - num
                        container.append(self._game_board[row][column])
                    num += 1
                num = 1

        if "B" in container or "W" in container:
            return False
        return True

    def scan(self, location):
        """
        Check the content of the specified location.
        *Currently this function doesn't seem to help much
        in developing the program. Might just scrap it in the end*
        Parameter:
            location = the desired location to check
        Returns:
             the content of the location/position
        """
        row = self._game_board[int(location[1:]) - 1]
        column = (ord(location[0].upper()) - 64) - 1

        return row[column]

    def is_empty(self, location):
        """
        Check to see if the location is empty (containing '.').
        Parameter:
            location = the desired location to check
        Returns:
            True, if location is empty.
            Otherwise returns False.
        """
        if self.scan(location) == ".":
            return True
        return False


class Piece(GessGame):
    """
    The Piece class controls updating all valid player move inputs.
    It works hand in hand with the GessGame class, the parent class.
    The GessGame class validates the user's inputs, and the Piece
    class executes the valid inputs.

    The Piece class has a variety of move methods, where the specialty
    depends on the direction of stone movement/relocation.
    """

    def __init__(self, old_board):
        super().__init__()
        self._game_board = old_board

    def move_vertical_1(self, current, vertical_distance):
        """
        Replaces the new center's footprint with the current center's
        footprint. In the 3x3 footprint, the bottom row is added first,
        followed by middle, and top.
        Parameters:
            current = current center's location/coordinate
            vertical_distance = difference (tiles away) between
            the current center's row and new center's row
        Returns:
            an updated game board back to the GessGame class.
            If nothing is returned, then the updates won't take effect.
        """
        surrounding = self.search_surrounding2(current)

        for x in range(9):
            # the variable names' are kind of vague, but I'll update at the end
            num1 = surrounding[x][0]
            num2 = surrounding[x][1]
            num3 = surrounding[x][0] + vertical_distance
            num4 = surrounding[x][1]
            self.set_game_board(num1, num2, num3, num4)
        return self.get_game_board()

    def move_vertical_2(self, current, vertical_distance):
        """
        Replaces the new center's footprint with the current center's
        footprint. In the 3x3 footprint, the top row is added first,
        followed by middle, and lastly bottom.
        Parameters:
            current = current center's location/coordinate
            vertical_distance = difference (tiles away) between
            the current center's row and new center's row
        Returns:
            an updated game board back to the GessGame class.
        """
        surrounding = self.search_surrounding2(current)

        for x in range(8, -1, -1):
            num1 = surrounding[x][0]
            num2 = surrounding[x][1]
            num3 = surrounding[x][0] + vertical_distance
            num4 = surrounding[x][1]
            self.set_game_board(num1, num2, num3, num4)
        return self.get_game_board()

    def move_right(self, current, horizontal_distance):
        """
        Replaces the new center's footprint with the current center's
        footprint. In the 3x3 footprint, the top row is added first,
        followed by middle, and lastly bottom.
        Parameters:
            current = current center's location/coordinate
            vertical_distance = difference (tiles away) between current center's column
             and new center's column
        Returns:
            an updated game board back to the GessGame class.
        """
        surrounding = self.search_surrounding2(current)

        for x in range(8, -1, -1):
            num1 = surrounding[x][0]
            num2 = surrounding[x][1]
            num3 = surrounding[x][0]
            num4 = surrounding[x][1] + horizontal_distance
            self.set_game_board(num1, num2, num3, num4)
        return self.get_game_board()

    def move_left(self, current, horizontal_distance):
        """
        Replaces the new center's footprint with the current center's
        footprint. In the 3x3 footprint, the left column is added first,
        followed by middle, and lastly right column.
        Parameters:
            current = current center's location/coordinate
            vertical_distance = difference (tiles away) between current center's column
             and new center's column
        Returns:
            an updated game board back to the GessGame class.
        """
        surrounding = self.search_surrounding2(current)

        for x in range(3):
            for y in range(6 + x, -3 + x, -3):
                num1 = surrounding[y][0]
                num2 = surrounding[y][1]
                num3 = surrounding[y][0]
                num4 = surrounding[y][1] + horizontal_distance
                self.set_game_board(num1, num2, num3, num4)
        return self.get_game_board()

    def move_diagonal_up(self, current, new, horizontal_distance):
        """
        Replaces the new center's footprint with the current center's footprint
        for a Piece that aims to relocate top right or top left of the game board.
        Like the other move methods, this one would also use the search_surroundings2
        method to search for the center's footprint and add each of it's component
        to the new location.
        Parameters:
            current = current center's location/coordinate
            horizontal_distance = difference between the current center's row and
            the new center's row.
            vertical_distance = difference (tiles away) between current center's column
             and new center's column
        Returns:
            an updated game board back to the GessGame class.
        """
        new_column = ord(new[0].upper()) - 64
        new_row = int(new[1:])

        current_column = ord(current[0].upper()) - 64
        current_row = int(current[1:])

        surrounding = self.search_surrounding2(current)

        # moving bottom left
        if new_column < current_column and new_row > current_row:
            for x in range(9):
                num1 = surrounding[x][0]
                num2 = surrounding[x][1]
                num3 = surrounding[x][0] + abs(horizontal_distance)
                num4 = surrounding[x][1] - abs(horizontal_distance)
                self.set_game_board(num1, num2, num3, num4)

        # moving bottom right
        elif new_column > current_column and new_row > current_row:

            for x in range(9):
                num1 = surrounding[x][0]
                num2 = surrounding[x][1]
                num3 = surrounding[x][0] + horizontal_distance
                num4 = surrounding[x][1] + horizontal_distance
                self.set_game_board(num1, num2, num3, num4)

        # moving top left
        elif new_column < current_column:
            for x in range(8, -1, -1):
                num1 = surrounding[x][0]
                num2 = surrounding[x][1]
                num3 = surrounding[x][0] - abs(horizontal_distance)
                num4 = surrounding[x][1] - abs(horizontal_distance)
                self.set_game_board(num1, num2, num3, num4)

        # moving top right
        else:
            for x in range(8, -1, -1):
                num1 = surrounding[x][0]
                num2 = surrounding[x][1]
                num3 = surrounding[x][0] - horizontal_distance
                num4 = surrounding[x][1] + horizontal_distance
                self.set_game_board(num1, num2, num3, num4)
        return self.get_game_board()
