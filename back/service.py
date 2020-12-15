# Modelos
import matplotlib.pyplot as plt
from re import split
import model

# Librerías propias
import tweepyService
import data
from modules.preprocesador import Preprocesador

# Librerías de flask y tweepy
from flask import send_file, Response
from io import BytesIO, StringIO
from skimage.io import imsave
from PIL import Image
from wordcloud import WordCloud

import tweepy

# Librerías Python
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')

# variables globales
lastStreamingWord = ""
myStream = None
preprocesador = Preprocesador()

# keys
aToken = "998860480683929600-6fdzyVcKzetwzwVwJZsMyy62OWJIp8J"
aTokenSecret = "T09QODFQNKayBWybDQ8Jgbgmjftwtzoh5NZZoV2IYKR8m"
cKey = "y7AKteQ8a6JwrsCmP2WSX6j3Z"
cSecret = "e6gaZmrQP62mUZhraTgKHwKTe29ttoyuFv6kztjvjxCmkx5Uht"


def __setAuthForStreaming():
    auth = tweepy.OAuthHandler(cKey, cSecret)
    auth.set_access_token(aToken, aTokenSecret)
    return auth


def __createStreamingListener():
    global myStream
    #global streamingStore
    myStreamListener = tweepyService.TweepyStream()
   # myStreamListener.set_streamingStore(data.streamingStore)
    myStream = tweepy.Stream(__setAuthForStreaming(),
                             myStreamListener, tweet_mode='extended')


def __stopStreaming():
    global myStream
    myStream.disconnect()
    __createStreamingListener()


def __parsearQuery(word):
    words = [w.strip() for w in word.split(';')]
    return words


def __initializeVariables():
    data.countAggresive = 0
    data.countNonAggresive = 0
    data.countNeutral = 0
    data.countTotal = 0

    data.streamingStore = data.streamingStore[0:0]


def __multi_color_func(word=None, font_size=None,
                       position=None, orientation=None,
                       font_path=None, random_state=None):
    colors = [[185, 16, 29],
              [185, 11, 45],
              [185, 11, 8],
              [185, 16, 32]]
    rand = random_state.randint(0, len(colors) - 1)
    return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])


def __plotWordCloud():
    #try:
        wordList = data.streamingStore['Texto'].tail(20).to_list()
        wordsDF = ' '.join(wordList)
        wordsDF = preprocesador.pasar_a_minusculas(wordsDF)
        wordsDF = preprocesador.eliminar_menciones(wordsDF)
        wordsDF = preprocesador.eliminar_urls(wordsDF)
        wordsDF = preprocesador.eliminar_hash(wordsDF)
        wordsDF = preprocesador.eliminar_espacios(wordsDF)
        wordsDF = preprocesador.eliminar_puntuacion(wordsDF)
        wordsDF = preprocesador.eliminar_stopwords(wordsDF)

        mask = np.array(Image.open(r'back\images\mapa.jpg'))

        wordcloud = WordCloud(background_color='white', mask=mask, width=800, height=1600,
                            color_func=__multi_color_func, collocations=False).generate(wordsDF)

        fig = plt.figure(figsize=(10, 20))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        # plt.show()

        strIO = BytesIO()
        #plt.savefig(strIO, dpi=fig.dpi)
        wordcloud.to_image().save(strIO, 'PNG')
        strIO.seek(0)
        plt.close(fig)
        return strIO
    #except:
    #    print('error!!')


def streaming(word):

    global myStream
    global lastStreamingWord
    # si la nueva búsqueda es distinta a la última búsqueda entonces actualizamos
    if(lastStreamingWord != word):
        __initializeVariables()
        #Permito que inicie el streaming
        data.isRunning = True
        # si no tenemos creado el stream lo hacemos
        if(myStream == None):
            __createStreamingListener()
        # si está creado, detenemos el streaming para una nueva búsqueda
        else:
            __stopStreaming()
        # iniciamos el stream
        myStream.filter(track=__parsearQuery(word), is_async=True)
        lastStreamingWord = word
    result = model.textList()
    result.setData('True')
    return result.getResponse()

def startDemo(word):
    
    __initializeVariables()
    #Detengo el streaming en caso de búsqueda previa en tiempo real
    data.isRunning = False

    excel_file = r'back\demo_files\TweetsDemo.xlsx'
    if word=='1':
        tweets = pd.read_excel(excel_file, sheet_name='1')
        tweepyService.fake_streaming(tweets)
    else:
        tweets = pd.read_excel(excel_file, sheet_name='2')
        tweepyService.fake_streaming(tweets)        
    result = model.textList()
    result.setData('True')
    return result.getResponse()

def getTweets():
    #global streamingStore
    result = model.textList()

    if data.countTotal > 8:
        result.setData(data.streamingStore.sort_values(by='Id',
                                                       ascending=False).iloc[:8, [1, 2, 4]].to_json(force_ascii=False, orient='records'))
    if data.countTotal > 0 and len(data.streamingStore) <= 8:
        result.setData(data.streamingStore.sort_values(by='Id',
                                                       ascending=False).iloc[:, [1, 2, 4]].to_json(force_ascii=False, orient='records'))
    if data.countTotal == 0:
        return ''
    return result.getResponse()


