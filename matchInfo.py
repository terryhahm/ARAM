import numpy as np
import pandas as pd
import riotConstant
import time 
import requests

def wait( tik ):
    tik = int(tik)
    tik += 2
    while( tik > 0 ):
        print("API Rate Limit exceeded, wait for " + str(tik) + " second(s)", end = '   \r')
        tik -= 1
        time.sleep(1)
    print("                                                     ", end='\r')
    return

def getMatchInfoURL( region, matchID, api_key ):
    url = "https://" + region\
        + ".api.riotgames.com/lol/match/v4/matches/" + str(matchID)\
        + "?api_key=" + api_key

    return url

def parsePlayerStat( participant ):

    new_obs = {
        'win': participant['stats']['win'],
        'spell1Id': participant['spell1Id'],
        'spell2Id': participant['spell2Id'],
    }

    stats = participant['stats']
    stats_key = ['perkPrimaryStyle', 'perk0', 'perk1', 'perk2', 'perk3',
                 'perkSubStyle', 'perk4', 'perk5', 'item0', 'item1',
                 'item2', 'item3', 'item4', 'item5', 'item6']
    for key in stats_key:
        try:
            new_obs[key] = stats[key]
        except KeyError:
            new_obs[key] = 0

    return new_obs

def getMatchInfo( region, tier, matchID, api_key ):

    url = getMatchInfoURL( region, matchID, api_key )

    while( True ):
        try:
            response = requests.get( url )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if( response.status_code == 429 ):
                retry_after = response.headers['Retry-After']
                wait(retry_after)
                continue
            elif( response.status_code == 503 ):
                print(e)
                print("Retry getting the data")
                continue
            else:
                print(e)
                break

        else:
            json_data = response.json()
            participants = json_data['participants']
            # Data needed to be considered
            # 1. Champion
            # 2. Rune (perkPrimaryStyle, perkSubStyle)
            # 3. Detailed Rune (perk0, perk1, perk2, perk3, perk4, perk5)
            # 4. Item (item0, item1, item2, item3, item4, item5, item6)
            # 5. Result (win)
            # 6. Spell (spell1Id, spell2Id)
            for participant in participants:
                # Get the champion Name for each participant
                championId = participant['championId']
                
                # Parse through json data, generate new observation row
                new_obs = parsePlayerStat( participant )

                # Read and write to csv file  
                df_matchInfo = pd.read_csv("./data/finalData/" + region + "/" + tier + "/champion_" + str(championId) + ".csv")
                df_matchInfo = df_matchInfo.append(new_obs, ignore_index = True)
                df_matchInfo.to_csv("./data/finalData/" + region + "/" + tier + "/champion_" + str(championId) + ".csv")

            break
    return

def getFinalData( region ):

    RIOTConstant = riotConstant.RIOTConstant()
    api_key = RIOTConstant.api_key

    filepath = "./data/" + region + 'matchId.csv'
    df_matchId = pd.read_csv( filepath )

    for column in df_matchId.columns:
        tier = column.split('_')[0]
        matchId_list = df_matchId[column].dropna(axis = 0)
        print("Trying to get match info from " + region + " server, " + column)
        for matchId in matchId_list:
            getMatchInfo( region, tier, int( matchId ) , api_key)

