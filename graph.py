import re
import copy
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import date,timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc
import matplotlib.ticker as ticker


def move_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

def pgraph(event):
#    str1 = '삼성전자'
    str2 = event.encode('euc-kr')
    print(str2)
    print(str2.decode('euc-kr'))

    str3 = str(str2)[2:-1]
    str3 = re.sub('\\\\x','%',str3)
    str3 = str3.upper()
    print(str3)
    #print(re.sub('\\\\x','%',str3))

    #url = 'https://finance.naver.com/search/searchList.nhn?query='
    #url = 'https://finance.naver.com/search/searchList.nhn?query='+str3
    soup = move_url('https://finance.naver.com/search/searchList.nhn?query='+str3)
    #print(url)

    p = soup.find(class_='section_search')

    if p != None:
        p = p.find_all(class_='tit')
        for i in p:
            print(i)
            #print(i.get_text().split()[0])
            if i.get_text().split()[0] == event:
                print('i=====')
                print(i)
                print('a=====')
                print(i.find('a').attrs['href'])
                # r = re.compile('/.*"')
                # match = r.search(str(i.find('a')))
                # print(match.group(0)[0:-1])
                soup = move_url('https://finance.naver.com'+i.find('a').attrs['href'])

    p = soup.find(class_='content_wrap').find(class_='tabs_submenu tab_total_submenu').find_all('a')

    for i in p:
        if i.get_text() == '시세':
            print(i)
            r = re.compile('href=.*\s')
            match = r.search(str(i))
            #print(match.group(0).split('href="')[1][0:-2])
            soup = move_url('https://finance.naver.com'+match.group(0).split('href="')[1][0:-2])

    p = soup.find(class_='content_wrap').find(class_='section inner_sub').find_all('iframe')

    for i in p:
        print(i.attrs['title'])
        r = re.compile('title\S*\s?\S*')
        match = r.search(str(i))
        #print(match.group(0).split('title="')[1][0:-1])
        if match.group(0).split('title="')[1][0:-1] == '일별 시세':
            r = re.compile('src=\S*')
            match = r.search(str(i))
            #print(match.group(0).split('src="')[1][0:-1])
            print('https://finance.naver.com'+match.group(0).split('src="')[1][0:-1])
            driver = webdriver.Chrome('./chromedriver')
            driver.get('https://finance.naver.com'+match.group(0).split('src="')[1][0:-1])
            time.sleep(0.1)
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')

    url = driver.current_url
    a = driver.find_elements_by_tag_name('a')
    # print(len(a))
    #
    # for i in range(len(a)):
    #     print(a[i].get_attribute('href'))

    last_page = int(a[-1].get_attribute('href').split('page=')[1])

    #p = soup.find_all(class_='tah p10 gray03')

    # for i in p:
    #    print(i.get_text())

    #now_date = int(p[0].get_text().replace('.','')) - 30
    #print(now_date)
    #print(type(now_date))

    #date_time = date_time - timedelta(days=10)

    #last_time = date.today() - timedelta(days=20)
    last_time = date.today().replace(year=date.today().year-3)
    #print(date_time)
    #print(last_time)

    data_list = []

#page 이동 및 데이터 가지고 오기
    for i in range(2,1+last_page):
        #print(p)
        #p = soup.find_all(class_='tah p10 gray03')
        p = soup.find(class_='type2').find_all('td')
        mid_list = []
        count = 0
        for j in p:
            if len(j.get_text().split()) > 0:
                count += 1
                if count == 1:
                    if (date.fromisoformat(j.get_text().replace('.','-')) - last_time).days < 0:
                        i = last_page + 1
                        break
                mid_list.append(j.get_text().replace('\n', '').replace('\t', ''))
                if count == 3:
                    s = '하락'
                    if str(j).find('하락') == -1:
                        s = '상승'
                    mid_list[2] = mid_list[2] + s
                if count == 7:
                    count = 0
                    #print(mid_list)
                    data_list.append(copy.deepcopy(mid_list))
                    mid_list.clear()
            # print(date.fromisoformat(j.get_text().replace('.','-')))
            # print(last_time)
            # print((date.fromisoformat(j.get_text().replace('.','-'))-last_time).days)
            # print()
            #print(i.get_text())
        #print('--------')
        # p = soup.find(class_='Nnavi').find(class_='on')
        # a = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[%d]'%(int(p.get_text().split()[0])+1))
        # a.click()
        if i == last_page + 1:
            break
        driver.get(url+'&page='+str(i))
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source,'html.parser')


    #print('--------결과발표--------')
    #for i in range(len(data_list)):
    #    print(data_list[i])
    #    print()

