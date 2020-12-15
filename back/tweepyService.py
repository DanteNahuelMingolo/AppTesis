#Librerías propías
from capturador import prepareTweetsForDB

#Librería Python
import tweepy
import time
import pandas as pd

#Librería propia
import capturador, data

class TweepyStream(tweepy.StreamListener):
    streamingStore = []

    def on_status(self, status):
        if data.isRunning:
            if 'RT @' not in status.text and not status.source == 'Twibbon' and status.lang== 'es':  
                capturador.addTweetToBuffer(status)
                return True
        else:
            return False

    def on_error(self, status):
        print(status)
    
    def set_streamingStore(self, globalStreamingStore):
        self.streamingStore = data.streamingStore

def fake_streaming(df):
    for tweet in df.itertuples(index=None):
        if not data.isRunning:
            tDF = pd.DataFrame([tweet], columns=['Id','Texto','Fecha de creación','Fuente'])
            capturador.prepareFakeTweetsForDB(tDF)
            time.sleep(1)
        else:
            return False