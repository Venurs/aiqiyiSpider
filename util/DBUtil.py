import mysql.connector as mysql
from util import config



"""
查询语句
成功返回 查询结果
失败返回None
"""


def selectSQL(sql):
    cnx = mysql.connect(user=config.USER, password=config.PASSEORD, host=config.HOST, database=config.DATABASE)
    try:
        cursor = cnx.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        cnx.close()
    return None


def executeSQL(sql, param=()):
    """
    执行数据库的插入 删除  修改操作
    :param sql: 数据库语句
    :param param: 所需要的参数，不需要参数时为空
    :return: 执行成功与否
    """
    cnx = mysql.connect(user=config.USER, password=config.PASSEORD, host=config.HOST, database=config.DATABASE)
    try:
        cur = cnx.cursor()
        print(sql)
        print(param)
        cur.execute(sql, param)
        cnx.commit()
        return True
    except:
        cnx.rollback()
        return False
    finally:
        cnx.close()


def categroyMovieTableAdd(models):
    results = selectSQL("SELECT * FROM categroymovietable WHERE url = '%s' AND title = '%s'" % (models.url, models.title))
    if results != None and len(results) > 0:
        return False
    sql = 'INSERT INTO categroymovietable(categroy, url, title, source) VALUES (%s,%s,%s,%s)'
    param = list()
    param.append(models.categroy)
    param.append(models.url)
    param.append(models.title)
    param.append(models.source)
    params = tuple(param)
    isSuccess = executeSQL(sql=sql, param=params)
    return isSuccess


def queryUrlFromCategroyMovieTable():
    sql = "SELECT url FROM categroymovietable"
    results = selectSQL(sql=sql)
    return results


def movieTableAdd(models):
    results = selectSQL("SELECT * FROM movietable WHERE moviename = '%s' AND url = '%s'" % (models.moviename, models.url))
    if len(results) > 0:
        return False
    sql = "INSERT INTO movietable(moviename, time, url, imagepath, saveimagepath, score, status, source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    param = list()
    param.append(models.moviename)
    param.append(models.time)
    param.append(models.url)
    param.append(models.imagepath)
    param.append(models.saveimagepath)
    param.append(models.score)
    param.append(models.status)
    param.append(models.source)
    params = tuple(param)
    isSuccess = executeSQL(sql=sql, param=params)
    return isSuccess


def queryIdAndUrlFromMovieTable():
    results = selectSQL("SELECT id, url FROM movietable LIMIT 500")
    return results


def movieDetailAdd(models):
    results = selectSQL("SELECT * FROM moviedetailtable WHERE id = '%s'" % models.id)
    if len(results) > 0:
        return False
    sql = "INSERT INTO moviedetailtable VALUES (%s,%s,%s,%s,%s)"
    param = list()
    param.append(models.id)
    param.append(models.director)
    param.append(models.keyword)
    param.append(models.categroy)
    param.append(models.des)
    params = tuple(param)
    isSuccess = executeSQL(sql=sql, param=params)
    return isSuccess


def moviePerformerAdd(models):
    results = selectSQL("SELECT * FROM movieperformertable WHERE id = '%s'" % models.id)
    if len(results) > 0:
        return False
    sql = "INSERT INTO movieperformertable VALUES (%s,%s,%s)"
    param = list()
    param.append(models.id)
    param.append(models.performer)
    param.append(models.role)
    params = tuple(param)
    isSuccess = executeSQL(sql=sql, param=params)
    return isSuccess


def movieUrlAdd(models):
    results = selectSQL("SELECT * FROM movieurl WHERE id = '%s'" % models.id)
    if len(results) > 0:
        return False
    sql = 'INSERT INTO movieurl VALUES (%s,%s)'
    param = list()
    param.append(models.id)
    param.append(models.movieurl)
    params = tuple(param)
    isSuccess = executeSQL(sql=sql, param=params)
    return isSuccess