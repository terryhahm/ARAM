# Get Summoner Name from csv file
# Call Riot API to collect account ID
import requests
import numpy as np
import pandas as pd
import riotConstant
import time 
import math
import os.path

def wait( tik ):
    tik = int(tik)
    tik += 2
    while( tik > 0 ):
        print("API Rate Limit exceeded, wait for " + str(tik) + " second(s)", end = '   \r')
        tik -= 1
        time.sleep(1)
    print("                                                     ", end='\r')
    return

def getAccntIdURL( region, name, api_key ):
    url = "https://" + region\
        +".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name\
        +"?api_key=" + api_key
    return url

def getAccntId( region, name, api_key ):

    url = getAccntIdURL(region, name, api_key)

    while( True ):
        try:
            response = requests.get( url )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if( response.status_code == 429 ):
                retry_after = response.headers['Retry-After']
                wait(retry_after)
                continue
            else:
                print(e)
                break

        else:
            json_data = response.json()
            accountId = json_data['accountId']
            break
        
    return accountId

def getAccountId( region ):

    RIOTConstant = riotConstant.RIOTConstant()
    api_key = RIOTConstant.api_key
    tier_div = RIOTConstant.tier_div

    df_accnt = pd.DataFrame(columns=['IRON_I','IRON_II','IRON_III','IRON_IV',
                                    'BRONZE_I','BRONZE_II','BRONZE_III','BRONZE_IV',
                                    'SILVER_I','SILVER_II','SILVER_III','SILVER_IV',
                                    'GOLD_I','GOLD_II','GOLD_III','GOLD_IV',
                                    'PLATINUM_I','PLATINUM_II','PLATINUM_III','PLATINUM_IV',
                                    'DIAMOND_I','DIAMOND_II','DIAMOND_III','DIAMOND_IV',
                                    'MASTER_I', 'GRANDMASTER_I', 'CHALLENGER_I'])

    # Get the dataframe of summoner name
    file_path_orig = "./data/" + region + "summonerName.csv"
    df_smmnr = pd.read_csv(file_path_orig)

    # Prepare the output file
    file_path_dest = "./data/" + region + "accountId.csv"
    df_accnt = pd.DataFrame()

    print("Start gathering account id of " + region + " Server." )

    for column in tier_div:
        # Get the summoner names in each tier / division
        print("Getting " + column + " user account Id           ")
        smmnr_name =  df_smmnr[column].dropna(axis = 0)
        
        # Get total number & counter for process status
        total = len(smmnr_name)
        count = 1

        # Prepare list to store the account ID
        accountIdList = []

        # Start iterating through summoner name
        for name in smmnr_name:
            accountId = getAccntId( region, name, api_key )
            print("Getting account id : " + str(count) + " out of " + str(total), 
                  end='                     \r')
            accountIdList.append(accountId)
            count = count + 1

        new_column = pd.DataFrame( data = { column : accountIdList })
        df_accnt = pd.concat( [df_accnt, new_column], axis=1 )
        df_accnt.to_csv(file_path_dest, index=False)
        
