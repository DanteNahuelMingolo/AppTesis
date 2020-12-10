# Librerías Python
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline, make_pipeline, make_union, FeatureUnion
from collections import Counter

# Librerías propias
import data
from extractor_columnas import DataFrameColumnExtracter
from etiquetador import Etiquetador
from extractor_citas import ExtractorCitas
from extractor_insultos import ExtractorInsultos
from extractor_risas import ExtractorRisas
from normalizador import Normalizador
from preprocesador import Preprocesador

# Cargar modelo desde el archivo
pkl_filename = "back/tags/pipeline_final.pkl"

with open(pkl_filename, 'rb') as file:
    pipeline = pickle.load(file)

# Instancio módulos de ayuda para procesamiento
norm = Normalizador(entidades=False)
prep = Preprocesador(emojis=True, acentos=True, repetidos=False,
                     stop_words=False, raices=False, lemas=True)
ext_risas = ExtractorRisas()
ext_citas = ExtractorCitas()
ext_insultos = ExtractorInsultos()
etiquetador = Etiquetador()


def actualizar_sentimientos(preds):
    conteos = Counter(preds)
    data.cantAgresivo += conteos['sí']
    data.cantNeutro += conteos['neutro']
    data.cantNoAgresivo += conteos['no']


def clasificar(tweets_original):
    tweets = tweets_original.copy(deep=True)
    tweets['Normalizado'] = norm.fit_transform(tweets['Texto'])
    tweets['Preprocesado'] = prep.fit_transform(tweets['Normalizado'])
    tweets['Cantidad insultos'] = ext_insultos.fit_transform(
        tweets['Normalizado'])
    tweets['Cantidad risas'] = ext_risas.fit_transform(tweets['Normalizado'])
    tweets['Cantidad citas'] = ext_citas.fit_transform(tweets['Normalizado'])
    tweets['POS'] = etiquetador.fit_transform(tweets['Normalizado'])

    etiquetador.helper_etiquetador.guardar_cache()

    preds = pipeline.predict(tweets)

    actualizar_sentimientos(preds)
    return preds
