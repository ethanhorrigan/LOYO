import math

class Elo:
    """
    Elo Class is an Implementation of the ELo rating system.
    Updates the users rating after a game depending on the game outcome.
    """

    """
    What do i need?

    - List of players for Team 1 or Team 2
    - Average MMR for both teams.
    - The players rating (for each player)
    - compare ratings 
    - 1v1:
    - Both players MMR
    - The players Rating
    - Calculate Rating
    - Output rating
    """

    # The K-factor used by the USCF (United States Chess Federation)
    # The average ratings for chess players:
    # In general, 
    # a beginner (non-scholastic) is 800, 
    # the average player is 1500 
    # professional level is 2200.
    def k_factor(self, totalPlayed, gamesPlayed):
        return 800 / (totalPlayed + gamesPlayed)

    # i only want to update rating for the winning player or team
    def calculate_new_rating(self, winners_rating, losers_rating):
        """
        I know that the subject won, so outcome computation 
        is not needed.
        Therefore, i only need to get the rating for the winning team/player.
        Update rating for new player, accordingly.

        Score Results:
        0 : Loss
        1 : Win
        Score result will always be 1, because i am only updating winners rating.
        """
        # Calcuate the expected rating for the winning player.
        expected_rating = self.expect_result(losers_rating, winners_rating)
        k = self.k_factor(0, 5)
        print(k)
        # Calculate the updated rating for the winning player.
        new_rating = winners_rating + k * (1 - expected_rating)
        new_rating = str(new_rating).split('.')[0]
        return int(new_rating)

    def expect_result(self, opponent_rating, player_rating):
        """
        Calculates the expected result for the winning player based
        off the opponents current rating.

        Equation:
        # Ea = 1 / 1+10**(Rb - ra) / 400
        """
        Ea = 1 / (1 + 10**( (opponent_rating - player_rating) /400))
        return Ea

    # https://realpython.com/python-rounding/
    def round_down(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier

e = Elo()
print(e.calculate_new_rating(700, 1000))