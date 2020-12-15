import re

def normalizar_insultos(tweet):
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

print(normalizar_insultos('flaca 1ero CITAME EL puto TUIT DEJA D DAR VUELTAS, 2do queres q tengan respeto hacia todas pero vos no respetas a los otros pq opinan diferente, y 3to a nadie le importa si no queres aborto https://t.co/LrmhsRWxQR'))