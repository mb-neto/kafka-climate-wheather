import os, sys
import pandas as pd
import numpy as np
import json, time
from database import insert_firerisks_data

#INPE: https://queimadas.dgi.inpe.br/queimadas/dados-abertos/#

INPE_API_LINK='https://queimadas.dgi.inpe.br/api/focos/?pais_id=33&estado_id=13' # pais_id=33(br) e estado_id=13(amazonas)

while (True):
    df_queimadas = pd.read_json(INPE_API_LINK)
    df_queimadas["geometry"] = df_queimadas["geometry"].map(lambda item: json.dumps(item))
    df_queimadas["properties"] = df_queimadas["properties"].map(lambda item: json.dumps(item))

    print(df_queimadas.head()) # Dataframe first row
    print(df_queimadas.count()) # Data info
    print(df_queimadas.columns) # Dataframe columns

    insert_firerisks_data(df_queimadas)

    time.sleep(600) #86400