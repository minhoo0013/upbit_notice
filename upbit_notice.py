# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:23:57 2022

@author: 82109
"""

import time
import pyupbit
import requests
import json
import telegram

CHAT_ID = '5174159613'
TOKEN = '5967076689:AAFpeHRkgV--Cx1N3KgIEUXcN_NLTFSIf5w'
UPBIT_API = 'XTosaR8B3j8JizUruwQiIisBUjkWEGdcOZF'
UPBIT_SECRET = 'wGmzzUjefNqexGTxYrfBjbTK7KbxbyaOswPqu'
    
def upbit_notice_crolling():
    url_noti = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=2000&thread_name=general'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    html_upb = requests.get(url_noti, headers=headers)
    notice_list = json.loads(html_upb.text)['data']['list']
    return notice_list

def upbit_notice_check(coin, last_id):
    try:
        notice_list = upbit_notice_crolling()
        for course in notice_list:
            if course['id'] <= last_id:
                break    
            else:
                if coin in course['title']:
                    return 'TRUE'
                else:
                    return course['title']
        return 'FALSE'
    
    except Exception as e:
        print(e)
        return e

if __name__ == "__main__":
    LAST_ID = upbit_notice_crolling()[0]['id']
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text="start")
    
    result = 'FALSE'
    while result != 'TRUE':
        result = upbit_notice_check('GMT',LAST_ID)
        if result == 'TRUE':
            print('order')
            bot.sendMessage(chat_id=CHAT_ID, text='ORDER GMT')
        elif result == 'FALSE':
            print('running..')
        else:
            bot.sendMessage(chat_id=CHAT_ID, text=result)
        time.sleep(1.5)
        
    chat_text = "end"
    bot.sendMessage(chat_id=CHAT_ID, text=chat_text)

upbit = pyupbit.Upbit(access=UPBIT_API, secret=UPBIT_SECRET)
#ret = upbit.buy_market_order(ticker='KRW-GMT', price=6000)
print(ret)

