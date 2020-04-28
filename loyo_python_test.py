
from api import PasswordSetup, Summoner
import api
import unittest

class SimpleTest(unittest.TestCase):
    """Conducts tests for the back-end of the application

    Arguments:
        unittest -- using pythons unnitest lib for unit testing.
    """    
    def test_get_tier(self):
        self.assertEqual(Summoner.get_tier('Yupouvit'), 'GOLD')

    def test_get_rank(self):
        self.assertEqual(Summoner.get_rank('Yupouvit'), 1)
    
    def test_get_summoner_id(self):
        self.assertEqual(Summoner.get_player_icon('Dylan Loftus'), 1456)

    def test_summoner_name(self):
        self.assertEqual(api.SummonerName.get(self,'Ethan'), [('Dylan Loftus',)])

if __name__ == '__main__':
    unittest.main()