import unittest
import contextlib
from io import StringIO
from a2 import *
from _ast import Lambda
from random import randint

# Ensure we always create the same set of "random" numbers.
RND_SEED = 10
# #######################################################


# #######################################################
class TestUtil(unittest.TestCase):
    def test_random_seed(self):
        random.seed(RND_SEED)

        i = random.randint(1,6)
        self.assertEqual(i,5,'randint A')

        i = random.randint(1,6)
        self.assertEqual(i,1,'randint B')

        i = random.randint(1,6)
        self.assertEqual(i,4,'randint C')
        
class TestTile(unittest.TestCase):
    def test_unit(self):
        self.assertRaises(ValueError, Tile('', 3))

    def test_minus(self):
        self.assertRaises(ValueError, Tile('B', -2))

    def test_getter(self):
        tile1 = Tile('m', 3)
        tile2 = Tile('d', 2)
        
        self.assertEqual(tile1.get_letter(),"m",'get_letter')
        self.assertEqual(tile1.get_score(),3,'get_score')

    def test_str(self):
        tile1 = Tile('m', 3)
        tile2 = Tile('d', 2)
        
        self.assertEqual(str(tile2),str('d:2'),'__str__')
        
    def test_print(self):
        tile1 = Tile('m', 3)
        tile2 = Tile('d', 2)
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(tile2)
        output = temp_stdout.getvalue().strip()
        assert output == 'd:2'

    def test_wildcard_repr(self):
        wild = Wildcard(0)
        self.assertEqual(str(wild),'?:0','__repr__')

    def test_wildcard_setter(self):
        wild = Wildcard(0)
        wild.set_letter('r')
        self.assertEqual(str(wild),'r:0','set_letter')

    def test_wildcard_reset(self):
        wild = Wildcard(0)
        wild.set_letter('r')
        self.assertEqual(str(wild),'r:0','set_letter')
        wild.reset()
        self.assertEqual(str(wild),'?:0','reset')
# #######################################################


# #######################################################
class TestBonus(unittest.TestCase):
    def test_double_word(self):
        double_word = WordBonus(2)
        
        self.assertEqual(double_word.get_value(),2,'get_value')
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(double_word)
        output = temp_stdout.getvalue().strip()
        assert output == 'W2'

    def test_triple_letter(self):
        triple_letter = LetterBonus(3)
        
        self.assertEqual(triple_letter.get_value(),3,'get_value')
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(triple_letter)
        output = temp_stdout.getvalue().strip()
        assert output == 'L3'
# #######################################################


# #######################################################
class TestPlayer(unittest.TestCase):
    def test_print(self):
        player = Player("Michael Scott")
        tiles = [Tile('t', 1), Tile('w', 4), Wildcard(0), Tile('s', 1), Tile('s', 1)]
        for tile in tiles: 
             player.add_tile(tile)
         
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(player)
        output = temp_stdout.getvalue().strip()
        
        self.assertEqual(output,'Michael Scott:0\nt:1, w:4, ?:0, s:1, s:1','print (a)')
            
        player.add_score(50)
        self.assertEqual(player.get_rack_score(),7,'get_rack_score (a)')
        self.assertEqual(str(player.remove_tile(1)),'w:4','remove_tile (a)')
        self.assertEqual(player.get_rack_score(),3,'get_rack_score (b)')
        self.assertEqual(len(player),4,'get_rack_score (b)')
        
        self.assertEqual(str(tile),'s:1','tile')
         
        self.assertEqual(tile in player,True,'tile in player (a)')
        self.assertEqual(str(player.remove_tile(3)),'s:1','remove_tile (b)')
        self.assertEqual(tile in player,False,'tile in player (b)')

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(player)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'Michael Scott:50\nt:1, ?:0, s:1','print (b)')
        
    def test_remove_tile(self):
        player = Player("Michael Scott")
        tiles = [Tile('t', 1), Tile('w', 4), Wildcard(0), Tile('s', 1), Tile('s', 1)]
        for tile in tiles: 
             player.add_tile(tile)
        self.assertEqual(str(type(player.remove_tile(1))),"<class 'a2.Tile'>",'remove_tile must return a Tyle object.')
