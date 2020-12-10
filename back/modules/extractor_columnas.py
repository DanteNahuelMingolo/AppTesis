from sklearn.base import TransformerMixin

class DataFrameColumnExtracter(TransformerMixin):

    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X[self.column]