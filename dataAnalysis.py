#%%
import pandas as pd
import matplotlib.pyplot as plt
import riotConstant

# Language / Region / Champion / Tier 
# will be passed as parameter from user's selection

# Read Data
def readData( language, region, championName, tier ):

    RIOTConstant = riotConstant.RIOTConstant()
    RIOTConstant.setLanguage(language)

    championId = RIOTConstant.getChampionId(championName)

    data = pd.read_csv('./data/finalData/' + region + "/" + tier + "/champion_" + str(championId) + ".csv")
    
    return data
    

def dataSort( language, region, championName, tier ):
    # pd.options.mode.chained_assignment = None

    RIOTConstant = riotConstant.RIOTConstant()
    RIOTConstant.setLanguage(language)

    championId = RIOTConstant.getChampionId(championName)


    data = readData( language, region, championName, tier)

    # Changin the combination of spells in ascending order to check frequency
    print( data[['spell1Id', 'spell2Id']].head(5) )
    spell_combination = data[['spell1Id', 'spell2Id']]
    for i, spells in spell_combination.iterrows():
        if( spells['spell1Id'] > spells['spell2Id']):
            data.loc[i, ['spell1Id', 'spell2Id']] = [spells['spell2Id'], spells['spell1Id']]
    print( data[['spell1Id', 'spell2Id']].head(5) )

    print( data[['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']].head(5) )
    item_combination = data[['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']]
    for i, items in item_combination.iterrows():
        sorted_items = items.sort_values(ascending=False)
        data.loc[i, ['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']] = sorted_items.to_numpy()
    print( data[['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']].head(5) )


    print( data[['perkPrimaryStyle', 'perk0', 'perk1','perk2','perk3']].head(5))
    prime_run_combination = data[['perkPrimaryStyle', 'perk0', 'perk1','perk2','perk3']]
    for i, prime_runes in prime_run_combination.iterrows():
        sorted_prime_runes = prime_runes.sort_values(ascending=True)
        data.loc[i, ['perkPrimaryStyle', 'perk0', 'perk1','perk2','perk3']] = sorted_prime_runes.to_numpy()
    print( data[['perkPrimaryStyle', 'perk0', 'perk1','perk2','perk3']].head(5) )

    
    print( data[['perkSubStyle', 'perk4', 'perk5']].head(5))
    sub_run_combination = data[['perkSubStyle', 'perk4', 'perk5']]
    for i, sub_runes in sub_run_combination.iterrows():
        sorted_sub_runes = sub_runes.sort_values(ascending=True)
        data.loc[i, ['perkSubStyle', 'perk4', 'perk5']] = sorted_sub_runes.to_numpy()
    print( data[['perkSubStyle', 'perk4', 'perk5']].head(5) )

    data.to_csv('./data/finalData/' + region + "/" + tier + "/champion_" + str(championId) + ".csv")
    return

def byWinRate( language, region, championName, tier ):
    data = readData( language, region, championName, tier)
    return



def byPickRate( language, region, championName, tier ):
    data = readData( language, region, championName, tier)
    return

def spellByWinRate( language, region, championName, tier ):
    data = readData( language, region, championName, tier)
    # print( data[['win', 'spell1Id', 'spell2Id']].head(5) )

    print( data.groupby(["win", "spell1Id", "spell2Id"]).size() )

    print( data.groupby(["spell1Id", "spell2Id"]).size() )

def runeByWinRate( language, region, championName, tier ):
    data = readData( language, region, championName, tier)
    # print( data[['win', 'spell1Id', 'spell2Id']].head(5) )

    print( data.groupby(["win", "perkPrimaryStyle", "perkSubStyle"]).size() )

    print( data.groupby(["win", "perk0", "perk1", "perk2", "perk3"]).size())

    print( data.groupby(["win", "perk4", "perk5"]).size())

    print( data.groupby(["perkPrimaryStyle", "perkSubStyle"]).size() )

    print( data.groupby(["perk0", "perk1", "perk2", "perk3"]).size())

    print( data.groupby(["perk4", "perk5"]).size())


dataSort( "ko_KR", "BR1", "annie", "GOLD")
spellByWinRate( "ko_KR", "BR1", "annie", "GOLD" )
runeByWinRate( "ko_KR", "BR1", "annie", "GOLD" )