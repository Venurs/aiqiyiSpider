from model import *
from util import *
import traceback
import json


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
            # print("start")
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
            try:
                soup1 = BS.netUrlParser(url=url1)
                # 判断是否是最后一个页面
                search_page = BS.getElementByFind(element=soup1, tag="a", param={"data-search-page": "item"})[-2]
                page = BS.getElementByAtt(element=search_page, attName="data-key")
                if int(page) < i:
                    break
            except:
                # print("页面请求错误：" + url1)
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
                movie = Movie.Movie(moviename, time, table_url, "http:"+img, score)
                # 插入数据库
                DBUtil.movieTableAdd(movie)
            i += 1


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

                getMovieDetailTable(id, soup)

                getPerformer(id, soup)

            except:
                print("出错：" + res[1])
                print(traceback.print_exc())


def downloadPhoto():
    while True:
        results = DBUtil.queryImageUrlAndSaveImagePathFromMovieTable()
        if len(results) == 0:
            break
        for re in results:
            url, path = re[0], re[1]
            DownLoadUtil.createFile(path=path)
            DownLoadUtil.downLoadPhotoForRequest(url=url, path=path)
            DBUtil.updateMovieTableStatus(param=re)


def performerDetail(performerdetail):
    """
    获取演员的详细信息，一共19项数据
    :param performerdetail: 演员详细信息界面的文档流
    :return: 已经初始化的演员实例
    """
    try:
        url_performer = "http:" + performerdetail
        soup = BS.netUrlParser(url=url_performer)
    except:
        print("演员信息页面请求错误" + url_performer)
    try:
        soup1 = BS.getElementByFindFirst(element=soup, tag="div", param={"class": "result_detail"})
        soup_left = BS.getElementByFindFirst(element=soup, tag="dl", param={"class": "basicInfo-block basicInfo-left"})
        soup_right = BS.getElementByFindFirst(element=soup, tag="dl", param={"class": "basicInfo-block basicInfo-right"})
    except:
        print("解析错误")
        print(traceback.print_exc())
    #获取姓名
    name = BS.getElementByFindFirst(element=soup1, tag="h1", param=None).text
    # 获取图片
    img_div = BS.getElementByFindFirst(element=soup, tag="div", param={"class": "result_pic"})
    img = BS.getElementByFindFirst(element=img_div, tag="img", param={"itemprop": "image"})
    imgurl = BS.getElementByAtt(element=img, attName="src")
    # # 职业
    Occuption_li = BS.getElementByFindFirst(element=soup1, tag="li", param={"itemprop": "jobTitle"})
    occuption_str = Occuption_li.text.strip().replace(" ", "").replace("\n", "")
    Occuption = occuption_str[occuption_str.rfind("：") + 1:]
    # # 体重
    weight_li = BS.getElementByFindFirst(element=soup1, tag="li", param={"itemprop": "weight"}).text.strip().replace(" ", "").replace("\n", "")
    weight = weight_li[weight_li.rfind("：") + 1:]
    # 简介
    introduce = BS.getElementByFindFirst(element=soup, tag="p", param={"class": "introduce-info"}).text
    # 获取表格文档流
    dds_left = BS.getElementByFind(element=soup_left, tag="dd", param={"class": "basicInfo-item basicInfo-value"})
    dds_right = BS.getElementByFind(element=soup_right, tag="dd", param={"class": "basicInfo-item basicInfo-value"})
    # 从表格获取其他信息
    # 外文名
    e_name = dds_left[0].text.strip().replace(" ", "").replace("\n", "")
    # 性别
    sex = dds_left[1].text.strip().replace(" ", "").replace("\n", "")
    # 身高
    height = dds_left[2].text.strip().replace(" ", "").replace("\n", "")
    # 出生日期
    birthday = dds_left[3].text.strip().replace(" ", "").replace("\n", "")
    # 出生地
    birthplace = dds_left[4].text.strip().replace(" ", "").replace("\n", "")
    # 毕业院校
    school = dds_left[5].text.strip().replace(" ", "").replace("\n", "")
    # 成名年代
    fameyear = dds_left[6].text.strip().replace(" ", "").replace("\n", "")
    # 别名
    alias = dds_right[0].text.strip().replace(" ", "").replace("\n", "")
    # 血型
    bloodtype = dds_right[1].text.strip().replace(" ", "").replace("\n", "")
    # 地区
    address = dds_right[2].text.strip().replace(" ", "").replace("\n", "")
    # 星座
    constellation = dds_right[3].text.strip().replace(" ", "").replace("\n", "")
    # 现居地
    location = dds_right[4].text.strip().replace(" ", "").replace("\n", "")
    # 经纪公司
    brokerageagency = dds_right[5].text.strip().replace(" ", "").replace("\n", "")
    # 爱好
    hobby = dds_right[6].text.strip().replace(" ", "").replace("\n", "")
    """
    __init__(self, name, e_name, alias, sex, bloodtype, height, address,
                 birthday, constellation, location, ResidentialAddress, school,
                 BrokerageAgency, fameyear, hobby, Occupation, weight, image, des)
    
    """
    performer = PerformerDetail.PerformerDetail(name=name, e_name=e_name, alias=alias, sex=sex, bloodtype=bloodtype,
                                                height=height, address=address, birthday=birthday,
                                    constellation=constellation, location=location,
                                    ResidentialAddress=birthplace, school=school, BrokerageAgency=brokerageagency,
                                     fameyear=fameyear, hobby=hobby, Occupation=Occuption,
                                    weight=weight, image=imgurl, des=introduce)
    return performer


