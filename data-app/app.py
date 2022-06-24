import os, sys
import pandas as pd
import numpy as np
import json, time
from database import insert_firerisks_data

#INPE: https://queimadas.dgi.inpe.br/queimadas/dados-abertos/#

COUNTRY='33'
STATE='13'
INPE_API_LINK=f'https://queimadas.dgi.inpe.br/api/focos/?pais_id={COUNTRY}&estado_id={STATE}' # pais_id=33(br) e estado_id=13(amazonas)

print('Contacting INPE API...')
print(f'Country: ({COUNTRY})')
print(f'State: ({STATE})')
print(f'API Link: ({INPE_API_LINK})')

while (True):
    print("Sending request...")
    df_queimadas = pd.read_json(INPE_API_LINK)
    df_queimadas["geometry"] = df_queimadas["geometry"].map(lambda item: json.dumps(item))
    df_queimadas["properties"] = df_queimadas["properties"].map(lambda item: json.dumps(item))

    print("Data collected: ")
    print(df_queimadas.head()) # Dataframe first row
    print(df_queimadas.count()) # Data info
    print(df_queimadas.columns) # Dataframe columns

    insert_firerisks_data(df_queimadas)

    print("Time interval!")
    time.sleep(600) #86400 (24h)
    print("End of time interval!".center(40, "#"))