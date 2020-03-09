from src.watchTest import Summoner
from api import PasswordSetup
import unittest

class SimpleTest(unittest.TestCase):

    def test_get_tier(self):
        self.assertEqual(Summoner.get_tier('Yupouvit'), 'GOLD')

    def test_get_rank(self):
        self.assertEqual(Summoner.get_rank('Yupouvit'), 1)

    def test_password_create(self):
        self.assertEqual(PasswordSetup.create_password(self, '123'), '123')

if __name__ == '__main__':
    unittest.main()