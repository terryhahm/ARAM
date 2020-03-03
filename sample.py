import numpy as np
import pandas as pd
import riotAPIKey
import time 
import requests

df = pd.read_csv('./data/br1matchId.csv').dropna(axis = 0)
df = df.astype(int)
df.to_csv('./data/br1matchId.csv', index=False)