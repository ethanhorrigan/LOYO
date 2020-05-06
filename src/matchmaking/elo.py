import math

class Elo:
    """Elo Class is an Implementation of the Elo rating system.
    Updates the users rating after a game depending on the game outcome.
    This rating system is used to update players points on the platform.

    Returns:
        [int] -- the amount of points the player recieves.
    """

    def __init__(self, player_rating, losers_rating, total_played_lol, games_played):
        """Create a new instance of Elo

        Arguments:
            player_rating {int} -- the players rating (MMR)
            losers_rating {int} -- the opponents rating (MMR)
            total_played_lol {int} -- total games played in LoL
            games_played {[type]} -- total games using this platform
        """        
        self.player_rating = player_rating
        self.losers_rating = losers_rating
        self.total_played_lol = total_played_lol
        self.games_played = games_played

    def k_factor(self):
        """The K-factor used by the USCF (United States Chess Federation)
        The average ratings for chess players:
        beginner (non-scholastic) is 800, 
        average player is 1500 
        professional level is 2200.

        Returns:
            [int] -- [K Factor used to determine how much points the player gets.]
        """        
        return self.player_rating / (self.total_played_lol + self.games_played)

    def calculate_new_rating(self):
        """We only need to get the rating for the winning team/player.
        Update rating for new player, accordingly.

        Returns:
            [int] -- [the amount of points the player recieves based off the Elo System.]
        """        
        # Calcuate the expected rating for the winning player.
        expected_rating = self.expect_result()
        k = self.k_factor()
        # Calculate the updated rating for the winning player.
        new_rating = self.player_rating + k * (1 - expected_rating)
        new_rating = str(new_rating).split('.')[0]
        return int(new_rating)

    def update_points(self):
        """Calculate the players new rating and then remove that rating 
        from their previous rating, to calculate how much points they 
        recieve.

        Returns:
            updated_points : the amount of points the player recieves.
        """        
        updated_rating = self.calculate_new_rating()
        points = updated_rating - self.player_rating
        return points
        
    def expect_result(self):
        """Calcualtes the expected outcome between two participants 
        for use in the Elo System.

        Returns:
            [int] -- [Ea, the expected result]
        """        
        Ea = 1 / (1 + 10**( (self.losers_rating - self.player_rating) /400))
        return Ea

    def calculate_growth_rate(self):
        # PR = (V presetn - V pass) / v Pass x 1000
        # n = divide that by number of years (games)
        r = self.k_factor()
        current_rating = self.player_rating
        past_rating = 100
        n = self.total_played_lol
        PR = (current_rating - past_rating) / past_rating * 100
        PR = PR / n

        return PR