import sys, os
sys.path.append('back\helpers')
from sklearn.base import TransformerMixin, BaseEstimator
from helper_etiquetador import HelperEtiquetador
from nltk import TweetTokenizer

class Etiquetador(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.helper_etiquetador = HelperEtiquetador()
        self.tokenizer = TweetTokenizer()

    def fit(self, tweets, y=None):
        return self

    def transform(self, tweets):
        return [self.etiquetar_gramatica(tweet) for tweet in tweets]

    # Devuelve una lista de diccionarios con la palabra original y su etiqueta.
    def etiquetar_gramatica(self, tweet):
        # Devuelve lista de sus etiquetas
        if tweet:
            self.tokenizer = TweetTokenizer()
            return self.helper_etiquetador.etiquetar_gramatica(tweet)
        else:
            return ' '