import stanza 
import pickle
import os

from nltk import TweetTokenizer

class HelperEtiquetador:

    def __init__(self):
        self.path_pos = 'back/tags/gramaticas.pkl'
        self.path_lemas = 'back/tags/lemas.pkl'

        if os.path.getsize(self.path_pos) >0:
            self.cache_pos = self.cargar_cache(self.path_pos)
        else: 
            self.cache_pos={}

        if os.path.getsize(self.path_lemas) >0:
            self.cache_lemas = self.cargar_cache(self.path_lemas)
        else: 
            self.cache_lemas={}
                
        self.nlp = stanza.Pipeline(
    lang='es', processors='tokenize,mwt,pos,lemma', tokenize_no_ssplit=True, verbose=False)
        self.tokenizer = TweetTokenizer()

    # Devuelve una lista de diccionarios con etiqueta gramatical
    def etiquetar_gramatica(self, tweet):
        etiquetas = []
        tokens = self.tokenizer.tokenize(tweet)

        for token in tokens:
            if token in self.cache_pos:
                etiquetas.append(self.cache_pos.get(token))
            else:
                palabra= self.actualizar_gramatica(token)
                etiquetas.append(palabra['pos'])
        #self.guardar_cache(self.cache_pos,self.path_pos)
        #self.guardar_cache(self.cache_lemas, self.path_lemas)

        return ' '.join(etiquetas)

    # Devuelve lista de lemas
    def lematizar_gramatica(self, tweet):
        lemas = []
        tokens = self.tokenizer.tokenize(tweet)

        for token in tokens:
            if token in self.cache_lemas:
                lemas.append(self.cache_lemas.get(token))
            else:
                palabra= self.actualizar_gramatica(token)
                lemas.append(palabra['lema'])
        #self.guardar_cache()
        return ' '.join(lemas)

    def cargar_cache(self,path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    def guardar_cache(self):
        self.guardar_cache_pos()
        self.guardar_cache_lemas()

    def guardar_cache_pos(self):
        with open(self.path_pos, 'wb') as f:
            pickle.dump(self.cache_pos, f, pickle.HIGHEST_PROTOCOL)

    def guardar_cache_lemas(self):
        with open(self.path_lemas, 'wb') as f:
            pickle.dump(self.cache_lemas, f, pickle.HIGHEST_PROTOCOL)

    def agregar_nueva_pos(self,etiquetas):
        self.cache_pos[etiquetas['text']] = etiquetas.get('pos')
    
    def agregar_nuevo_lema(self,etiquetas):
        self.cache_lemas[etiquetas['text']] = etiquetas.get('lema')
    
    def actualizar_gramatica(self,token):
        doc = self.nlp(token)
        gramatica ={
        'text' : doc.sentences[0].words[0].text,
        'lema' : doc.sentences[0].words[0].lemma,
        'pos' : doc.sentences[0].words[0].pos
        }
        self.agregar_nueva_pos(gramatica)
        self.agregar_nuevo_lema(gramatica)
        return gramatica