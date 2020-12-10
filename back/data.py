import pandas as pd

#Guarda todos los tweets capturados en una sesión.
streamingStore = pd.DataFrame(columns = ['Id','Texto','Fecha de creación','Fuente','Agresivo'])
streamingStore['Fecha de creación'] = pd.to_datetime(streamingStore['Fecha de creación'])

tweetsBuffer = []

bufferSize = 2

#Contadores
cantAgresivo = 0 
cantNoAgresivo = 0
cantNeutro = 0