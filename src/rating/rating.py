
def get_average_mmr(mmr_list):
    """calculates the average mmr by adding mmr of all team members
    and dividing by the number of paricipants.
       
    Arguments:
        mmr_list [list] -- list of ratings

    Returns:
        [int] -- [the average mmr (rating)]
    """    
    total_mmr = sum(mmr_list)
    
    avg_mmr = (total_mmr / len(mmr_list))

    avg_mmr = str(avg_mmr).split('.')[0]
    return int(avg_mmr)


def calculate_growth_rate(self, current_rating, no_of_games):
    """calculates the growth to enhance the matchmaking algorithm

    Arguments:
        current_rating [int] -- the players current rating (mmr)
        no_of_games [int] -- [the total number of games for a player]

    Returns:
        [int] -- [mmr with appended growth rate]
    """    
    # PR = (V presetn - V pass) / v Pass x 1000
    # n = divide that by number of (games)
    past_rating = 100
    n = no_of_games
    PR = (current_rating - past_rating) / past_rating * 100
    PR = PR / n

    return PR