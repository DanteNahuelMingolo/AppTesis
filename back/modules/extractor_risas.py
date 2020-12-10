from normalizador import Normalizador
from sklearn import preprocessing
from sklearn.base import BaseEstimator, TransformerMixin

class ExtractorRisas(BaseEstimator,TransformerMixin):

    def __init__(self, normalizado=True):
        self.normalizador = Normalizador()
        self.normalizado = normalizado

    def transform(self, tweets, y=None):

        cantidad_risas = []

        if self.normalizado:
            for tweet in tweets:
                cantidad_risas.append([tweet.count('laughtw')])
        else:
            for tweet in tweets:
                tweet = self.normalizador.normalizar_risa(tweet)
                cantidad_risas.append([tweet.count('laughtw')])
            
        return preprocessing.MinMaxScaler().fit_transform(cantidad_risas)

    def fit(self, df, y=None):
        return self