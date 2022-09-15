import telegram
import logging

def sendMessage(token, chat_id, message):
    '''
    텔레그램 메세지 전송
    '''
    try:
        bot = telegram.Bot(token)
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error("sendMessage Error", e, [token, chat_id, message])