#Modelos
from re import split
import model

#Librerías propias
import tweepyService, data

#Librerías de flask y tweepy
from flask import jsonify
import tweepy

from random import randrange

#variables globales 
lastStreamingWord = ""
myStream = None

#keys
aToken = "998860480683929600-6fdzyVcKzetwzwVwJZsMyy62OWJIp8J"
aTokenSecret = "T09QODFQNKayBWybDQ8Jgbgmjftwtzoh5NZZoV2IYKR8m"
cKey = "y7AKteQ8a6JwrsCmP2WSX6j3Z"
cSecret = "e6gaZmrQP62mUZhraTgKHwKTe29ttoyuFv6kztjvjxCmkx5Uht"

def __setAuthForStreaming():
    auth = tweepy.OAuthHandler(cKey, cSecret)
    auth.set_access_token(aToken, aTokenSecret)
    return auth

def __createStreamingListener():
    global myStream
    #global streamingStore
    myStreamListener = tweepyService.TweepyStream()
   #myStreamListener.set_streamingStore(data.streamingStore)
    myStream = tweepy.Stream(__setAuthForStreaming(), myStreamListener, tweet_mode='extended')

def __stopStreaming():
    global myStream
    myStream.disconnect()    
    __createStreamingListener()

def __parsearQuery(word):
    words = [w.strip() for w in word.split(';')]
    return words

def streaming(word):
    data.cantAgresivo = 0 
    data.cantNoAgresivo = 0
    data.cantNeutro = 0

    global myStream
    global lastStreamingWord
    #si la nueva búsqueda es distinta a la última búsqueda entonces actualizamos
    if(lastStreamingWord != word):
        #si no tenemos creado el stream lo hacemos
        if(myStream == None):
            __createStreamingListener()
        #si está creado, detenemos el streaming para una nueva búsqueda
        else:        
            __stopStreaming()
        #iniciamos el stream
        myStream.filter(track=__parsearQuery(word), is_async=True)
        lastStreamingWord = word
    result = model.textList()
    result.setData('True')
    return result.getResponse()

def getTweets():
    #global streamingStore
    result = model.textList()

    list_test = []
    list_test.append(data.streamingStore[0:1]['Texto'].to_string())
    list_test.append(data.streamingStore[1:2]['Texto'].to_string())
    if len(data.streamingStore.index) > 5:
        result.setData(data.streamingStore.sort_values(by='Fecha de creación',ascending=False).iloc[:5,1:3].to_json(force_ascii=False,orient='records'))
        #result.setData(list_test)
    if len(data.streamingStore.index) >0 and len(data.streamingStore) <=5:   
        result.setData(data.streamingStore.sort_values(by='Fecha de creación',ascending=False).iloc[:,1:3].to_json(force_ascii=False,orient='records'))
        #result.setData(list_test)
    if len(data.streamingStore.index) == 0:
        return ''
    return result.getResponse()

def dataForPieChart(word):
    result = model.chart()
    result.setData([data.cantAgresivo, data.cantNeutro, data.cantNoAgresivo])
    result.setLabel(word)
    result.setChartLabels(["Agresivo", "Neutro", "No agresivo"])    
    return result.getResponse()