# driver url test
    # print(driver.current_url)
    #
    # p = soup.find(class_='Nnavi').find(class_='on')
    #
    # print('/html/body/table[2]/tbody/tr/td[%d]' % (int(p.get_text().split()[0]) + 1))
    # driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[%d]'%(int(p.get_text().split()[0])+1)).click()
    # time.sleep(2)
#     print(driver.current_url)
#     #driver.get('https://finance.naver.com/item/sise_day.nhn?code=005930&page=3')
#     #driver.get('https://finance.naver.com/item/sise_day.nhn?code=005930&page=4')
#     #driver.get('https://finance.naver.com/item/sise_day.nhn?code=005930&page=5')
#     html = driver.page_source
#     soup = BeautifulSoup(html,'html.parser')
#
#     time.sleep(2)
# #    / html / body / table[2] / tbody / tr / td[3]
#
#     #print(soup.find_all('a'))
#     p = soup.find(class_='Nnavi').find(class_='on')
#     print('/html/body/table[2]/tbody/tr/td[%d]' % (int(p.get_text().split()[0]) + 1))
#     a = driver.find_elements_by_tag_name('a')
#     for i in range(len(a)):
#         if a[i].get_attribute('href'):
#             print(a[i].get_attribute('href'))

    #a.click()
    #driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[%d]' % (int(p.get_text().split()[0]) + 1)).click()
    #time.sleep(2)
    #print(a)

    #print(driver.current_url)




 #   / html / body / table[2] / tbody / tr / td[11]
    driver.close()

#그래프 그리는 부분
    data_list.sort(key=lambda x: x[0])
    columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'avg_5d', 'avg_20d', 'avg_60d', 'avg_120d', 'avg_240d']
    index = []
    data = []

    df = DataFrame(data=data, index=pd.to_datetime(index), columns=columns)
    df = df.astype('float')

    for i in range(len(data_list)):
        data = data_list[i]

        for j in range(len(data)):
            data[j] = data[j].replace(',', '')

        df.loc[pd.to_datetime(data[0])] = [int(data[3]), int(data[4]), int(data[5]), int(data[1]), int(data[6]), 0, 0,
                                           0, 0, 0]
    df['avg_5d'] = df['Close'].rolling(5).mean()
    df['avg_20d'] = df['Close'].rolling(20).mean()
    df['avg_60d'] = df['Close'].rolling(60).mean()
    df['avg_120d'] = df['Close'].rolling(120).mean()
    df['avg_240d'] = df['Close'].rolling(240).mean()


    pltfig = plt.figure(figsize=(20, 10))
    ax = pltfig.add_subplot(111)
    index = df.index.astype('str')  # 캔들스틱 x축이 str로 들어감

    # 이동평균선 그리기
    ax.plot(index, df['avg_5d'], label='MA5', linewidth=0.7)
    ax.plot(index, df['avg_20d'], label='MA20', linewidth=0.7)
    ax.plot(index, df['avg_60d'], label='MA60', linewidth=0.7)
    ax.plot(index, df['avg_120d'], label='MA120', linewidth=0.7)
    ax.plot(index, df['avg_240d'], label='MA240', linewidth=0.7)

    # X축 티커 숫자 20개로 제한
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

    # 그래프 title과 축 이름 지정
    ax.set_title('KOSPI INDEX', fontsize=22)
    ax.set_xlabel('Date')

    # 캔들차트 그리기
    candlestick2_ohlc(ax, df['Open'], df['High'],
                      df['Low'], df['Close'],
                      width=0.5, colorup='r', colordown='b')
    ax.legend()
    plt.grid()
