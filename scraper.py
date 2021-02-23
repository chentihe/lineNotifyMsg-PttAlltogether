import requests
from bs4 import BeautifulSoup
import time

rs = requests.session()
response = rs.get('https://www.ptt.cc/bbs/Alltogether/index.html')
soup = BeautifulSoup(response.text, 'html.parser')
local_time = time.localtime()
timeString = time.strftime('%m/%d', local_time) #顯示 月/日

def scraper(token):
    if timeString[0] == '0':
        timeString = timeString[1:] # 讓 月/日格式和ptt一樣
    for entry in soup.select(' .r-ent'):
        if ('徵男' in entry.select(' .title')[0].text) and (entry.select('.date')[0].text.strip() == timeString):
            headers = {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            params = {'message': entry.select(' .title')[0].text + '\n' +
            'https://www.ptt.cc' + entry.find('a').get('href')}

            r = requests.post('https://notify-api.line.me/api/notify',
                                headers=headers, params=params)
            
            return r.status_code
        time.sleep(10)

if __name__ == '__main__':
    token = 'D7fZ04VxabHBFobJN7IxDN9BwNOc2HkboyumpcFMGDm'

    scraper(token)