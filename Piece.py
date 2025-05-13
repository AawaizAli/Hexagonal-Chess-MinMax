from Move import Move

class Piece():
    """
    Represents a chess piece.

    Attributes:
        color (str): The color of the piece.
        value (int): The value of the piece.
        index (int): The index of the piece.

    Methods:
        set_color(color): Sets the color of the piece.
        get_color(): Returns the color of the piece.
    """

    def __init__(self, color, index=None):
        """
        Initializes a new instance of the Piece class.

        Args:
            color (str): The color of the piece.
            index (int, optional): The index of the piece. Defaults to None.
        """
        self.color = color
        self.value = 0
        self.index = index

    def set_color(self, color):
        """
        Sets the color of the piece.

        Args:
            color (str): The color of the piece.
        """
        self.color = color
    
    def get_color(self):
        """
        Returns the color of the piece.

        Returns:
            str: The color of the piece.
        """
        return self.color

    def __lt__(self, other):
        """
        Less than comparison operator.

        Args:
            other (Piece): The other piece to compare with.

        Returns:
            bool: True if the value of this piece is less than the value of the other piece, False otherwise.
        """
        if isinstance(other, Piece):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        """
        Less than or equal to comparison operator.

        Args:
            other (Piece): The other piece to compare with.

        Returns:
            bool: True if the value of this piece is less than or equal to the value of the other piece, False otherwise.
        """
        if isinstance(other, Piece):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        """
        Greater than comparison operator.

        Args:
            other (Piece): The other piece to compare with.

        Returns:
            bool: True if the value of this piece is greater than the value of the other piece, False otherwise.
        """
        if isinstance(other, Piece):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        """
        Greater than or equal to comparison operator.

        Args:
            other (Piece): The other piece to compare with.

        Returns:
            bool: True if the value of this piece is greater than or equal to the value of the other piece, False otherwise.
        """
        if isinstance(other, Piece):
            return self.value >= other.value
        return NotImplemented

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.en_passant = False
        self.value = 10 if self.color == "white" else -10
        self.name = "p" if self.color == "white" else "P"
        self.total_moves = 0
    
    def _get_legal_moves(self, row, col, hexboard):
        """
        Get the legal moves for the piece at the specified position on the hexagonal board.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            hexboard (HexBoard): The hexagonal board object.

        Returns:
            list: A list of Move objects representing the legal moves for the piece.
        """
        moves = []

        # Check if there is an empty space two rows above (for white) or two rows below (for black)
        target = (row - 2, col) if self.color == "white" else (row + 2, col)
        if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
            piece_on_target = hexboard.get_piece(target[0], target[1])
            if piece_on_target is None:
                move = Move(self, (row, col), target, None)
                moves.append(move)
        
        # Check if it's the first move and there are empty spaces four rows above (for white) or four rows below (for black)
        if self.first_move:
            target_first_move = (row - 4, col) if self.color == "white" else (row + 4, col)
            if 0 <= target_first_move[0] < 21 and 0 <= target_first_move[1] < 11 and hexboard.get_hexagon(target_first_move[0], target_first_move[1]) is not None:
                piece_on_target_first_move = hexboard.get_piece(target_first_move[0], target_first_move[1])
                if piece_on_target is None and piece_on_target_first_move is None:
                    move = Move(self, (row, col), target, None)
                    moves.append(move)
        
        # Check if there is an opponent's piece one row above and one column to the left (for white) or one row below and one column to the right (for black)
        target = (row - 1, col - 1) if self.color == "white" else (row + 1, col + 1)
        if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
            piece_on_target = hexboard.get_piece(target[0], target[1])
            if piece_on_target is not None and piece_on_target.color != self.color:
                move = Move(self, (row, col), target, piece_on_target)
                moves.append(move)
        
        # Check if there is an opponent's piece one row above and one column to the right (for white) or one row below and one column to the left (for black)
        target = (row - 1, col + 1) if self.color == "white" else (row + 1, col - 1)
        if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
            piece_on_target = hexboard.get_piece(target[0], target[1])
            if piece_on_target is not None and piece_on_target.color != self.color:
                move = Move(self, (row, col), target, piece_on_target)
                moves.append(move)

        return moves

    def set_en_passant(self, en_passant):
        self.en_passant = en_passant
    
    def get_en_passant(self):
        return self.en_passant
    
    def set_first_move(self, first_move):
        self.first_move = first_move
    
    def get_first_move(self):
        return self.first_move

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 30 if self.color == "white" else -30
        self.name = "n" if self.color == "white" else "N"
        self.directions = [
            (-5, -1), (-4, -2), (-5, 1), (-4, 2),
            (-1, 3), (1, 3), (1, -3), (-1, -3),
            (5, -1), (4, -2), (5, 1), (4, 2)
        ]
    
    def _get_legal_moves(self, row, col, hexboard):
        """
        Get the legal moves for the piece at the specified position on the hexagonal board.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            hexboard (HexBoard): The hexagonal board object.

        Returns:
            list: A list of Move objects representing the legal moves for the piece.
        """
        moves = []
        for direction in self.directions:
            target = (row + direction[0], col + direction[1])
            if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                piece_on_target = hexboard.get_piece(target[0], target[1])
                if piece_on_target is None or piece_on_target.color != self.color:
                    move = Move(self, (row, col), target, piece_on_target)
                    moves.append(move)

        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 30 if self.color == "white" else -30
        self.name = "b" if self.color == "white" else "B"
        self.directions = [(-3, -1), (-3, 1), (3, -1), (3,1), (0,2), (0,-2)]
    
    def _get_legal_moves(self, row, col, hexboard):
        """
        Get the legal moves for the piece at the specified position on the hexagonal board.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            hexboard (HexBoard): The hexagonal board object.

        Returns:
            list: A list of Move objects representing the legal moves for the piece.
        """
        moves = []

        for direction in self.directions:
            counter = 1
            while True:
                target = (row + counter * direction[0], col + counter * direction[1])
                if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                    piece_on_target = hexboard.get_piece(target[0], target[1])
                    if piece_on_target is None:
                        move = Move(self, (row, col), target, piece_on_target)
                        moves.append(move)
                    else:
                        if piece_on_target.color != self.color:
                            move = Move(self, (row, col), target, piece_on_target)
                            moves.append(move)
                        break   
                    counter += 1
                else:
                    break
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 50 if self.color == "white" else -50
        self.name = "r" if self.color == "white" else "R"
        self.directions = [(-1, -1), (2,0), (1, 1), (-1,1), (-2,0), (1,-1)]
    
    def _get_legal_moves(self, row, col, hexboard):
        """
        Get the legal moves for the piece at the specified position on the hexagonal board.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            hexboard (HexBoard): The hexagonal board object.

        Returns:
            list: A list of Move objects representing the legal moves for the piece.
        """
        moves = []

        for direction in self.directions:
            counter = 1
            while True:
                target = (row + counter * direction[0], col + counter * direction[1])
                if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                    piece_on_target = hexboard.get_piece(target[0], target[1])
                    if piece_on_target is None:
                        move = Move(self, (row, col), target, piece_on_target)
                        moves.append(move)
                    else:
                        if piece_on_target.color != self.color:
                            move = Move(self, (row, col), target, piece_on_target)
                            moves.append(move)
                        break   
                    counter += 1
                else:
                    break

        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 90 if self.color == "white" else -90
        self.name = "q" if self.color == "white" else "Q"
        self.directions = [(-1, -1), (2,0), (1, 1), (-1,1), (-2,0), (1,-1), (-3, -1), (-3, 1), (3, -1), (3,1), (0,2), (0,-2)]
        
    
    def _get_legal_moves(self, row, col, hexboard):
        """
        Get the legal moves for the piece at the specified position on the hexagonal board.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            hexboard (HexBoard): The hexagonal board object.

        Returns:
            list: A list of Move objects representing the legal moves for the piece.
        """
        moves = []

        for direction in self.directions:
            counter = 1
            while True:
                target = (row + counter * direction[0], col + counter * direction[1])
                if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                    piece_on_target = hexboard.get_piece(target[0], target[1])
                    if piece_on_target is None:
                        move = Move(self, (row, col), target, piece_on_target)
                        moves.append(move)
                    else:
                        if piece_on_target.color != self.color:
                            move = Move(self, (row, col), target, piece_on_target)
                            moves.append(move)
                        break   
                    counter += 1
                else:
                    break
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 1000 if self.color == "white" else -1000
        self.name = "k" if self.color == "white" else "K"
        self.directions = [(-1, -1), (2,0), (1, 1), (-1,1), (-2,0), (1,-1), (-3, -1), (-3, 1), (3, -1), (3,1), (0,2), (0,-2)]
 
    def _get_legal_moves(self, row, col, hexboard):
        """
        Get the legal moves for the piece at the specified position on the hexagonal board.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            hexboard (HexBoard): The hexagonal board object.

        Returns:
            list: A list of Move objects representing the legal moves for the piece.
        """
        moves = []

        for direction in self.directions:
            target = (row + direction[0], col + direction[1])
            if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                piece_on_target = hexboard.get_piece(target[0], target[1])
                if piece_on_target is None or piece_on_target.color != self.color:
                    move = Move(self, (row, col), target, piece_on_target)
                    moves.append(move)

        return moves

