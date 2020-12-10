from normalizador import Normalizador
from sklearn import preprocessing
from sklearn.base import BaseEstimator, TransformerMixin

class ExtractorCitas(BaseEstimator,TransformerMixin):

    def __init__(self, normalizado=True):
        self.normalizador = Normalizador()
        self.normalizado = normalizado

    def transform(self, tweets, y=None):

        cantidad_citas = []

        if self.normalizado:
            for tweet in tweets:
                cantidad_citas.append([tweet.count('quotetw')])
        else:
            for tweet in tweets:
                tweet = self.normalizador.normalizar_citas(tweet)
                cantidad_citas.append([tweet.count('quotetw')])
            
        return preprocessing.MinMaxScaler().fit_transform(cantidad_citas)

    def fit(self, df, y=None):
        return self
