import json

class RIOTConstant:
    def __init__(self):
        self.regions = ["BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "RU", "TR1"]
        self.api_key = "YOUR API KEY"
        self.file_path = 'constants/dragontail-10.4.1/10.4.1/data/'
        self.language = 'en_US'
        self.tier_div = ['IRON_I','IRON_II','IRON_III','IRON_IV',
                           'BRONZE_I','BRONZE_II','BRONZE_III','BRONZE_IV',
                           'SILVER_I','SILVER_II','SILVER_III','SILVER_IV',
                           'GOLD_I','GOLD_II','GOLD_III','GOLD_IV',
                           'PLATINUM_I','PLATINUM_II','PLATINUM_III','PLATINUM_IV',
                           'DIAMOND_I','DIAMOND_II','DIAMOND_III','DIAMOND_IV',
                           'MASTER_I', 'GRANDMASTER_I', 'CHALLENGER_I']

    def setLanguage(self, language):
        self.language = language
        return

    def getLanguage(self):
        return self.language

    def getChampionId(self, championName):
        championName = championName.upper()
        champions = self.getChampion()
        for id, name in champions.items(): 
            if(name.upper() == championName):
                return id

    def getItem(self):
        item_dictionary = {}
        file_path = self.file_path + self.language + "/item.json"

        # Get the riot data dragon json data, and store it with key / value structure
        with open( file_path) as json_file:
            json_data = json.load(json_file)
            items = json_data['data']
            for item in items:
                item_name = items[item]['name']
                item_dictionary[ str(item) ] = item_name 

        return item_dictionary

    def getRune(self):
        rune_dictionary = {}
        file_path = self.file_path + self.language + "/runesReforged.json"

        # Get the riot data dragon json data, and store it with key / value structure
        with open( file_path ) as json_file:
            data = json.load(json_file)
            for prime in data:
                rune_dictionary[ prime['id'] ] = prime['name']
                slots = prime['slots']
                for slot in slots:
                    runes = slot['runes']
                    for rune in runes:
                        rune_dictionary[ rune['id'] ] = rune['name']
        
        return rune_dictionary

    def getSpell(self):
        spell_dictionary = {}
        file_path = self.file_path + self.language + "/summoner.json"

        # Get the riot data dragon json data, and store it with key / value structure
        with open( file_path ) as json_file:
            summoner = json.load(json_file)
            spells = summoner['data']
            for spell in spells:
                spell_info = spells[spell]
                spell_dictionary[ spell_info['key'] ] = spell_info['name']

        return spell_dictionary

    def getChampion(self):
        champion_list = {}
        file_path = self.file_path + self.language + "/champion.json"

        with open( file_path ) as json_file:
            json_data = json.load(json_file)
            champions = json_data['data']
            for champion in champions:
                champion_list[ champions[champion]['key'] ] = champion

        return champion_list

    def getDFColumn(self):
        df_column = []
        df_column.extend(['win'])

        column_dictionary = {}
        runes = self.getRune()        
        items = self.getItem()            
        spells = self.getSpell()
        column_dictionary = {**runes, **items, **spells}

        for column in column_dictionary.items():
            df_column.append( str(column[0]) + "_" + column[1])

        return df_column
      


language = 'en_US'
data = RIOTConstant()
# print( data.getSpell(language) )
# print( data.getDFColumn() )