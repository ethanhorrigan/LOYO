import requests
import json
## Get account details by providing the account name
def requestSummonerData(summonerName, APIKey):
    URL= "https://api.pandascore.co/players/" + summonerName + "?token="+APIKey
    print (URL)
    response = requests.get(URL)
    return response.json()

def requestGames(APIKey):
    URL= "https://api.pandascore.co/lol/matches/past?token="+APIKey
    print (URL)
    response = requests.get(URL)
    return response.json()

def main():
    ## Parameters
    summonerName = "faker"
    APIKey = "_jJDgPKYeCsyi7VKas3R9Zvb6eaSqFEeLkDSMl5GZEW1hjA5TEY"

    summonerData  = requestSummonerData(summonerName, APIKey)

    # Uncomment this line if you want a pretty JSON data dump
    print(json.dumps(summonerData, sort_keys=True, indent=2))

    with open('data.json', 'w') as json_file:
        json.dump(summonerData, json_file, sort_keys=True, indent=2)

    games  = requestGames(APIKey)

    # Uncomment this line if you want a pretty JSON data dump
    print(json.dumps(games, sort_keys=True, indent=2))

    with open('games.json', 'w') as json_file:
        json.dump(games, json_file, sort_keys=True, indent=2)   

if __name__ == "__main__":
    main()