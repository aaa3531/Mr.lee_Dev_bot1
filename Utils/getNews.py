import requests
import datetime
from bs4 import BeautifulSoup
import re
import Utils.hashUtil as hashUtil
# import hashUtil
import json


'''
TODO
함수 하나로 묶기
url, css selector 데이터베이스에 넣어서 수정 쉽게 하기
'''

with open('/home/ubuntu/telegram_bot2/latestNews.json', 'r') as f:
    latest_news = json.load(f)



def getThinkPoolNews():
    '''
    씽크풀 뉴스
    '''    
    try:
        data = []
        thinkpoll_url = "http://www.thinkpool.com/nnews/realtime/"
        res = requests.get(thinkpoll_url+"list.jsp")
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.select("body > table > tr > td > nobr")
        for i in contents:
            if i.a['href'] == latest_news['thinkpool']:
                break
            data.append({"title": i.get_text(), "link": thinkpoll_url+i.a['href'], 'keyword': [], 'company': 'thinkpool', 'describe': i.get_text()})
        latest_news['thinkpool'] = contents[0].a['href']
        if len(data) > 15:
            print("News might be duplicated", [getThinkPoolNews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent="\t")
    
        return data
    except Exception as e:
        print("Error occurred : ", [getThinkPoolNews.__name__, e])
        return []


# 네이버 뉴스는 2분정도 느림
def getNaverNews():
    '''
    네이버 뉴스
    '''    
    try:
        data = []
        res = requests.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=101", headers={'User-Agent':'Mozilla/5.0'})
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.select("#main_content > div.list_body.newsflash_body > ul > li > dl > dt:not(.photo) > a")
        describe = soup.select("#main_content > div.list_body.newsflash_body > ul > li > dl > dd > span.lede")
        for i in range(len(contents)):
            if hashUtil.get_hash_value(contents[i].get_text().strip(), 16, 'number') == latest_news['naver']:
                break
            data.append({'title': contents[i].get_text().strip(), 'link': contents[i]["href"], 'keyword': [], 'company': 'naver', 'describe': describe[i].get_text()})

        latest_news['naver'] = hashUtil.get_hash_value(contents[0].get_text().strip(), 16, 'number')
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getNaverNews.__name__, e])
        return []

# 스포츠/연예 관련 뉴스가 같이 나옴
# def getMKNews():
#     '''
#     매일경제
#     '''
#     data = []
#     today = datetime.today().strftime("%Y/%m/%d")
#     mk_url = f"https://www.mk.co.kr/sitemap/{today}"
#     res = requests.get(mk_url, headers={'User-Agent':'Mozilla/5.0'})
#     soup = BeautifulSoup(res.content.decode('euc-kr', 'replace'), "html.parser")
#     cont = soup.select("#container > div.sitemap_article2 > ul.articles_list > li > a")
#     for i in cont:
#         if i.get_text() == mock_db['mk']:
#             mock_db['mk'] = cont[0].get_text()
#             return data
#         data.append({"title": i.get_text(), "link": i["href"]})
        
#     return data

