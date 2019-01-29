"""
CSSE1001 Assignment 2
Semester 2, 2017
"""

# Import statements go here
import a2_support
import random

# Fill these in with your details
__author__ = "Vu Anh Le (s4490763)"
__email__ = "s4490763@student.uq.edu.au"
__date__ = "01/09/2017"

# Write your classes here


class Tile(object):
    """The Tile class is used to represent a regular Scrabble tile."""

    def __init__(self, letter, score):
        """Constructor

        Parameters:
            letter (str): Letter of the tile
            score (int): Score of the tile
        """
        self.set_letter(letter)
        self.set_score(score)

    def set_letter(self, letter):
        """Sets the letter of the tile

        Parameters:
            letter (char): The letter of the tile
        """
        if (letter.isalpha() and len(letter) == 1) or letter == a2_support.WILDCARD_CHAR: 
            self._letter = letter.lower()
        else: raise ValueError(f"{letter} is not a valid letter")

    def set_score(self, score):
        """Sets the score of the tile

        Parameters:
            score (int): The score of the tile
        """
        if score >= 0: 
            self._score = score
        else: raise ValueError(f"{score} is less than 0")

    def get_letter(self):
        """(str) Returns the letter of the tile"""
        return self._letter

    def get_score(self):
        """(int) Returns the base score of the tile"""
        return self._score

    def reset(self):
        """Does nothing"""
        pass

    def __str__(self):
        """(str) Returns a string including the tile's letter and score"""
        return "{0}:{1}".format(self._letter, self._score)

    def __repr__(self):
        return self.__str__()


class Wildcard(Tile):
    """The Wildcard class is used to represent a wildcard Scrabble tile. 
    The user can choose the letter this tile represents when they play it on the board."""

    def __init__(self, score):
        """Constructor

        Parameters:
            score (int): Score of the wildcard tile
        """
        super().__init__(a2_support.WILDCARD_CHAR, score)

    def reset(self):
        """Resets this tile back to its wildcard state"""
        self._letter = a2_support.WILDCARD_CHAR


class Bonus(object):
    """Bonuses allow the score of a letter or a word to be doubled or tripled."""

    def __init__(self, value):
        """Constructor

        Parameters:
            value (int): Value of the bonus
        """
        self.set_value(value)

    def set_value(self, value):
        """Sets the value of the bonus

        Parameters:
            value (int): The value of the bonus
        """
        if value >= 1: 
            self._value = value
        else:
            raise ValueError(f"{value} is less than 1")

    def get_value(self):
        """(int) Returns the value of this bonus"""
        return self._value

    def __repr__(self):
        return "Bonus({0})".format(self.__str__())


class WordBonus(Bonus):
    def __str__(self):
        """(str) Returns a human readable string, of the form {type}{value}"""
        return "W{0}".format(self._value)


class LetterBonus(Bonus):    
    def __str__(self):
        """(str) Returns a human readable string, of the form {type}{value}"""
        return "L{0}".format(self._value)


class Player(object):
    """The Player class represents a player and their rack of tiles."""

    def __init__(self, name):
        """Constructor

        Parameters:
            name (str): Name of the player
        """
        self._tiles = []
        self._score = 0
        self._name = name

    def get_name(self):
        """(str) Return's the player's name"""
        return self._name

    def add_tile(self, tile):
        """Adds a tile to the player's rack

        Parameters:
            tile (Tile): The tile object to be added
        """
        if len(self) < a2_support.MAX_LETTERS:
            self._tiles.append(tile)
        else:
            raise IndexError(f"Player already has the maximum number of tiles")

    def remove_tile(self, index):
        """(Tile) Removes the tile at index from the player's rack
        and return the removed tile

        Parameters:
            index (int): The index of the tile
        """
        return self._tiles.pop(index)

    def get_tiles(self):
        """(list<Tile>) Returns all tiles in the player's rack"""
        return self._tiles

    def get_score(self):
        """Return's the player's score"""
        return self._score
        
    def add_score(self, score):
        """Adds score to the player's total score
        
        Parameters:
            score (int): Number of score to be added
        """
        if score >= 0:
            self._score += score
        else:
            raise ValueError(f"{score} is less than 0")

    def get_rack_score(self):
        """(int) Returns the total score of all letters in the player's rack"""
        return sum(tile.get_score() for tile in self._tiles)

    def reset(self):
        """Resets the player for a new game, emptying their rack and clearing their score"""
        self._tiles = []
        self._score = 0

    def __contains__(self, tile):
        """(bool) Returns True if the player has tile in their rack

        Parameters:
            tile(Tile): The tile to be checked
        """
        return tile in self._tiles

    def __len__(self):
        """(int) Returns the number of letters in the player's rack"""
        return len(self._tiles)

    def __str__(self):
        """(str) Returns a string including the player's name and tiles"""
        return "{0}:{1}\n{2}".format(self._name, self._score,
                                     ', '.join([str(tile) for tile in self._tiles]))

    def __repr__(self):
        return "Player({0})",format(self._name)


