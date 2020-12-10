from normalizador import Normalizador
from sklearn import preprocessing
from sklearn.base import BaseEstimator, TransformerMixin

class ExtractorInsultos(BaseEstimator,TransformerMixin):

    def __init__(self, normalizado=True):
        self.normalizador =  Normalizador()
        self.normalizado = normalizado

    def transform(self, tweets, y=None):

        cantidad_insultos = []

        if self.normalizado:
            for tweet in tweets:
                cantidad_insultos.append([tweet.count('cursingtw')])
        else:
            for tweet in tweets:
                tweet = self.normalizador.normalizar_insultos(tweet)
                cantidad_insultos.append([tweet.count('cursingtw')])

        return preprocessing.MinMaxScaler().fit_transform(cantidad_insultos)

    def fit(self, df, y=None):
        return self