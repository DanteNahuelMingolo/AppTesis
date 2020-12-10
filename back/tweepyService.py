#Librería tweepy
from capturador import prepareTweetsForDB
import tweepy

#Librería propia
import capturador, data

class TweepyStream(tweepy.StreamListener):
    streamingStore = []

    def on_status(self, status):
        if 'RT @' not in status.text and not status.source == 'Twibbon' and status.lang== 'es':  
            capturador.addTweetToBuffer(status)
            #data.streamingStore.append(status.text)
            return True

    def on_error(self, status):
        print(status)
    
    def set_streamingStore(self, globalStreamingStore):
        self.streamingStore = data.streamingStore