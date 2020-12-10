class Tweet:
    def __init__(self,id=0,texto='', fecha='',fuente=''):
        self.id = id
        self.texto = texto
        self.fecha = fecha
        self.fuente = fuente

    def obtener_texto(self):
        return self.texto

    def obtener_fecha(self):
        return self.fecha
    
    def obtener_fuente(self):
        return self.fuente

    def to_dict (self):
        return {
            'Id':self.id,
            'Texto':self.texto,
            'Fecha de creación':self.fecha,
            'Fuente':self.fuente
        }