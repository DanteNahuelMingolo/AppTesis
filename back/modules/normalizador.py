import re
import stanza

from sklearn.base import BaseEstimator, TransformerMixin
from preprocesador import Preprocesador


class Normalizador(BaseEstimator, TransformerMixin):
    
    def __init__(self, risa=True, leng_inclusivo=True,insultos=True, entidades=True, 
                citas=True):
        self.risa = risa
        self.leng_inclusivo = leng_inclusivo
        self.insultos = insultos
        self.entidades = entidades
        self.citas = citas
        self.prep = Preprocesador()
        self.nlp = stanza.Pipeline(
             lang='es', processors='tokenize,ner', tokenize_no_ssplit=True, verbose=False)


    # Método fit para poder usar pipelines
    def fit(self, tweets, y=None):
        # Se retorna a sí mismo porque no se "aprende" nada
        return self

    # Método transform para poder usar pipelines
    def transform(self, tweets):
        return [self.normalizar(tweet) for tweet in tweets]
        
    # Reemplaza cualquier "jajajaja" y sus combinaciones por "risa"
    def normalizar_risa(self, tweet):
        if tweet:
            tweet = re.sub(r'\b(?=\w*[j])[aeiouj]{4,}\b', ' laughtw ', tweet, flags=re.IGNORECASE)
            tweet = re.sub(r'lol|\bxd\b|lmao', ' laughtw ', tweet, flags=re.IGNORECASE)
            return tweet
        else:
            return ' '

    # Normaliza los términos del lenguaje inclusivo
    def normalizar_leng_inclusivo(self, tweet):
        if tweet:
            tweet = re.sub(r'diputad(@|x|e)s', 'diputados', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'chic(x|@)s|chiques', 'chicos', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'chique|chic(@|x)', 'chico', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'hermos(x|@|e)s', 'hermosos', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'hij(e|@|x)s', 'hijos', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'hij(e|x|@)', 'hijo', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'pib(x|@)s', 'pibes', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'much(x|@|e)s', 'muchos', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'pib(x|@)', 'pibe', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'comp(x|e)s', 'compañeros', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'compañer(@|e)', 'compañero', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'escuchad(x|e|@)s', 'escuchados', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'\b(ell?(e|@|x)s)\b', 'ellos', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'tod(e|x|@)s', 'todos', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'\b(ell?(e|@|x))\b', 'ella', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'\b(l(x|@)s)\b', 'los', tweet, flags = re.IGNORECASE)
            tweet = re.sub(r'nosotr(e|x|@)s', 'nosotros',tweet,flags=re.IGNORECASE)
            return tweet
        else:
            return ' '

    # Normalizo insultos presentes en cada tweet
    def normalizar_insultos(self, tweet):
        if tweet:
            tweet = re.sub(r'\b(pelotudit(e|a|o)(s)?|pelotud(o|a|e)s?|romper l(o|a|e)s huev(o|e)s|concha(.*)lora|(re)?conchas?|conchud(a|e|o)s?|mierdas?|\
            |mal(.*)parid(a|o)s?|cabeza de termo|est(ú|u)pid(e|x|@)s?|tarad(o|a)s?|bolude(z|s|ces)?|pelotude(z|s)|pelotudeces?|bolud(x|o|a)s?|imb(é|e)cil(es)?|\
            |mon?g(ó|o)lic(a|o)s?|(huevos?|bolas?) llenos?|pelotas llenas|romp(e|er|en|an)(.*)(pelotas?|bolas?)|cajeta|peter(o|a)s?|culos?|pijas?|yeguas?|suda(k|c)as?|\
            |ortos?|fachos?|put(a|e|o)s?( madre)?|hij(o|a)s? de (re mil |remil |mil )?putas?|feminazis?|femiprogres?|marimachos?|pajer(a|o)s?|aborteras?|chupa(.*)huevos?|\
            |chot(a|o)s?|vergas?|provincian(a|o)s?|soret(e|a)s?|cag(o|ó)n(a|e)?s?|lptm|lym|lpm|hdps?|ctm|ogt|hdrmp|lctdm|hijueputas?|choriplaner(a|o)s?|gil(e|a)?s?|ojetes?|\
            |culiad(e|a|o)s?|cagar(on|r(á|a)n|l(a|o)s?|les?|te|nos)?|caga(n|mos|te)?)\b', 'cursingtw', tweet, flags=re.IGNORECASE)
            return tweet
        else:
            return ' '

    # Normalizo entidades: Mauricio Macri, Cámara de Diputados
    def normalizar_entidades(self, tweet):
        if tweet:
            original_tweet=tweet
            tweet = self.prep.eliminar_hashtag(tweet)
            tweet = self.prep.eliminar_menciones(tweet)
            #tweet = self.normalizar_insultos(tweet)
            #tweet = self.normalizar_leng_inclusivo(tweet)
            tweet = self.prep.expandir_abreviaciones(tweet)
            tweet = self.prep.eliminar_urls(tweet)
            tweet = self.prep.eliminar_puntuacion(tweet)

            doc = self.nlp(tweet)
            for ent in doc.ents:
                original_tweet =original_tweet.replace(ent.text,'entitytw')
            return (original_tweet)
        else:
            return ' '      
    
    # Normalizo comillas y dos puntos, presentes en tweets neutros
    def normalizar_citas(self,tweet):
        if tweet:
            tweet = re.sub(r'(?<!https)((:)|(\|)|("|“)|(\'))',' quotetw ',tweet,flags=re.IGNORECASE)
            return tweet
        else:
            return ' '

    def normalizar(self, tweet):
        # identifica y reemplaza todas las expresiones del tipo "jajaja"
        if self.risa:
            tweet = self.normalizar_risa(tweet)
        # normaliza varios términos como "todes, todxs, tod@s" por "todos"
        if self.leng_inclusivo:
           tweet = self.normalizar_leng_inclusivo(tweet)
        # normaliza insultos comunes
        if self.insultos:
            tweet = self.normalizar_insultos(tweet)
        # normaliza entidades (Mauricio Macri, Cámara de Diputados)
        if self.entidades:
            tweet = self.normalizar_entidades(tweet)
        # normaliza las comillas y los dos puntos, encontrados en tweets neutros
        if self.citas:
            tweet = self.normalizar_citas(tweet)

        return tweet

