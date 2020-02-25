'''
时间帮助类
'''
from datetime import datetime
from random import randrange


class DateTimeUtil:

    '''
        根据时间生成随机名
    '''
    @staticmethod
    def randTimeName():
        rand=rand= randrange(1, 100000, 1)
        dt=datetime.now()
        return ('%s%s%s%s%s%s%s%s') % \
               (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond,rand)

    '''
        格式化时间，返回字符串
    '''

    @staticmethod
    def formatTime(format):
        dt=datetime.now()
        if(isinstance(format, str) and len(format)>0):
            return dt.strftime(format)
        else:
            return dt.strftime('%Y-%m-d %H:%M:%S')



