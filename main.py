import pandas as pd
import riotConstant
import summonerName
import accountId
import matchId
import matchInfo

def createDataFrame():

    RIOTConstant = riotConstant.RIOTConstant()
    champs_id = RIOTConstant.getChampion().keys()
    region_id = RIOTConstant.regions

    tierDiv_list = ['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']

    df_column = ['win', 
                'spell1Id', 'spell2Id', 
                'perkPrimaryStyle', 'perk0', 'perk1', 'perk2', 'perk3', 
                'perkSubStyle', 'perk4', 'perk5',
                'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']
    df_matchInfo = pd.DataFrame(columns=[df_column])
    
    for region in region_id:
        for tierDiv in tierDiv_list:
            for champ_id in champs_id:
                filepath = "./data/finalData/" + region + "/" + tierDiv + "/champion_" + champ_id + ".csv"
                df_matchInfo.to_csv( filepath, index=False)

def main():

    RIOTConstant = riotConstant.RIOTConstant()
    region_id = RIOTConstant.regions

    # createDataFrame()

    for region in region_id:
        # Get Sumoner Names
        # summonerName.getSummonerName( region )

        # Get Account ID for each summoner name
        # accountId.getAccountId( region )

        # Get Match ID (ARAM) played by each account ID
        # matchId.getMatchId( region )

        # Get Match Info and store it as final data
        matchInfo.getFinalData( region )
        
    return 0

main()