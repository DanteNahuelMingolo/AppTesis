# Import libraries
import pandas as pd
import pyodbc
import re, pytz, json, time
import pickle

from flask import jsonify, redirect

from pytz import timezone
from pandas.io import sql
from sqlalchemy import create_engine
from copy import deepcopy

import sys, os
sys.path.append('back\modules')

# Librerías propias
import data 
from modules.clasificador import clasificar, clasificarFakeTweets
# Define after how many twitts we do a insert in the data base.
bufferSize = data.bufferSize

# Define a connectiont to read-write to the Sql server Database
engine = create_engine(
    "mssql+pyodbc://hxsnb-dmingolo/TwitterDB?driver=SQL+Server+Native+Client+11.0")

def addTweetToBuffer(tweet):

    data.tweetsBuffer.append(tweet)

    if (len(data.tweetsBuffer) == bufferSize):
        prepareTweetsForDB(data.tweetsBuffer)
        data.tweetsBuffer = []
    return data.tweetsBuffer

# --------------------------------------------------------------------------------
# como las fechas vienen adelantadas 3 horas (UTC) las llevo al horario de Bs. As.
def localizeDate(date_utc):
    tz = timezone('America/Buenos_Aires')
    date_utc = date_utc.replace(tzinfo=pytz.utc).astimezone(tz)
    date_gmt = date_utc.strftime('%Y-%m-%d %H:%M:%S')
    return date_gmt

def saveTweetsToDB (lista_tweets):
    lista_tweets.set_index('Id', inplace=True)
    lista_tweets.to_sql("TweetsCaptura", engine, None, if_exists='append')

def prepareTweetsForDB(twitts):
    #global tData
    tData = pd.DataFrame(columns = ['Id','Texto','Fecha de creación','Fuente'])

    # manejo de campos
    for t in twitts:
            #if t['place'] is not None:
            #    if 'Argentina' in t['place']['country']:
        #tweet = Tweet()
        tweet = {}
        tweet['Id'] = t.id
        if t.truncated:
            tweet['Texto'] = t.extended_tweet['full_text']
        else:
            tweet['Texto'] = t.text

        tweet['Fecha de creación'] = localizeDate(t.created_at)
        tweet['Fuente'] = t.source
    
        tData = tData.append(tweet,ignore_index=True)

    tData['Agresivo']=clasificar(tData)

    # Actualizo streamingStore, para mostrar de a 5 tweets
    data.streamingStore = data.streamingStore.append(tData)
    data.countTotal = len(data.streamingStore.index)


    # Guardo los tweets en SQL
    saveTweetsToDB(tData.loc[:,['Id','Texto','Fecha de creación','Fuente','Agresivo']])

def prepareFakeTweetsForDB(t):
    t['Agresivo'] = clasificarFakeTweets(t)

    # Actualizo streamingStore, para mostrar de a 5 tweets
    data.streamingStore = data.streamingStore.append(t)
    data.countTotal = len(data.streamingStore.index)

