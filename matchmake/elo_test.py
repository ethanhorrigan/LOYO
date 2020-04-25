from elo import Elo

e = Elo(1000, 1000, 64, 1)
rating = e.calculate_new_rating()
print(rating)