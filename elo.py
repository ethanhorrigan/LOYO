import math

class Elo:
    """
    Elo Class is an Implementation of the Elo rating system.
    Updates the users rating after a game depending on the game outcome.
    """

    """
    What do i need?
    - Players Games in this Tournament
    - Players total games on league
    """

    def __init__(self, player_rating, losers_rating, total_played_lol, games_played):
        self.player_rating = player_rating
        self.losers_rating = losers_rating
        self.total_played_lol = total_played_lol
        self.games_played = games_played

    # The K-factor used by the USCF (United States Chess Federation)
    # The average ratings for chess players:
    # In general, 
    # a beginner (non-scholastic) is 800, 
    # the average player is 1500 
    # professional level is 2200.
    def k_factor(self):
        return self.player_rating / (self.total_played_lol + self.games_played)

    # i only want to update rating for the winning player or team
    def calculate_new_rating(self):
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
        expected_rating = self.expect_result()
        k = self.k_factor()
        # Calculate the updated rating for the winning player.
        new_rating = self.player_rating + k * (1 - expected_rating)
        new_rating = str(new_rating).split('.')[0]
        return int(new_rating)

    def expect_result(self):
        """
        Calculates the expected result for the winning player based
        off the opponents current rating.

        Equation:
        # Ea = 1 / 1+10**(Rb - ra) / 400
        """
        Ea = 1 / (1 + 10**( (self.losers_rating - self.player_rating) /400))
        return Ea