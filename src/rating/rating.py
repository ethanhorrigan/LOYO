"""
def get_average_mmr(mmr_list):
    total_mmr = 0
    for mmr in mmr_list:
        total_mmr += mmr
    
    avg_mmr = (total_mmr / len(mmr_list))

    avg_mmr = str(avg_mmr).split('.')[0]
    return int(avg_mmr)
"""

def get_average_mmr(mmr_list):
    total_mmr = sum(mmr_list)
    
    avg_mmr = (total_mmr / len(mmr_list))

    avg_mmr = str(avg_mmr).split('.')[0]
    return int(avg_mmr)


def calculate_growth_rate(self, current_rating, no_of_games):
    # PR = (V presetn - V pass) / v Pass x 1000
    # n = divide that by number of years (games)
    past_rating = 100
    n = no_of_games
    PR = (current_rating - past_rating) / past_rating * 100
    PR = PR / n

    return PR