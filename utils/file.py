'''
文件目录帮助类
'''
import os
import shutil

from utils.commonUtil import CommonUtil


class FileUtil:

    '''
    处理文件路径
    '''

    @staticmethod
    def cleanPath(path):
        path=path.strip('\\');
        return path

    '''
    判断路径是否存在
    '''

    @staticmethod
    def isExists(path):
        return os.path.exists(path)

    '''
    新建目录
    '''
    @staticmethod
    def mkdir(dir,isMany):
        dir=''.join(dir);
        CommonUtil.toString(dir)
        dir=FileUtil.cleanPath(dir)
        if(FileUtil.isExists(dir)):
            return False
        else:
            try:
                if(isMany==True):
                    os.makedirs(dir)
                else:
                    os.mkdir(dir)
            except:
                return False
            return True

    '''
    删除目录
    '''
    @staticmethod
    def removeDir(dir,isRemoveAll):
        try:
            if(isRemoveAll):
                shutil.rmtree(dir)
            else:
                os.rmdir(dir)
            return True
        except:
            return False

    '''
    重命名
    '''
    @staticmethod
    def reName(oldName,newName):
        try:
            os.rename(oldName,newName)
            return True
        except:
            return False

    '''
        按行读取文件
    '''
    @staticmethod
    def readFileLines(path):
        try:
            f=open(path,'r',encoding='utf-8')
            list_lines=f.readlines();
            for line in list_lines:
                line=line.rstrip();
            return ''.join(list_lines);
        except:
            return '';

    @staticmethod
    def writeFileBytes(path,content):
        with open(path, 'w',encoding='utf8') as f:
            f.write(content)






