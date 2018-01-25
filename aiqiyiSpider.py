from model import *
from util import *
import traceback


def getCategroyMovieList():
    try:
        soup = BS.netUrlParser(url=config.INDEX_URL)
    except Exception as e:
        print("页面请求错误：" + config.INDEX_URL)
        print(traceback.print_exc())
        return False
    divs = BS.getElementByFind(element=soup, tag="div", param={"class": "mod_sear_list"})
    divs = divs[1:-1]
    for div in divs:
        # 获取category
        categroy_div = BS.getElementByFindFirst(element=div, tag="h3", param=None)
        categroy = categroy_div.text[:-1]
        # 获取category分类下面的title
        ul = BS.getElementByFindFirst(element=div, tag="ul", param={"class": "mod_category_item"})
        a_s = BS.getElementByFind(element=ul, tag="a", param=None)
        a_s = a_s[1:]
        for a in a_s:
            title = a.text
            url = BS.getElementByAtt(element=a, attName="href")
            # 实例categroymovie对象
            categroymovie = CategroyMovie.CategroyMovie(categroy=categroy, url=url, title=title)
            # 插入数据库
            DBUtil.categroyMovieTableAdd(categroymovie)


def getMovieList():
    movieList = list()
    urlList = DBUtil.queryUrlFromCategroyMovieTable()
    for url in urlList:
        i = 1
        while True:
            url1 = config.WEB_URL + url[0][:-16] + str(i) + url[0][-15:]
            print(url1)
            try:
                soup1 = BS.netUrlParser(url=url1)
                # 判断是否是最后一个页面
                search_page = BS.getElementByFind(element=soup1, tag="a", param={"data-search-page": "item"})[-2]
                page = BS.getElementByAtt(element=search_page, attName="data-key")
                print(page, "     ", i)
                if int(page) < i:
                    break
            except:
                print("页面请求错误：" + url1)
                print(traceback.print_exc())
                continue
            movie_ul = BS.getElementByFindFirst(element=soup1, tag="ul", param={"class": "site-piclist site-piclist-180236 site-piclist-auto"})
            movie_lis = BS.getElementByFind(element=movie_ul, tag="li", param=None)
            for li in movie_lis:

                a = BS.getElementByFindFirst(element=li, tag="a", param=None)
                # 获取电影名
                moviename = BS.getElementByAtt(element=a, attName="title")
                # 获取url
                table_url = BS.getElementByAtt(element=a, attName="href")
                # 获取图片
                li_img = BS.getElementByFindFirst(element=a, tag="img", param=None)
                img = BS.getElementByAtt(element=li_img, attName="src")
                # 获取时长
                time = BS.getElementByFindFirst(element=a, tag="span", param={"class": "icon-vInfo"}).text.strip()
                # 获取评分
                score_element = BS.getElementByFindFirst(element=li, tag="span", param={"class": "score"})
                if score_element == None:
                    score = None
                else:
                    score = score_element.text.split(">")[0]
                # 初始化一个对象
                # init__(self, moviename, time, url, imagepath, score, status = None, source = config.SOURCE)
                movie = Movie.Movie(moviename, time, table_url, "http:"+img, score)
                # 插入数据库
                DBUtil.movieTableAdd(movie)
            i += 1


                # 打印
                # print(moviename, url, img, time)


def getMovieDetail():
    while True:
        # 每次取出500个数据
        results = DBUtil.queryIdAndUrlFromMovieTable()
        if len(results) == 0:
            break
        for res in results:
            # 获取id
            id = res[0]
            # 通过获取URL获取其他信息
            try:
                soup = BS.netUrlParser(url=res[1])
                # 获取category
                category_span = BS.getElementByFindFirst(element=soup, tag="span", param={"class": "mod-tags_item"})
                category_as = BS.getElementByFind(element=category_span, tag="a", param=None)
                categroy = ""
                for category_a in category_as:
                    categroy = "," + category_a.text
                # 获取导演，看点，简介
                details = BS.getElementByFind(element=soup, tag="span", param={"class": "type-con"})
                # print(len(details))
                # print(details)
                # 获取导演
                directors = BS.getElementByFind(element=details[1], tag="a", param=None)
                director = ""
                for dir in directors:
                    director = dir.text + ","
                # 获取看点
                keywords = BS.getElementByFind(element=details[3], tag="a", param=None)
                keyword = ""
                for key in keywords:
                    keyword = key.text + ","
                keyword = keyword.strip()[:-1]
                # 获取简介
                des = details[4].text.strip()

                # 获取performer和role
                performers = BS.getElementByFind(element=soup, tag="a", param={"itemprop": "actor"})

                roles = BS.getElementByFind(element=soup, tag="span", param={"class": "type-con_div"})
                print(len(performers), len(roles))
                for i in zip(performers, roles):
                    performer, role = i
                    movieperformer = MoviePerformer.MoviePerformer(id=id, performer=performer.text, role=role.text.strip())
                    # 插入数据库movieperformertable
                    DBUtil.moviePerformerAdd(movieperformer)
                    # 获取演员个人详细信息
                    performerdetail = BS.getElementByAtt(element=performer, attName="href")

                # 获取视频连接
                # video_div = BS.getElementByFindFirst(element=soup, tag="div", param={"class": "pw-video"})
                # print(video_div)
                # video = BS.getElementByFindFirst(element=video_div, tag="video", param=None)
                # video_url = BS.getElementByAtt(element=video, attName="src")
                # print(video_url)
                # # 创建MovieUrl对象
                # movieurl = MovieUrl.MovieUrl(id=id, movieurl=video_url)
                # # 将对象插入movieurl表
                # DBUtil.movieUrlAdd(movieurl)
            except:
                print("出错：" + res[1])
                print(traceback.print_exc())
            # 创建MovieDetail实例
            moviedetail = MovieDetail.MovieDetail(id, director, keyword, categroy, des)
            DBUtil.movieDetailAdd(moviedetail)


def Preformer():
    pass


def downloadPhoto():
    pass


def performerDetail(performerdetail):
    try:
        soup = BS.getElementByFindFirst(element=performerdetail, tag="div", param={"class": "result_detail"})
        sou2 = BS.getElementByFindF(element=performerdetail, tag="dl", param={"class": "basicInfo-block basicInfo-left"})
    except:
        print("解析错误")
        print(traceback.print_exc())
    # 获取姓名
    name = BS.getElementByFindFirst(element=soup, tag="h1", param=None).text
    # 职业
    Occuption_li = BS.getElementByFindFirst(element=soup, tag="li", param={"itemprop": "jobTitle"}).text
    Occuption_li.
    Occuption = BS.getElementByFindFirst(element=Occuption_li, tag="span", param={"class": "c999"}).text.strip()
    # 生日
    birthday_li = BS.getElementByFindFirst(element=soup, tag="li", param={"itemprop": "birthdate"})
    birthday = BS.getElementByFindFirst(element=Occuption_li, tag="span", param={"class": "c999"}).text.strip()
    # 出生地
    birthplace = BS.getElementByFindFirst(element=soup, tag="li", param={"itemprop": "birthdate"})






if __name__ == '__main__':
    # getCategroyMovieList()
    # getMovieList()
    getMovieDetail()
