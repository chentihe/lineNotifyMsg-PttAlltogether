import requests
from bs4 import BeautifulSoup
import time
from random import randrange

token = 'your_token'
def lineNotifyMsg(token, msg):
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': msg}
    r = requests.post('https://notify-api.line.me/api/notify',
                    headers=headers, params=payload)
    return r.status_code

def scraper():
    rs = requests.session()
    url = 'https://www.ptt.cc/bbs/Alltogether/index.html'

    local_time = time.localtime()
    timeString = time.strftime('%m/%d', local_time) #顯示 月/日
    if timeString[0] == '0':
        timeString = timeString[1:] # 讓 月/日格式和ptt一樣

    for _ in range(5): # 搜尋歐兔板前五頁
        response = rs.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        previousPage = soup.select('div.btn-group.btn-group-paging a')[1]['href']
        url = 'https://www.ptt.cc' + previousPage

        for target in soup.select('.r-ent'):
            if ('徵男' in target.select(' .title')[0].text) and (target.select('.date')[0].text.strip() == timeString):
                # 徵男文 ＆ 當天日期
                title = target.find(class_='title').text.strip()
                link = 'https://www.ptt.cc' + target.find('a').get('href')
                msg = title + '\n' + link
                lineNotifyMsg(token, msg)

        sleep_time = randrange(1, 60)
        time.sleep(sleep_time)

scraper()