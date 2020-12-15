# Librerías Python
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from collections import Counter
from imblearn.over_sampling import SVMSMOTE
from imblearn.pipeline import make_pipeline, Pipeline as p
from sklearn.svm import LinearSVC
from sklearn.pipeline import FeatureUnion
from sklearn.model_selection import train_test_split

# Librerías propias
from extractor_columnas import DataFrameColumnExtracter
from etiquetador import Etiquetador
from extractor_citas import ExtractorCitas
from extractor_insultos import ExtractorInsultos
from extractor_risas import ExtractorRisas
from normalizador import Normalizador
from preprocesador import Preprocesador

import pandas as pd
import csv
import numpy as np
import joblib

# Cargar modelo desde el archivo
pkl_filename = "back/tags/pipeline_final_smote.joblib"



excel_file = "../../../../OneDrive/Tesis/Excels/MuestraTweets.xlsx"
tweets = pd.concat(pd.read_excel(excel_file, sheet_name=None),ignore_index=True, sort=False)

# Instancio módulos de ayuda para procesamiento
norm = Normalizador(entidades=False)
prep = Preprocesador(emojis=True, acentos=True, repetidos=False,
                     stop_words=False, raices=False, lemas=True)
ext_risas = ExtractorRisas()
ext_citas = ExtractorCitas()
ext_insultos = ExtractorInsultos()
etiquetador = Etiquetador()

tweets['Normalizado'] = norm.fit_transform(tweets['Texto'])
tweets['Preprocesado'] = Preprocesador(emojis = True, acentos=True, repetidos=False, stop_words=False, raices=False, lemas=True).fit_transform(tweets['Normalizado'])
tweets['Cantidad insultos'] = ext_insultos.fit_transform(tweets['Normalizado'])
tweets['Cantidad risas'] = ext_risas.fit_transform(tweets['Normalizado'])
tweets['Cantidad citas'] = ext_citas.fit_transform(tweets['Normalizado'])
tweets['POS'] = etiquetador.fit_transform(tweets['Normalizado'])

pipe_prep = p([
    ('columna',DataFrameColumnExtracter('Preprocesado'))
    ,('vector',TfidfVectorizer(lowercase=False,tokenizer=None,stop_words=None, ngram_range=(1,1), max_features=None, use_idf=False))
])

pipe_ext_insultos = p([
    ('texto',DataFrameColumnExtracter('Normalizado'))
    ,('ext',ExtractorInsultos())
])

pipe_ext_risas = p([
    ('texto',DataFrameColumnExtracter('Normalizado'))
    ,('ext',ExtractorRisas())
])

pipe_ext_citas = p([
    ('texto',DataFrameColumnExtracter('Normalizado'))
    ,('ext',ExtractorCitas())
])

pipe_pos = p([
    ('texto',DataFrameColumnExtracter('POS'))
    ,('vector',TfidfVectorizer())
])

pipe_fuente = p([
        ('fuente',DataFrameColumnExtracter('Fuente'))
        ,('vector',TfidfVectorizer())
])

caracteristicas = tweets[['Normalizado','Preprocesado','POS','Fuente','Cantidad citas','Cantidad risas','Cantidad insultos']]
etiqueta = tweets['Agresivo']
X_train, X_test, y_train, y_test = train_test_split(caracteristicas, etiqueta, test_size = 0.2, stratify=etiqueta)

pipeline = p([
    ('feats',FeatureUnion([
            ('preprocesador',pipe_prep)
            ,('fuente',pipe_fuente)
            ,('pos',pipe_pos)
            ,('risas',pipe_ext_risas)
            ,('insultos',pipe_ext_insultos)
            ,('citas',pipe_ext_citas)
                         ])
    
    )
    #,('downsampler',RandomUnderSampler(sampling_strategy={'no':1500}))
    ,('upsampler',SVMSMOTE(sampling_strategy={'sí':1000,'neutro':1000}))
   # ,('selector',SelectKBest(score_func=chi2,k=4500))
    ,('modelo',LinearSVC(C=0.5,class_weight='balanced',dual=True))
                    ])

pipeline.fit(tweets, tweets['Agresivo'])

with open(pkl_filename, 'wb') as file:
    joblib.dump(pipeline, file)
with open(pkl_filename, 'rb') as file:
    pipeline = joblib.load(file)