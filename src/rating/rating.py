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