def getDataForPieChart():
    if (data.countTotal != 0):
        result = model.chart()
        result.setData(
            [data.countAggresive, data.countNonAggresive, data.countNeutral])
        # result.setLabel(word)
        result.setChartLabels(["Agresivo", "No agresivo", "Neutro"])
        return result.getResponse()
    else:
        return ''


def getDataForLineChart():
    if len(data.streamingStore.index) > 0:
        groupedDF = data.streamingStore.copy()
        groupedDF['Fecha de creación'] = pd.to_datetime(
            groupedDF['Fecha de creación'])

        groupedDF['Cantidad'] = 1
        groupedDF = groupedDF.set_index('Fecha de creación')

        groupedDF = groupedDF.groupby(
            ['Agresivo']).resample('10S').sum().reset_index()

        # Cálculo para no agresivos
        nonAggresiveDF = groupedDF[groupedDF['Agresivo'] == 'no'].tail()
        if len(nonAggresiveDF.index) > 0:
            minNonAggresive = groupedDF['Fecha de creación'].min().strftime(
                '%Y-%m-%d %H:%M:%S')
            maxNonAggresive = nonAggresiveDF['Fecha de creación'].max().strftime(
                '%Y-%m-%d %H:%M:%S')
            chartLabelsNonAggresive = pd.date_range(
                end=maxNonAggresive, periods=5, freq='10S')
            chartLabelsNonAggresive = chartLabelsNonAggresive.strftime(
                '%H:%M:%S').tolist()

            # Cálculo para agresivos
            aggresiveDF = groupedDF[(groupedDF['Agresivo'] == 'sí') & (
                groupedDF['Fecha de creación'] >= pd.to_datetime(minNonAggresive))].tail()

            # Cálculo para neutros
            neutralDF = groupedDF[(groupedDF['Agresivo'] == 'neutro') & (
                groupedDF['Fecha de creación'] >= pd.to_datetime(minNonAggresive))].tail()

            # Relleno las listas en caso de faltantes
            valuesNonAggresive = []
            valuesAggresive = []
            valuesNeutral = []

            valuesNonAggresive = nonAggresiveDF['Cantidad'].tolist()
            valuesAggresive = aggresiveDF['Cantidad'].tolist()
            valuesNeutral = neutralDF['Cantidad'].tolist()

            valuesNonAggresive = valuesNonAggresive + \
                [0]*(5 - len(valuesNonAggresive))
            valuesAggresive = valuesAggresive + [0]*(5 - len(valuesAggresive))
            valuesNeutral = valuesNeutral + [0]*(5 - len(valuesNeutral))

            chartDataNonAggresive = {
                'values': valuesNonAggresive,
                'lineLabel': 'No agresivo'}
            chartDataAggresive = {
                'values': valuesAggresive,
                'lineLabel': 'Agresivo'}
            chartDataNeutral = {
                'values': valuesNeutral,
                'lineLabel': 'Neutro'}

            dictionaryList = []
            dictionaryList.append(chartDataNonAggresive)
            dictionaryList.append(chartDataAggresive)
            dictionaryList.append(chartDataNeutral)

            result = model.chart()
            result.setData(dictionaryList)
            result.setChartLabels(chartLabelsNonAggresive)
            return result.getResponse()
        else:
            return ''
    else:
        return ''


def getWordCloud():
    if len(data.streamingStore.index) >= 5:
        strIO = __plotWordCloud()
        return send_file(strIO, mimetype='image/png')
    return ''


def getCounters():
    counters = {}
    counters['countAggresive'] = data.countAggresive
    counters['countNeutral'] = data.countNeutral
    counters['countNonAggresive'] = data.countNonAggresive
    counters['countTotal'] = data.countTotal
    result = model.textList()
    result.setData(counters)
    return result.getResponse()


def exportExcel():
    options = {}
    options['strings_to_formulas'] = False
    options['strings_to_urls'] = False

    file_buffer = BytesIO()    
    writer = pd.ExcelWriter(file_buffer, engine='openpyxl', options=options)

    excel_df = data.streamingStore.iloc[:,[1,2,3,4]]
    excel_df['Texto'] = excel_df
    excel_df.to_excel(writer, index=False, sheet_name='Tweets')
    writer.close()

    file_buffer.seek(0)
    return send_file(file_buffer, attachment_filename="testing.xlsx", as_attachment=True)

def exportCSV():
    file_buffer = StringIO()

      # Write the dataframe to the buffer
    csv_df =  data.streamingStore.iloc[:,[1,2,3,4]]
    csv_df['Texto'] = csv_df['Texto'].apply(preprocesador.eliminar_espacios)
    csv_df.to_csv(file_buffer, encoding="utf-8", index=False, sep=",")

      # Seek to the beginning of the stream
    file_buffer.seek(0)

    response = Response(file_buffer, mimetype="text/csv")

    response.headers.set(
          "Content-Disposition", "attachment", filename="{0}.csv".format('TweetsCSV')
      )
    return response
    return send_file(xlsxData, attachment_filename='Tweets.xlsx', as_attachment=True)
