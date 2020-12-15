import re
import emoji

import unicodedata
import itertools

from nltk import TweetTokenizer
from nltk.corpus import stopwords as stp
from nltk.stem import SnowballStemmer

from helper_etiquetador import HelperEtiquetador
from string import punctuation
from sklearn.base import TransformerMixin, BaseEstimator


class Preprocesador(BaseEstimator, TransformerMixin):

    def __init__(self, minusculas=True, menciones=True, urls=True,
                 hashtags=True, puntuacion=True, emojis=True, acentos=False,
                 repetidos=True, abreviaciones=True,
                 leng_inclusivo=True, espacios=True, stop_words=True,
                 raices=False, lemas=False):
        self.stopwords_espaniol = stp.words('spanish')
        self.stopwords_espaniol.extend(['vos', 'sos'])
        self.stopwords_sin_acentos = self.eliminar_acentos_stopwords(
            self.stopwords_espaniol)
        self.tokenizer = TweetTokenizer()

        self.stemmer = SnowballStemmer('spanish')

        self.minusculas = minusculas
        self.menciones = menciones
        self.urls = urls
        self.hashtags = hashtags
        self.puntuacion = puntuacion
        self.emojis = emojis
        self.acentos = acentos
        self.repetidos = repetidos
        self.abreviaciones = abreviaciones
        self.leng_inclusivo = leng_inclusivo
        self.espacios = espacios
        self.stop_words = stop_words
        self.raices = raices
        self.lemas = lemas

        self.helper_etiquetador = HelperEtiquetador()

    # Método fit para poder usar pipelines
    def fit(self, tweets, y=None):
        # Se retorna a sí mismo porque no se "aprende" nada
        return self

    # Método transform para poder usar pipelines
    def transform(self, tweets):
        # return [self.preprocesar(tweet) for tweet in tweets if not self.preprocesar(tweet)=='emptytw']
        return [self.preprocesar(tweet) for tweet in tweets]

    # Quita las tildes en las stopwords
    @staticmethod
    def eliminar_acentos_stopwords(palabras):
        for i, palabra in enumerate(palabras):
            palabras[i] = unicodedata.normalize('NFKD', palabra).encode(
                'ascii', 'ignore').decode('utf-8', 'ignore')
        return palabras

    # Pone todo el texto en minúsculas
    def pasar_a_minusculas(self, tweet):
        return tweet.lower()

    # Remover menciones (ej. @usuario1234)
    def eliminar_menciones(self, tweet):
        tweet = re.sub(r'(?<!\w)@\w+', '', tweet, flags=re.IGNORECASE)
        return tweet

    # Remover URLs (ej. https://t.co/ZdChVNsLYz)
    def eliminar_urls(self, tweet):
        tweet = re.sub(r'http\S+|www\S+|https\S', '', tweet, flags=re.IGNORECASE)
        return tweet

    # Remover hashtags (solo el símbolo #)
    def eliminar_hash(self, tweet):
        tweet = re.sub(r'\#|\brt\b', '', tweet, flags=re.IGNORECASE)
        return tweet

    # Remover completamente el hashtag
    def eliminar_hashtag(self, tweet):
        tweet = re.sub('#\w+|\brt\b|retweeted', '', tweet, flags=re.IGNORECASE)
        return tweet

    # Remover signos de puntuación
    def eliminar_puntuacion(self, tweet):
        signos = list(punctuation)
        signos.extend(['¿', '¡'])
        signos.extend(map(str, range(10)))
        tweet = tweet.translate(str.maketrans(
            ''.join(signos), ' '*len(''.join(signos))))
        return tweet

    # Transforma emojis en su versión textual en inglés
    def decodificar_emojis(self, tweet):
        return emoji.demojize(tweet, delimiters=(" ", " "))

    # Remueve cualquier tipo de tildes, salvo la virguilla ñ
    def eliminar_acentos(self, tweet):
        #trans_tab = dict.fromkeys(map(ord,u'\u0301\u0308'),None)
        #tweet = unicodedata.normalize('NFKD',tweet).encode('ascii','ignore').decode('utf-8','ignore')
        #tweet = unicodedata.normalize('NFKD', unicodedata.normalize('NFKD', tweet).translate(trans_tab))
        tweet = re.sub(
            r'([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+', r'\1',
            unicodedata.normalize("NFD", tweet), 0, re.I
        )
        return tweet

    # Elimina caracteres consecutivos repetidos, ej.: noooooo -> no
    def eliminar_repetidos(self, tweet):
        #tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))
        #tweet = ''.join(i[0] for i in itertools.groupby(tweet))
        tweet = re.sub(r'([^rlc])\1{1,}', r'\1', tweet)
        tweet = re.sub(r'(r|l|c)\1{2,}',r'\1\1',tweet)
        return tweet

    # Expande los términos abreviados
    def expandir_abreviaciones(self, tweet):
        tweet = re.sub(r'\b(tqm|tkm)\b', 'te quiero mucho', tweet, flags=re.IGNORECASE)
        tweet = re.sub(r'\b(xfas|xfavor|pls|plis|porfa)\b', 'por favor', tweet, flags=re.IGNORECASE)
        tweet = re.sub(r'\b(kien)\b', 'quien', tweet, flags=re.IGNORECASE)
        tweet = re.sub(r'\b(weno)\b', 'bueno', tweet, flags=re.IGNORECASE)
        tweet = re.sub(r'\b(tw)\b', 'twitter', tweet, flags=re.IGNORECASE)
        tweet = re.sub(r'\b(xq)\b', 'porque', tweet, flags=re.IGNORECASE)

        return tweet

    # Eliminar espacios y saltos de líneas excedentes
    def eliminar_espacios(self, tweet):
        tweet = re.sub(r'\s+|\\n', ' ', tweet, flags=re.IGNORECASE)
        return tweet

    # Separa el texto en sus palabras componentes
    def tokenizar(self, tweet):
        return self.tokenizer.tokenize(tweet)

    # Quita palabras vacías
    def eliminar_stopwords(self, tweet, acentos=False):
        tokens = self.tokenizar(tweet)
        if acentos:
            tweet = [
                token for token in tokens if token not in self.stopwords_sin_acentos and len(token) > 2]
        else:
            tweet = [
                token for token in tokens if token not in self.stopwords_espaniol and len(token) > 2]
        return ' '.join(tweet)

    # Stemming
    def stemming(self, tweet):
        tokens = self.tokenizar(tweet)
        tweet_raiz = ' '.join([self.stemmer.stem(token) for token in tokens])
        return tweet_raiz

    # Devuelve lista de tokens, pero lematizados
    def lematizar(self, tweet):
        if tweet:
            return self.helper_etiquetador.lematizar_gramatica(tweet)
        else:
            return ' '

    # Normalizo los tweets vacíos para no tener problemas con los vectores
    def normalizar_tweet_vacio(self, tweet):
        if len(tweet) == 0:
            return 'emptytw'
        else:
            return tweet

    # Compilo todas las operaciones en una sola función
    def preprocesar(self, tweet):
        # pasar a minusculas
        if self.minusculas:
            tweet = self.pasar_a_minusculas(tweet)
        # elimina las menciones @
        if self.menciones:
            tweet = self.eliminar_menciones(tweet)
        # elimina las urls https://
        if self.urls:
            tweet = self.eliminar_urls(tweet)
        # eliminar solo el símbolo del hashtag #
        if self.hashtags:
            tweet = self.eliminar_hash(tweet)
        # transforma los emojis en su versión textual (inglés)
        if self.emojis:
            tweet = self.decodificar_emojis(tweet)
        # reemplaza abreviaciones comunes por su expresión completa
        if self.abreviaciones:
            tweet = self.expandir_abreviaciones(tweet)
        # eliminar signos de puntuación y números
        if self.puntuacion:
            tweet = self.eliminar_puntuacion(tweet)
        # quita cualquier tipo de tilde
        if self.acentos:
            tweet = self.eliminar_acentos(tweet)
        # elimina caracteres repetidos (ej. maaaaal -> mal)
        if self.repetidos:
            tweet = self.eliminar_repetidos(tweet)
        # quita espacios y saltos de líneas repetidos (deja solo uno entre cada palabra/oración)
        if self.espacios:
            tweet = self.eliminar_espacios(tweet)
        # tokenizar
        #tweet = self.tokenizar(tweet)
        # quita las stopwords
        if self.stop_words:
            tweet = self.eliminar_stopwords(tweet, self.acentos)
        # stemming
        if self.raices and self.lemas == False:
            tweet = self.stemming(tweet)
        # lematizar
        if self.raices == False and self.lemas:
            tweet = self.lematizar(tweet)
        tweet = self.normalizar_tweet_vacio(tweet)
        return tweet
