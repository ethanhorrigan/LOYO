from elo import Elo

e = Elo()
print(e.calculate_new_rating(1000, 1000, 64, 0))
print(e.calculate_new_rating(500, 500, 64, 1))