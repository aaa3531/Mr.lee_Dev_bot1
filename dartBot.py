from Utils.telegramUtils import sendMessage
import time
import feedparser
import Utils.hashUtil as hashUtil
import json

my_token = '1570819804:AAGeHTU4gyirsIBVbTUAAOFM5Ebh0BPrMss' #@telegram_bot
chat_id = "-1001249399947"

def dart():
    with open("/home/ubuntu/telegram_bot2/dart.json", "r", encoding="UTF-8") as f:
        dart_json = json.load(f)

    dart_url = "http://dart.fss.or.kr/api/todayRSS.xml"
    d = feedparser.parse(dart_url)


    for i in d['entries']:
        if hashUtil.get_hash_value(i['title'], 16, 'number') == dart_json['last_title']:
            break
        #for j in dart_json['keyword']:
            #if j in i['title']:
        message = f"{i['title']}\n{i['link']}\n{i['author']}"
        sendMessage(my_token, chat_id, message)
            #break
            #print(message)
    dart_json['last_title'] = hashUtil.get_hash_value(d['entries'][0]['title'], 16, 'number')
    with open('/home/ubuntu/telegram_bot2/dart.json', 'w', encoding='UTF-8') as f:
        json.dump(dart_json, f, indent="\t")
if __name__ == '__main__':
    time.sleep(5)
    dart()
