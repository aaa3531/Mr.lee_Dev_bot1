from Utils.excelUtils import getColumnData
from Utils.telegramUtils import sendMessage
import Utils.getNews as getNews
import time
import psutil
import os
import datetime
from collections import defaultdict
import DB.Database as db

my_token = '1570819804:AAGeHTU4gyirsIBVbTUAAOFM5Ebh0BPrMss' #@telegram_bot
#chat_id = "-1001424452588"
# chat_id = "-1001255369898" #testchanel
chat_id = "-1001249399947"

def bot():
    '''
    TODO
    언론사 한번에 가져와서 확장성 및 가시성 높이기
    '''
    #데이터베이스 연결
    database = db.DB()
    count_company = defaultdict(int)
    filtered_news = []
    #코스피, 코스닥 종목 가져오기
    kospi_csv = open("krxData/kospi.csv", "rt", encoding="UTF8")
    kosdaq_csv = open("krxData/kosdaq.csv", "rt", encoding="UTF8")
    kospi_corp = getColumnData(kospi_csv, 2)
    kosdaq_corp = getColumnData(kosdaq_csv, 2)
    krx_corp = kospi_corp + kosdaq_corp
    #뉴스 긁어오기
    thinkpool_news = getNews.getThinkPoolNews()
    edaily_news = getNews.getEdailyNews()
    infostock_news = getNews.getInfostockDailyNews()
    chosunBiz_news = getNews.getChosunBizNews()
    fnnews = getNews.getFnnews()
    #naver_news = getNews.getNaverNews()
    sedaily_news = getNews.getSedaily()
    hankyung_news = getNews.getHankyungNews()
    moneytoday_news = getNews.getMoneyTodayNews()
    asiae_news = getNews.getAsiaeNews()
    all_news = edaily_news + infostock_news + thinkpool_news + chosunBiz_news + hankyung_news + moneytoday_news + fnnews + sedaily_news + asiae_news

    for i in all_news:
        for j in krx_corp:
            if j in i['describe']:
                #키워드출현 개수
                i['keyword'].append(j)
                count_company[j] += 1
        if i['keyword'] != []:
            filtered_news.append(i)


    #출현 단어 개수 디비 삽입
    count_company_data = {"created_at": datetime.datetime.now(), "company": dict(count_company)}
    database.insert_one(dict(count_company_data), 'telegramBot', 'count_data') 

    for i in filtered_news:
        #텔레그램으로 메세지 전송
        message = f"{i['keyword']}\n\n{i['title']}\n{i['link']}"
        sendMessage(my_token, chat_id, message)

if __name__ == "__main__":
    while 1:
        #3초에 한번씩 전송
        bot()
        time.sleep(3)


        #memory_usage_dict = dict(psutil.virtual_memory()._asdict())
        #memory_usage_percent = memory_usage_dict['percent']
        #print(f"memory_usage_percent: {memory_usage_percent}%")
        # current process RAM usage
        #pid = os.getpid()
        #current_process = psutil.Process(pid)
        #current_process_memory_usage_as_KB = current_process.memory_info()[0] / 2.**20
        #print(f"Current memory KB   : {current_process_memory_usage_as_KB: 9.3f} KB")
