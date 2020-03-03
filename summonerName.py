import requests
import riotConstant
import pandas as pd 
import time

def wait( tik ):
    tik = int(tik)
    tik += 2
    while( tik > 0 ):
        print("API Rate Limit exceeded, wait for " + str(tik) + " second(s)", end = '   \r')
        tik -= 1
        time.sleep(1)
    print("                                                     ", end='\r')
    return

# Get Summoner Name from all division & regions
def getURL( region, tier, division, page, api_key):
    url = "https://" + region\
    + ".api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/"\
    + tier + "/" + division + "?page=" + str(page) + "&api_key=" + api_key
    return url

# Iterate through whole page and get Summoner Name from Riot API response
def getSummonerIdByTierAndDivision( region, tier, division, api_key ):
    page = 1
    summonerName = []
    userRemain = True

    # Division may have more than 1 page of users, loop through all of them
    while ( userRemain ) :

        # Get Riot API URL
        url = getURL( region, tier, division, page, api_key)

        try:
            response = requests.get( url )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            # If API rate limit exceeded, wait for the amount of seconds indicated in the response header (which is aroung 35 here)
            if( response.status_code == 429 ):
                retry_after = response.headers['Retry-After']
                wait(retry_after)
                continue
            # Else, print out the error and break from loop
            else:
                print(e)
                break
        else:
            # Get the response data as JSON data
            json_data = response.json()

            # If there is no data from this page, finish loop
            # Otherwise, loop through all pages
            if( len(json_data) == 0 ):
                userRemain = False
                break
            else :
                page = page + 1
            
            # If you want to reduce the size of file by limiting the number of summoner name by tier/division,
            # then include the below if condition with your desired number of summoner names
            if( len(summonerName) > 100 ):
                break

            # For each page, iterate through all users, add summoner name of them to array by appending it to the end
            for users in json_data:
                summonerName.append(users['summonerName'])
                if( len(summonerName) > 10 ):
                    userRemain = False
                    break

    return summonerName

def getSummonerName( region ):

    RIOTConstant = riotConstant.RIOTConstant()
    api_key = RIOTConstant.api_key
    tier_div = RIOTConstant.tier_div

    df_summonerName = pd.DataFrame()
    
    print("current region is : " + region + "                       ")

    for column in tier_div:
        tier = column.split('_')[0]
        division = column.split('_')[1]

        print("Searching for summoners in : " + tier + "_" + division, 
                end = '                     \r')

        summonerName = getSummonerIdByTierAndDivision( region, tier, division, api_key)
        new_column = pd.DataFrame( data = { column : summonerName })
        df_summonerName = pd.concat( [ df_summonerName, new_column], axis=1 )
            
        path = './data/' + region + 'summonerName.csv'
        df_summonerName.to_csv(path, index=False)

    return 0