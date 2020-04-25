from matchmake.elo import Elo

dir(elo)
e = Elo(1000, 1000, 64, 1)
rating = e.calculate_new_rating()
print(rating)