# #######################################################


# #######################################################
class TestTileBag(unittest.TestCase):
    def test_print(self):
        random.seed(RND_SEED)
        
        data = {'b': (1, 5), 'z': (2, 8), 'e': (5, 1)}
        bag = TileBag(data)
        
        # instead of sorting we hardcode the random number seed. :)
        # to sort in place change to self._tile_rack.sort(... 
        # sorted_rack = sorted(key=lambda tile: tile.get_score(), reverse=False)
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(bag)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'z:8, z:8, e:1, e:1, e:1, e:1, e:1, b:5','print a')
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            for i in range(3): print(bag.draw())
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'b:5\ne:1\ne:1')
        self.assertEqual(len(bag),5,'len (a)')
        
        
        bag.drop(Wildcard(0))
        self.assertEqual(len(bag),6,'len (b)')

        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(bag)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'z:8, z:8, e:1, e:1, e:1, ?:0','drop')
        
        bag.shuffle()
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(bag)
        output = temp_stdout.getvalue().strip()
        self.assertNotEqual(output,'z:8, e:1, e:1, e:1, b:5, ?:0','shuffle')
        
        bag.reset()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(bag)
        output = temp_stdout.getvalue().strip()
        self.assertNotEqual(output,'z:8, e:1, e:1, e:1, b:5, ?:0','reset')
# #######################################################


# #######################################################
class TestBoard(unittest.TestCase):
    def test_print(self):
        random.seed(RND_SEED)
        
        word_bonuses = {2: [(2,2)], 3: [(0, 0), (0, 4), (4, 0),(4, 4)]}
        letter_bonuses = {2: [(0, 3), (4, 1)], 3: [(1, 0), (3, 4)]}
        board = Board(5, word_bonuses, letter_bonuses, (2, 2))
        
        self.assertEqual(board.get_size(),(5,5),'get_size')
        self.assertEqual(board.get_start(),(2,2),'get_start')
        self.assertEqual(board.is_position_valid((2,1)),True,'is_position_valid (A)')
        self.assertEqual(board.is_position_valid((2,8)),False,'is_position_valid (B)')
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(board)
        output = temp_stdout.getvalue().strip()
        
        validate = ""
        validate += "---------------------------------------------------\n"
        validate += "| None W3 | None    | None    | None L2 | None W3 |\n"
        validate += "---------------------------------------------------\n"
        validate += "| None L3 | None    | None    | None    | None    |\n"
        validate += "---------------------------------------------------\n"
        validate += "| None    | None    | None W2 | None    | None    |\n"
        validate += "---------------------------------------------------\n"
        validate += "| None    | None    | None    | None    | None L3 |\n"
        validate += "---------------------------------------------------\n"
        validate += "| None W3 | None L2 | None    | None    | None W3 |\n"
        validate += "---------------------------------------------------"
        
        self.maxDiff = None
        self.assertEqual(output,validate,"print")
        
        self.assertEqual(repr(board.get_bonus((2, 2))),"Bonus(W2)",'board.get_bonus')
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(board.get_bonus((2, 2)))
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'W2',"get_bonus (A)")
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(board.get_bonus((3, 4)))
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'L3',"get_bonus (B)")
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            print(board.get_bonus((1, 1)))
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output,'None',"get_bonus (C)")
        
        board.get_tile((2, 3))
        board.place_tile((2, 1), Tile('B', 3))
        board.place_tile((2, 2), Tile('A', 1))
        board.place_tile((2, 3), Tile('Z', 10))
        self.assertEqual(str(board.get_tile((2, 3))),'Z:10',"get_tile (A)")
        
        self.assertEqual(str(type(board.get_tile((2, 3)))),"<class 'a2.Tile'>","type")
        
        board.place_tile((2, 3), Tile('E', 1))
        self.assertEqual(str(board.get_tile((2, 3))),'E:1',"get_tile (B)")
# #######################################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

