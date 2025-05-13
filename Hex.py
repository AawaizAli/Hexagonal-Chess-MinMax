class Hex():
    def __init__(self, row, col, piece):
        """
        Initializes a Hex object with the specified row, column, and piece.

        Args:
            row (int): The row of the Hex object.
            col (int): The column of the Hex object.
            piece (str): The piece on the Hex object.

        """
        self.row = row
        self.col = col
        self.piece = piece

    def set_row(self, row):
        """
        Sets the row of the Hex object.

        Args:
            row (int): The new row value.

        """
        self.row = row
    
    def get_row(self):
        """
        Returns the row of the Hex object.

        Returns:
            int: The row of the Hex object.

        """
        return self.row

    def set_col(self, col):
        """
        Sets the column of the Hex object.

        Args:
            col (int): The new column value.

        """
        self.col = col

    def get_col(self):
        """
        Returns the column of the Hex object.

        Returns:
            int: The column of the Hex object.

        """
        return self.col

    def set_piece(self, piece):
        """
        Sets the piece on the Hex object.

        Args:
            piece (str): The new piece value.

        """
        self.piece = piece

    def get_piece(self):
        """
        Returns the piece on the Hex object.

        Returns:
            str: The piece on the Hex object.

        """
        return self.piece
