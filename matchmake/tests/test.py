from matchmake.elo import Elo

e = Elo(1200, 1000, 65, 1)

e.calculate_new_rating()