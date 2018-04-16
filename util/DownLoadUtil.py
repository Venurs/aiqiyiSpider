import urllib
import requests
import os

"""
url 网络地址
path 本地保存地址
"""
def downLoadPhotoForUrllib(url,path):
    isSuccess = createFile(path)
    if isSuccess == True:
        # 文件存在
        return False
    #进行保存
    try:
        urllib.request.urlretrieve(url,path)
        return True
    except:
        return False


"""

"""
def downLoadPhotoForRequest(url,path):
    isSuccess=createFile(path)
    if isSuccess:
        #文件存在
        print("文件存在")
        return False
    #发起请求
    ir=requests.get(url, stream=True)
    if ir.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in ir:
                f.write(chunk)
        return True
    else:
        return False




def createFile(path):
    isExists = os.path.exists(path)
    if isExists:
        return True
    #不存在的情况下获得上一级目录
    path1 = os.path.abspath(os.path.join(os.path.dirname(path)))
    if not os.path.exists(path1):
        #进行创建相关目录
        os.makedirs(path1)
    return False


def getFileNum(path):
    isFile = os.path.isfile(path)
    if isFile:
        #如果是文件，获取上一级路径
        path = os.path.abspath(os.path.dirname(path))

    #获取当前文件夹下的文件数量
    num = os.listdir(path)
    return len(num)


