from elo import Elo

e = Elo()
print(e.calculate_new_rating(1000, 1000, 64, 1))
print(e.calculate_new_rating(500, 500, 25, 1))