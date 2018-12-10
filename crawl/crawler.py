#-*- coding:utf-8 -*-
import requests
import datetime
from bs4 import BeautifulSoup

news_id = {'hani':'17', 'omn':'4', 'chosun': '200', 'joongang': '8'}
news_tend = {'hani':'0', 'omn':'0', 'kyounghyang':'0', 'dongah':'1', 'chosun': '1', 'joongang': '1'} # 0 : 진보, 1 : 보수
dt = datetime.datetime.now()
delta = datetime.timedelta(days=1)

def getTitleList(news_id, date):

    titles = []
    page = 1
    while True:
        req = requests.get('http://media.daum.net/cp/' + news_id + '?page='
                            + str(page) + '&regDate=' + date + '&cateId=1002')

        soup = BeautifulSoup(req.content, 'html.parser', from_encoding='utf-8')

        raw_titles = soup.find_all("strong", {"class": "tit_thumb"})
        raw_titles = raw_titles[:-2]
        if len(raw_titles) is 0:
            break

        for raw_title in raw_titles:
            title = str(raw_title).split('">')[2].split('</a>')[0]
            titles.append(title)

        page += 1

    return titles

#def makeTestSet(news_id, date):

f = open('data.txt', 'w')
id = 111111
f.write('id\tdocument\tlabel\n')
number = 200

# 신문사별로 과거 3000일까지 데이터 수집하여 파일로 저장

def makefile(current_day):
    news_list = {'dongah': '190'}
    parsing(current_day,'test_dongah', True, news_list)
    news_list = {'kyounghyang': '11'}
    parsing(current_day,'test_kyounghyang', True, news_list)
    news_list = {'chosun': '200', 'joongang': '8', 'dongah': '190'}
    parsing(current_day,'test_chojoongdong', True, news_list)
    news_list = {'hani': '17', 'omn': '4','kyounghyang': '11'}
    parsing(current_day,'test_hankyoungoh', True, news_list)
    news_list = {'chosun': '200'}
    parsing(current_day,'test_cho', True, news_list)
    news_list = {'joongang': '8'}
    parsing(current_day,'test_joong', True, news_list)
    news_list = {'hani': '17'}
    parsing(current_day,'test_han', True, news_list)
    news_list = {'omn': '4'}
    parsing(current_day,'test_oh', True, news_list)
    news_list = {'hani':'17', 'omn':'4', 'chosun': '200', 'joongang': '8','dongah': '190','kyounghyang': '11'}
    parsing(current_day,'test_set', True, news_list)
    
    #news_list = {'hani':'17', 'omn':'4', 'chosun': '200', 'joongang': '8'}
    #parsing(current_day,'train', False, news_list)

#테스트용이면 news_tend를 0으로 세팅, 조+중, 조, 중, 한+경, 한, 경 총 6개 파일
#train용이면 news_tend를 보수면 1 진보면 0 조+중+동+
 #booltie -> 조중동, 한경오를 묶을 것인지 booltest -> 테스트 용인지
def parsing(day, file_name, booltest, news_list):
    id = 111111
    number = 7
    weekago = day - datetime.timedelta(days=7)
    if(booltest==False):
        day = day - datetime.timedelta(days=7)
        weekago = day - datetime.timedelta(days=200)
        number=200
    filename = file_name+"_"+str(weekago.strftime('%Y%m%d'))+"-"+str(day.strftime('%Y%m%d'))
    print(filename)
    f = open(filename,'w')
    #f.write('date : ' + weekago.strftime('%Y%m%d')+"-"+day.strftime('%Y%m%d')+"\n")
    f.write('id\tdocument\tlabel\n')
    nowdate = weekago
    for j in range(0,number):
        nowdate = nowdate + datetime.timedelta(days=1)
        for news in news_list:
            t = getTitleList(news_list[news], nowdate.strftime('%Y%m%d'))
            #print(nowdate.strftime('%Y%m%d'))
            for title in t:
                if(booltest):
                    f.write(str(id) + '\t' + title + '\t' + str('0') + '\n')
                else:
                    f.write(str(id) + '\t' + title + '\t' + news_tend[news] + '\n')
                id += 1
    f2 = open('nameinfo.txt','a')
    f2.write(filename+",")
    f.close()
    f2.close()

makefile(datetime.datetime.now()- datetime.timedelta(days=21))

