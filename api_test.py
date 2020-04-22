from riotwatcher import RiotWatcher, ApiError

watcher = RiotWatcher('RGAPI-8af5f1d7-ae69-4750-82b6-6a3880750aa2')
my_region = 'euw1'
class SummmonerDetails():
    def get_total_games(self):
        wins = watcher.league.by_summoner(my_region, self)
        total_games = wins[0]['wins'] + wins[0]['losses']
        return total_games
    
    
print(SummmonerDetails.get_total_games('S0jR27E9QooVBVvqtkdwPLlsQOTDxtpUw6eqA_VFFw6L8arm'))


