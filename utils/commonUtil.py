import re

from django.db.models import QuerySet
from xpinyin import Pinyin


class CommonUtil:
    @staticmethod
    def toString(Obj):
        objtype=type(Obj)
        print(objtype)


    @staticmethod
    def querySetToList(querySet,field=""):
        if(type(querySet)==QuerySet):
            list=[]
            list=[', '.join(x) for x in querySet]
            return list
        return None


    @staticmethod
    def cn_to_pinyin(cn_words):
        pinyin = Pinyin().get_pinyin(cn_words).replace('-','').lower()
        pattern = re.compile('\\w*')
        result1 = pattern.findall(pinyin)
        result1 = ''.join(result1)
        return (result1.replace("_",''))