class TileBag(object):
    """The TileBag class is used to hold Scrabble tiles."""

    def __init__(self, data):
        """Constructor, initialize tile bag and shuffer it for the first time

        Parameters:
            data (dict): Data of all tiles
        """
        self._tiles = []
        self._data = data

        # Add tiles from data to tile bag
        for letter, value in self._data.items():
            count, score = value
            for i in range(count):
                if letter == "?":
                    self._tiles.append(Wildcard(score))
                else:
                    self._tiles.append(Tile(letter, score))
        self.shuffle()

    def draw(self):
        """(Tile) Draws and returns a random tile from the bag"""
        return self._tiles.pop()

    def drop(self, tile):
        """Drops a tile into the bag

        Parameters:
            tile (Tile): The tile to be dropped
        """
        self._tiles.append(tile)

    def shuffle(self):
        """Shuffles the bag"""
        random.shuffle(self._tiles)

    def reset(self):
        """Refills the bag and shuffles it, ready for a new game"""
        self.__init__(self._data)

    def __len__(self):
        """(int) Returns the number of tiles remaining in the bag"""
        return len(self._tiles)

    def __str__(self):
        """(str) Returns all the tiles in bags, separated by a comma"""
        return ', '.join([str(tile) for tile in self._tiles])

    def __repr__(self):
        return "TileBag({})".format(len(self))


class Board(object):
    """The Scrabble tiles can be played on the Board class. 
    It also keeps track of which cells have bonuses."""

    def __init__(self, size, word_bonuses, letter_bonuses, start):
        """Constructor, initialize the board

        Parameters:
            size (int): The number of rows/columns on the board
            word_bonuses (dict): Scale and a list of positions as value
            letter_bonuses (dict): Scale and a list of positions as value
            start (tuple<row, colum>): Position of the starting cell
        """
        self._tiles = {}
        self._bonuses = {}
        self.set_size(size)
        self.set_start(start)
        self.add_bonus(word_bonuses, WordBonus)
        self.add_bonus(letter_bonuses, LetterBonus)

    def set_size(self, size):
        """Sets the size of the board

        Parameters:
            size (char): The size of the board
        """
        if size > 0: 
            self._size = size
        else:
            raise ValueError(f"{size} less than or equal 0")

    def set_start(self, start):
        """Sets the start position of the board

        Parameters:
            start (char): The start position of the board
        """
        if self.is_position_valid(start):
            self._start = start
        else:
            raise IndexError(f"{start} is not a valid position")

    def add_bonus(self, bonuses, bonus_type):
        """Add word bonuses to internal dictionary

        Parameters:
            bonuses (char): The start position of the board
            bonus_type (class): The class of the bonuses 
        """
        for value, positions in bonuses.items():
            for position in positions:
                self._bonuses[position] = bonus_type(value)

    def get_start(self):
        """(tuple<int, int>) Returns the starting position"""
        return self._start
     
    def get_size(self): 
        """(tuple<int, int>) Returns the number of (rows, columns) on the board"""
        return (self._size, self._size)
     
    def is_position_valid(self, position): 
        """(bool) Returns True if the position is valid

        Parameters:
            position (tuple<int, int>): The position to be checked
        """
        x, y = position
        return (x in range(self._size) and y in range(self._size))
    
    def get_bonus(self, position):
        """(Bonus) Returns the bonus for a position on the board, else None if there is no bonus

        Parameters
            position: (tuple<int, int>): The position on the board
        """
        return self._bonuses.get(position)

    def get_all_bonuses(self):
        """(dict<position: bonus>) Returns a dictionary of all bonuses
        keys being positions and values being the bonuses"""
        return self._bonuses

    def get_tile(self, position):
        """(Tile) Returns the tile at position, else None if no tile has been placed there yet
        
        Parameters:
            position (tuple<int, int>): The position on the board
        """
        return self._tiles.get(position)

    def place_tile(self, position, tile): 
        """Places a tile at position; raises an IndexError if position is invalid
        
        Parameters:
            position (tuple<int, int>): The position on the board
            tile (Tile): The tile to be placed
        """
        if self.is_position_valid(position):
            self._tiles[position] = tile
        else:
            raise IndexError(f"{position} is not valid position")

    def reset(self):
        """Resets the board for a new game"""
        self._tiles = {}

    def __str__(self):
        """(str) Returns all the string that display the board with tiles and bonuses"""
        output = ""
        rows, columns = self.get_size()
        
        dashed_line = "-" * 10 * columns + "-"
        # Display the board by drawing row by row
        for row in range(rows):
            output += dashed_line + "\n"
            
            # For each cell in the row
            for column in range(columns):   
                output += "| "
                cell = (row, column)
                cell_tile = str(self.get_tile(cell))
                cell_bonus = str(self.get_bonus(cell)) if self.get_bonus(cell) else ""
                output += cell_tile.ljust(4) + cell_bonus.rjust(3) + " "
            output += "|\n"

        output += dashed_line
        return output

    def __repr__(self):
        return "Board(size: {0}x{0}, start: {1}".format(self._size, self._start)


################################################################################
#                         DO NOT EDIT BELOW THIS LINE                          #
################################################################################
if __name__ == "__main__":
    print("This file should not be run directly. See scrabble.py & scrabble_gui.py")