#    plt.show()


    trace1 = go.Candlestick(
        x=df.index,
        open=df.Open,
        high=df.High,
        low=df.Low,
        close=df.Close,
        increasing_line_color='red',
        decreasing_line_color='blue',
        name='캔들스틱'
    )

    trace2 = {'x': df.index,
              'y': df.avg_5d,
              'type': 'scatter',
              'mode': 'lines',
              'line': {'width': 4, 'color': 'chocolate'},
              'name': '5일 이동평균선'}

    trace3 = {'x': df.index,
              'y': df.avg_20d,
              'type': 'scatter',
              'mode': 'lines',
              'line': {'width': 4, 'color': 'orange'},
              'name': '20일 이동평균선'}

    trace4 = {'x': df.index,
              'y': df.avg_60d,
              'type': 'scatter',
              'mode': 'lines',
              'line': {'width': 4, 'color': 'darkred'},
              'name': '60일 이동평균선'}

    trace5 = {'x': df.index,
              'y': df.avg_120d,
              'type': 'scatter',
              'mode': 'lines',
              'line': {'width': 4, 'color': 'forestgreen'},
              'name': '120일 이동평균선'}

    trace6 = {'x': df.index,
              'y': df.avg_240d,
              'type': 'scatter',
              'mode': 'lines',
              'line': {'width': 4, 'color': 'indigo'},
              'name': '240일 이동평균선'}

    trace7 = {'x': df.index,
              'y': df.Volume / df.Volume.max() * (0.2 * df.Close.min()) + (0.7 * df.Close.min()),
              'type': 'scatter',
              'mode': 'lines',
              'line': {'width': 4, 'color': 'navy'},
              'name': '거래량'}

    data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7]
    fig = go.Figure(data=data)
    fig.update_layout(xaxis_rangeslider_visible=False)

    #fig.show()


    return fig,pltfig,df

    '''
    data2=data[-2:]
    print(data2)
    print('---------')
    print(data2.dtypes)
    print('---------')
    print(data2.T)
    print('---------')
    print(data2.values)
    print('---------')
    print(data2.index)
    print('---------')
    print(data2.columns)
    print('---------')
    print(data2.info())
    
    mpf.plot(data[-10:],
            type = 'candle',
            figratio = (12,4),
            style = s)
    mc = mpf.make_marketcolors(up = 'tab:red' , down = 'tab:blue')
    s = mpf.make_mpf_style(marketcolors = mc)
    
    columns = ['Open','High','Low','Close','Volume','Dividends','Stock Splits']
    index = ['2021.05.12','2021-05-13']
    data = [[80800.0,81200.0,79800.0,80000.0,35812268,0.0,0.0],
        [78900.0,79600.0,78400.0,78500.0,30973726,0.0,0.0]]
    
    df = DataFrame(data=data, index=pd.to_datetime(index), columns=columns)
    
    print(df)
    print('----------')
    print(df.info())
    mpf.plot(df,
            type = 'candle',
            figratio = (12,4),
            style = s)
    
    data_list = [['2021.05.13', '78,500', '1,500상승', '78,900', '79,600', '78,400', '31,020,142'],
    ['2021.05.12', '80,000', '1,200상승', '80,800', '81,200', '79,800', '35,812,268'],
    ['2021.05.11', '81,200', '2,000상승', '82,500', '82,600', '81,100', '28,996,680'],
    ['2021.05.10', '83,200', '1,300상승', '82,300', '83,500', '81,800', '19,385,027'],
    ['2021.05.07', '81,900', '400상승', '81,800', '82,100', '81,500', '14,154,882'],
    ['2021.05.06', '82,300', '300상승', '81,700', '82,300', '81,700', '17,047,511'],
    ['2021.05.04', '82,600', '900상승', '81,900', '82,600', '81,800', '12,532,550'],
    ['2021.05.03', '81,700', '200상승', '81,000', '82,400', '81,000', '15,710,336'],
    ['2021.04.30', '81,500', '200상승', '81,900', '82,100', '81,500', '18,673,197'],
    ['2021.04.29', '81,700', '400상승', '82,400', '82,500', '81,500', '20,000,973'],
    ['2021.04.28', '82,100', '800상승', '83,200', '83,200', '82,100', '15,596,759'],
    ['2021.04.27', '82,900', '600상승', '83,200', '83,300', '82,500', '12,941,533'],
    ['2021.04.26', '83,500', '700상승', '82,900', '83,500', '82,600', '15,489,938']]
    
    data_list.sort(key = lambda x:x[0])
        
    mc = mpf.make_marketcolors(up = 'tab:red' , down = 'tab:blue')
    s = mpf.make_mpf_style(marketcolors = mc)
    
    columns = ['Open','High','Low','Close','Volume','Dividends','Stock Splits']
    index = []
    data = []
    
    df = DataFrame(data = data, index = pd.to_datetime(index), columns = columns)
    df = df.astype('int')
    
    #print(df)
    #print(df.info())
    
    for i in range(len(data_list)) :
        data = data_list[i]
        
        for j in range(len(data)):
            data[j] = data[j].replace(',','')
        
        df.loc[pd.to_datetime(data[0])] = [int(data[3]),int(data[4]),int(data[5]),int(data[1]),int(data[6]),0,0]

    # data = data_list[0]
    
    # for i in range(len(data)) :
    #     data[i] = data[i].replace(',','')
    
    # df.loc[pd.to_datetime(data[0])] = [int(data[3]),int(data[4]),int(data[5]),int(data[1]),int(data[6]),0,0]
    
    # print(df)
    print(df.T)
    
    mpf.plot(df,
            type = 'candle',
            figratio = (12,4),
            volume = True,
            show_nontrading = True,
            style = s)


    '''