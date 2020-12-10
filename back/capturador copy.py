# Import libraries
import pandas as pd
import pyodbc
import re, pytz, json, time


import model
from info import tweets_actuales

from flask import jsonify, redirect

from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from pandas.io import sql
from sqlalchemy import create_engine
from pandas.io.json import json_normalize
# Declare variables that contains the user credentials to access Twitter API
# You can get your own keys in https://apps.twitter.com/
# --------------------------------------------------------------------------------
aToken = "998860480683929600-6fdzyVcKzetwzwVwJZsMyy62OWJIp8J"
aTokenSecret = "T09QODFQNKayBWybDQ8Jgbgmjftwtzoh5NZZoV2IYKR8m"
cKey = "y7AKteQ8a6JwrsCmP2WSX6j3Z"
cSecret = "e6gaZmrQP62mUZhraTgKHwKTe29ttoyuFv6kztjvjxCmkx5Uht"
# --------------------------------------------------------------------------------
# Define after how many twitts we do a insert in the data base.
bufferSize = 5
# Defina an array to store the tweets readed from the stream api
twittsBuffer = []
#tweets_actuales= []
# Define a connectiont to read-write to the Sql server Database
engine = create_engine(
    "mssql+pyodbc://hxsnb-dmingolo/TwitterDB?driver=SQL+Server+Native+Client+11.0")

# Define a function that receive a twitt by parameter and store it into the twittBuffer variable
# if the twittBuffer reach the buffersize defined lenght then call the function AddTwittsToDB that insert the twitts into
# the twittsBuffer array into the SQL Server database and clean the buffer
# --------------------------------------------------------------------------------
class StdOutListener(StreamListener):
    def on_status(self, status):
        #t = json.loads(data)
        if 'RT @' not in status.text and not status.source == 'Twibbon' and status.lang== 'es':  
            print (status.text)
            AddTwittToBuffer(status)

        #time.sleep(2)
        #return jsonify(t)
        return True

    def on_error(self, status):
        print(status)

myListener = StdOutListener()
authenticator = OAuthHandler(cKey, cSecret)
authenticator.set_access_token(aToken, aTokenSecret)

def AddTwittToBuffer(twitt):

    global twittsBuffer
    twittsBuffer.append(twitt)

    if (len(twittsBuffer) == bufferSize):
        AddTwittsToDB(twittsBuffer)
        twittsBuffer = []
    return

# --------------------------------------------------------------------------------
def transformar_fecha(fecha_utc):
    timestamp = mktime_tz(parsedate_tz(fecha_utc))
    dt = datetime.fromtimestamp(timestamp,pytz.timezone('America/Buenos_Aires'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def AddTwittsToDB(twitts):
    #global tData
    tData = {'Id': [],
             'Texto': [],
             'Fecha de creación': [],
             'Fuente': []}

    for t in twitts:
            #if t['place'] is not None:
            #    if 'Argentina' in t['place']['country']:
                tData['Id'].append(t.id)

                if t.truncated:
                    #if 'full_text' in t.extended_tweet:
                    tData['Texto'].append(t.extended_tweet['full_text'])
                else:
                    tData['Texto'].append(t.text)

                tData['Fecha de creación'].append(transformar_fecha(t.created_at))
                tData['Fuente'].append(re.search(r'(?<=>)(.*)(?=<)',t.source).group(1))

    # Guardo los tweets si es que hay alguno después de filtrar
    global tweets_actuales
    if len(tData['Id'])>0: 
        guardar_tweets_bd(tData)
        tweets_actuales +=tData['Texto']
    
    if len(tweets_actuales)>=5:
        #tweets_actuales=[]
        obtener_tweets()
    #return jsonify(tData)
# --------------------------------------------------------------------------------
# Create a listener class that process received tweets
# On error print status
# --------------------------------------------------------------------------------
def guardar_tweets_bd (diccionario_tweets):
    tweets = pd.DataFrame(diccionario_tweets)
    tweets.set_index('Id', inplace=True)

    tweets.to_sql("TweetsCaptura", engine, None, if_exists='append')
    
# --------------------------------------------------------------------------------
# Define a main function, the entry point of the program
#if __name__ == '__main__':
def iniciar_busqueda(query):

    stream = Stream(authenticator, myListener, tweet_mode='extended')
    stream.filter(track=['cuarentena','crackdona','diego','tolkien','OMS'], languages=['es'], is_async=True)
  #  except Exception as e:
   #     stream.disconnect()

def obtener_tweets():
    #if len(tweets_actuales) == 5 :
        result = model.textList()
        result.setData(tweets_actuales)
        return result.getResponse()
    #return ''   


iniciar_busqueda(['maradona'])