def getEdailyNews():
    '''
    이데일리
    '''   
    try:
        data = []
        edaily_url = "https://www.edaily.co.kr/news/realtimenews?tab=0"
        news_url = "https://www.edaily.co.kr/news/read?newsId="
        res = requests.get(edaily_url, headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select("#sticker02 > div.news_list > dl > dd > a")
        for i in contents:
            if re.findall("\d+", i['href'])[0] == latest_news['edaily']:
                break
            data.append({'title': i.get_text(), 'link': news_url + re.findall("\d+", i['href'])[0], 'keyword': [], 'company': 'edaily', 'describe': i.get_text()})
        latest_news['edaily'] = re.findall("\d+", contents[0]['href'])[0]
        if len(data) > 15:
            print("News might be duplicated", [getEdailyNews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent="\t")

        return data
    except Exception as e:
        print("Error occurred : ", [getEdailyNews.__name__, e])
        return []
        

def getInfostockDailyNews():
    '''
    인포스탁데일리
    '''
    try:
        data = []
        infostock_url = "http://www.infostockdaily.co.kr/news/articleList.html?view_type=sm"
        news_url = "http://www.infostockdaily.co.kr"
        res = requests.get(infostock_url, headers={'User-Agent':'Mozila/5.0'})
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select("#user-container > div.float-center.max-width-1080 > div.user-content > section > article > div.article-list > section > div.list-block > div.list-titles > a")
        describe = soup.select('#user-container > div.float-center.max-width-1080 > div.user-content > section > article > div.article-list > section > div > p > a')
        for i in range(len(contents)):
            if contents[i]['href'] == latest_news['infostock']:
                break
            data.append({'title': contents[i].get_text(), 'link': news_url + contents[i]['href'], 'keyword': [], 'company': 'infostockdaily', 'describe': describe[i].get_text().strip()})
        latest_news['infostock'] = contents[0]['href']
        if len(data) > 15:
            print("News might be duplicated", [getInfostockDailyNews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent="\t")
        
        return data
    except Exception as e:
        print("Error occurred : ", [getInfostockDailyNews.__name__, e])
        return []

def getChosunBizNews():
    '''
    조선비즈
    '''
    try:
        data = []
        chosun_biz_url = 'https://biz.chosun.com/svc/list_in/list.html'
        res = requests.get(chosun_biz_url)        
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select("#contents > div > div.news_cont_area > div.list_cont_wrap > div.list_content > dl > dt > a")
        describe = soup.select('#contents > div > div.news_cont_area > div.list_cont_wrap > div.list_content > dl > dd.desc')
        for i in range(len(contents)):
            if contents[i]['href'] == latest_news['chosunBiz']:
                break
            data.append({'title': contents[i].get_text(), 'link': 'https:'+contents[i]['href'], 'keyword': [], 'describe': describe[i].get_text()})
        latest_news['chosunBiz'] = contents[0]['href']
        if len(data) > 9:
            print("News might be duplicated", [getChosunBizNews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getChosunBizNews.__name__, e])
        return []

def getHankyungNews():
    '''
    한국경제
    '''
    try:
        data = []
        hk_economy_url = 'https://www.hankyung.com/all-news'
        res = requests.get(hk_economy_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select('#container > div.contents_wrap > div.contents > div.article_content > div.daily_article > div > ul > li > div > h3 > a')
        describe = soup.select('#container > div.contents_wrap > div.contents > div.article_content > div.daily_article > div > ul > li > div > p.read')
        for i in range(len(contents)):
            if contents[i]['href'] == latest_news['hankyung']:
                break
            data.append({'title': contents[i].get_text(), 'link': contents[i]['href'], 'keyword': [], 'describe': describe[i]})
        latest_news['hankyung'] = contents[0]['href']
        if len(data) > 15:
            print("News might be duplicated", [getHankyungNews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getHankyungNews.__name__, e])
        return []

def getMoneyTodayNews():
    '''
    머니투데이
    '''
    try:
        data = []
        #해당 url의 html을 가져옴
        moneytoday_url = 'https://news.mt.co.kr/newsflash/newsflash.html?sec=all&listType=left'
        res = requests.get(moneytoday_url)
        #css를 기준으로 원하는 태그를 찾음.
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select('#articleList > div > div.group > ul > li > strong > a')
        for i in contents:
            #3초전의 뉴스와 새로 가져온 뉴스의 제목이 같다면 종료
            if i["href"][33:-7] == latest_news['moneytoday']:
                break
            #최근 뉴스 추가
            data.append({'title': i.get_text(), 'link': "https://news.mt.co.kr/mtview.php?no=" + i['href'][33:-7], 'keyword': [], 'describe': i.get_text()})
        latest_news['moneytoday'] = contents[0]['href'][33:-7]
        if len(data) > 15:
            print("News might be duplicated", [getMoneyTodayNews.__name__, datetime.datetime.today()])
            print(data)
            return []        
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getMoneyTodayNews.__name__, e])
        return []

def getFnnews():
    '''
    파이낸셜 뉴스
    '''
    try:
        data = []
        fnnews_url = 'https://www.fnnews.com/newsflash/'
        res = requests.get(fnnews_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select('#root > div.contents > div > div > ul > li > a')
        describe = soup.select('li > a:nth-child(2) > p')
        for i in contents:
            if i['href'] == latest_news['fnnews']:
                break
            #최근 뉴스 추가
            data.append({'title': i.find('div', class_='news_tit').get_text().strip(), 'link': 'https://fnnews.com/' + i['href'], 'keyword': [], 'describe': i.find('div', class_='news_tit').get_text().strip()})
        latest_news['fnnews'] = contents[0]['href']
        if len(data) > 15:
            print("News might be duplicated", [getFnnews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getFnnews.__name__, e])
        return []
    
def getSedaily():
    '''
    서울경제
    '''
    try:
        data = []
        fnnews_url = 'https://www.sedaily.com/News/HeadLine/HeadLineListAjax?NClass=AL&Page=1'
        news_url = 'https://sedaily.com/NewsView/'
        res = requests.get(fnnews_url)
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')
        contents = soup.select('div > ul > li > a')
        for i in contents:
            if i['href'] == latest_news['sedaily']:
                break
            #최근 뉴스 추가]
            data.append({'title': i.get_text().strip(), 'link': news_url + i['href'].replace("javascript:NewsView('", '').replace("')", ''), 'keyword': [], 'describe': i.get_text().strip()})
        latest_news['sedaily'] = contents[0]['href']
        if len(data) > 15:
            print("News might be duplicated", [getSedaily.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getSedaily.__name__, e])
        return []

def getAsiaeNews():
    try:
        data = []
        asiae_url = 'https://www.asiae.co.kr/realtime/sokbo_left.htm'
        news_url = 'https://www.asiae.co.kr'
        form_data = {
            'pg':1,
            'tab':1,
            'rtime':180,
            'ltype':2,
            'settime':'on',
            'list_type':'on',
        }
        res = requests.post(asiae_url, form_data)
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select('#left > div > form > div > dl')
        for i in contents:
            if i.dt.a['href'] == latest_news['asiae']:
                break
            #최근 뉴스 추가
            data.append({'title': i.dt.a.get_text().strip(), 'link': news_url + i.dt.a['href'], 'keyword': [], 'describe': i.find('dd', class_ = lambda x: x != 'photo').get_text()})
        latest_news['asiae'] = contents[0].dt.a['href']
        if len(data) > 15:
            print("News might be duplicated", [getAsiaeNews.__name__, datetime.datetime.today()])
            print(data)
            return []
        with open('/home/ubuntu/telegram_bot2/latestNews.json', 'w', encoding='utf-8') as modified:
            json.dump(latest_news, modified, indent='\t')

        return data
    except Exception as e:
        print("Error occurred : ", [getAsiaeNews.__name__, e])
        return []
