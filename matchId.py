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

def getMatchIdURL( region, accountId, api_key):
    month_in_mill = 2592000000
    currentTime = int(round(time.time() * 1000))
    beginTime = currentTime - 3 * month_in_mill

    url = "https://" + region\
    + ".api.riotgames.com/lol/match/v4/matchlists/by-account/"+ accountId\
    +"?queue=450&beginTime="+ str(beginTime)\
    +"&api_key=" + api_key

    return url

def getMatchIdByPlayer( region, accountId, api_key ):

    # Create a list to store the match ID played by user with given account ID, and get Riot API URL
    matchIdList = []
    url = getMatchIdURL( region, accountId, api_key )

    # While loop to handle API rate limit exceeding 
    while( True ):
        # Request for match info played by user with given account Id
        try:
            response = requests.get( url )
            response.raise_for_status()
        # If any status code other than 200 occurs
        except requests.exceptions.RequestException as e:
            # User have not played ARAM in last 3 months (Data Not Found), break from while loop
            if( response.status_code == 404):
                #  print("User does not have record playing ARAM in last 3 months")
                break
            # If API Rate limit exceeded, wait for 1 min and try again.
            elif( response.status_code == 429 ):
                retry_after = response.headers['Retry-After']
                wait(retry_after)
                continue
            # Any other error will print out and break from while loop
            else:
                print(e)
                break
        # If request was successful, handle json data and break from while loop
        else:
            json_data = response.json()
            matches = json_data['matches']
            # print("Collected match history of user with account id : " + accountId)
            for match in matches:
                matchId = match['gameId']
                matchIdList.append(matchId)
            break

    return matchIdList

def getMatchId( region ):

    RIOTConstant = riotConstant.RIOTConstant()
    api_key = RIOTConstant.api_key
    
    # Read account ID file per region 
    file_path_accnt = './data/' + region + "accountId.csv" 
    df_accntId = pd.read_csv(file_path_accnt)

    # Create a new dataframe to store match ID
    df_matchId = pd.DataFrame()

    # For each tier / division 
    for column in df_accntId.columns:

        # Get the list of account ID, and create list to store match ID
        accntIdList = df_accntId[column].dropna(axis = 0)
        matchIdList = []

        # Create variable to track process of getting data
        total = len(accntIdList)
        count = 1

        # For each account ID
        for accntId in accntIdList:
            # Get the match ID played by each account ID
            matchidListByPlayer = getMatchIdByPlayer( region, accntId, api_key)
            print("Collecting match history : " + str(count) + " out of " + str(total), end = '\r')
            count = count + 1
            # Add the match ID to the list
            matchIdList.extend(matchidListByPlayer)

        # Once iterate through all account ID in each tier / division, 
        # check for duplicate, create a dataframe column and concatenate with previous dataframe 
        matchIdList = list(dict.fromkeys(matchIdList))
        new_column = pd.DataFrame( data = { column : matchIdList } )
        df_matchId = pd.concat( [df_matchId, new_column], axis=1 )
    
        df_matchId.to_csv('./data/' + region + "matchId.csv", index=False)

    # # Once all columns are done, convert everythin to Integer because some values are listed as float type
    # df_final = pd.read_csv('./data/' + region + "matchId.csv").dropna(axis = 0)
    # df_final = df.astype(int)
    # df_final.to_csv('./data/' + region + "matchId.csv", index=False)

