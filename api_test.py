from riotwatcher import RiotWatcher, ApiError

watcher = RiotWatcher('RGAPI-2223bdbc-71de-4799-ad6e-7b302b7264e2')
my_region = 'euw1'
class SummmonerDetails():
    def get_total_games(self):
        wins = watcher.league.by_summoner(my_region, self)
        print(wins[1]['wins'])
        print(wins[1]['losses'])
        return wins
    
    
print(SummmonerDetails.get_total_games('S0jR27E9QooVBVvqtkdwPLlsQOTDxtpUw6eqA_VFFw6L8arm'))


