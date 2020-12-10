from normalizador import Normalizador
from sklearn import preprocessing
from sklearn.base import BaseEstimator, TransformerMixin

class ExtractorEntidades(BaseEstimator,TransformerMixin):

    def __init__(self, normalizado=True):
        self.normalizador = Normalizador()
        self.normalizado = normalizado

    def transform(self, tweets, y=None):

        cantidad_entidades = []

        if self.normalizado:
            for tweet in tweets:
                cantidad_entidades.append([tweet.count('entitytw')])
        else:
            for tweet in tweets:
                tweet = self.normalizador.normalizar_entidades(tweet)
                cantidad_entidades.append([tweet.count('entitytw')])
            
        return preprocessing.MinMaxScaler().fit_transform(cantidad_entidades)

    def fit(self, df, y=None):
        return self