def getKeyword(soup):
    """
    解析json数据，获取视频的看点
    :param soup: 页面的html文档流
    :return: 返回视频的看点，字符串
    """
    try:
        p_movieid = BS.getElementByFindFirst(element=soup, tag="p", param={"id": "data-videopoint"})
        movieid = BS.getElementByAtt(element=p_movieid, attName="data-qipuid")
    except:
        print("获取看点是解析html错误")
    keyword_url = "http://qiqu.iqiyi.com/apis/video/tags/get?entity_id=" + movieid + "&limit=10"
    keyword_json = HttpUtil.getURLHtml(url=keyword_url, param=None)
    keyword_data = json.loads(keyword_json)
    data = keyword_data.get("data")
    keyword = ""
    for i in range(10):
        keyword = data[i].get("tag") + ","
    keyword = keyword[:-1]
    return keyword


def getMovieDetailTable(id, soup):
    """
    获取电影的详细信息，并将获取的信息封装，存入数据库表movietable
    :param soup: 页面的html文档流
    :return:
    """
    # 获取category
    category_span = BS.getElementByFindFirst(element=soup, tag="span", param={"class": "mod-tags_item"})
    category_as = BS.getElementByFind(element=category_span, tag="a", param=None)
    categroy = ""
    for category_a in category_as:
        categroy = "," + category_a.text
    # 获取导演，看点，简介
    details = BS.getElementByFind(element=soup, tag="span", param={"class": "type-con"})
    # 获取导演
    directors = BS.getElementByFind(element=details[1], tag="a", param=None)
    director = ""
    for dir in directors:
        director = dir.text + ","
    # 获取看点
    keyword = getKeyword(soup)
    # 获取简介
    des = details[4].text.strip()
    # 创建MovieDetail实例
    moviedetail = MovieDetail.MovieDetail(id, director, keyword, categroy, des)
    DBUtil.movieDetailAdd(moviedetail)


def getPerformer(id, soup):
    """
    1.获取电影的演员及扮演角色信息，并封装成对象，存入数据库表movieperformertable
    2.获取演员的详细信息，包括19项内容，并将信息封装城对象，存入数据库表performerdetailtable
    :param soup: 页面的html文档流
    :return:
    """
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
        performer = performerDetail(performerdetail)
        # 插入数据库performerdetailtable
        DBUtil.performerDetailAdd(performer)



