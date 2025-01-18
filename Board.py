import random


class Board:

    def __init__(self, n, t):
        """
        Constructor
        :param n: Length/Size of the box in integers (needs to be positive)
        :param t: Length of the treasure (needs to be positive)
        """
        if n <= 0 or t <= 0:
            raise ValueError("Only positive integers")

        self.layoutSize = n
        self.treasureNumber = t

        self.board = [['_' for col in range(n)] for row in range(n)] #A (n*n) board
        self.place_treasures()  #Calling place_treasures method to place treasures randomly

    def place_treasures(self):
        """
        Places treasure numbers on random places on the board
        :return: Int randomly placed values on the board
        """

        for label in range(1, self.treasureNumber + 1): #Loops till 1 to t (treasure number)
            count = label  # Space the treasure value occupy say 3 then three places on board
            placed = False

            while not placed:  # Randomly select position on board
                row = random.randint(0, self.layoutSize - 1)
                col = random.randint(0, self.layoutSize - 1)

                # Randomly decide if place treasure straight or vertically
                if random.choice([True, False]): # horizontally
                    if col + count <= self.layoutSize:
                        if all(self.board[row][col + i] == '_' for i in range(count)):
                            for i in range(count):
                                self.board[row][col + i] = str(label)
                            placed = True  #When placed successfully
                else:  # vertically
                    if row + count <= self.layoutSize:
                        if all(self.board[row + i][col] == '_' for i in range(count)):
                            for i in range(count):
                                self.board[row + i][col] = str(label)
                            placed = True

    def pick(self, row, col):
        """
        Based on the parameters value validate that these points exits, then pick the number from the board if any
        :param row: Cordinate of row to pick value from
        :param col: Cordinate of column to pick value from
        :return: the treasure of the board over their, idf any
        """
        if row < 0 or row >= self.layoutSize or col < 0 or col >= self.layoutSize:
            raise IndexError("Invalid Points, Does not exists")

        treasure = self.board[row][col] #Pick value

        if treasure != '_':
            self.board[row][col] = ' '  # Set the position with empty
            return int(treasure)
        else:
            return None

    def __str__(self):
        """
        String representation of the boards (used _ instead of spaces)
        :return: Printed board
        """
        board_str = '\n'.join(' '.join(str(item) for item in row) for row in self.board)
        return board_str