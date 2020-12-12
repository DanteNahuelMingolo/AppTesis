import pandas as pd

#Guarda todos los tweets capturados en una sesión.
streamingStore = pd.DataFrame(columns = ['Id','Texto','Fecha de creación','Fuente','Agresivo'])
streamingStore['Fecha de creación'] = pd.to_datetime(streamingStore['Fecha de creación'])

tweetsBuffer = []

bufferSize = 2

#Contadores
countAggresive = 0 
countNonAggresive = 0
countNeutral = 0
countTotal = 0