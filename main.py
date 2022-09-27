import re
import copy
import requests
import time
from bs4 import BeautifulSoup
import graph
import LSTM
from datetime import date,timedelta
from selenium import webdriver
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



def btn2press(fig):
    newWindow = Toplevel(window)
    newWindow.geometry("600x400")
    newWindow.resizable(False, False)
    # labelExample = Label(newWindow, text = "New Window")
    # buttonExample = Button(newWindow, text = "New Window button")
    #
    # labelExample.pack()
    # buttonExample.pack()
    canvas = FigureCanvasTkAgg(fig, master=newWindow)
    canvas.draw()
    canvas.get_tk_widget().pack()

def btn3press(fig):
    fig.show()

def btn4press(last_price,price,fig,score):
    newWindow2 = Toplevel(window)
    newWindow2.geometry("800x600")
    newWindow2.resizable(False, False)
    # labelExample = Label(newWindow, text = "New Window")
    # buttonExample = Button(newWindow, text = "New Window button")
    #
    # labelExample.pack()
    # buttonExample.pack()

    label1 = Label(newWindow2, text="오늘자 종가 : " + str(last_price) +' 내일 종가 예측 : ' +str(price))
    label2 = Label(newWindow2, text="정확도 : " + str(score) +' 다음은 주식 흐름도입니다.')

    label1.pack()
    label2.pack()

    canvas = FigureCanvasTkAgg(fig, master=newWindow2)
    canvas.draw()
    canvas.get_tk_widget().pack()


def btnpress():                   # 함수 btnpress() 정의
    #btn.config(text = ent.get())
    print(ent.get())
    fig, pltfig,df = graph.pgraph(ent.get())
    last_price, price, fig2, score = LSTM.lstm_model(df)

    # canvas = FigureCanvasTkAgg(fig, master=window)
    # canvas.draw()
    # canvas.get_tk_widget().pack()

    btn2 = Button(window)
    btn2.config(text='그래프보기')
    btn2.config(width=10)
    btn2.config(command=lambda: btn2press(pltfig))
    btn2.pack()

    btn3 = Button(window)
    btn3.config(text='확대보기')
    btn3.config(width=10)
    btn3.config(command=lambda: btn3press(fig))
    btn3.pack()

    btn4 = Button(window)
    btn4.config(text='주식예측하기')
    btn4.config(width=10)
    btn4.config(command=lambda: btn4press(last_price, price,fig2,score))
    btn4.pack()

#    price, fig2, score = LSTM.lstm_model(df)


if __name__ == '__main__':
    #driver = webdriver.Chrome('./chromedriver')
    #driver.get('https://google.com')
    #graph.pgraph("삼성전자")

    window = Tk()  # 창을 생성
    window.geometry("300x200")  # 창 크기설정
    window.title("주식정보")  # 창 제목설정
    window.option_add("*Font", "맑은고딕 25")  # 폰트설정
    window.resizable(False, False)  # x, y 창 크기 변경 불가

    ent = Entry(window)  # root라는 창에 입력창 생성
    ent.pack()  # 입력창 배치

    btn = Button(window)  # root라는 창에 버튼 생성
    btn.config(text="검색")  # 버튼 내용
    btn.config(width=10)  # 버튼 크기
    btn.config(command=btnpress)  # 버튼 기능 (btnpree() 함수 호출)
    btn.pack()  # 버튼 배치

    window.mainloop()

    #print(type(date.today()))
#page 데이터 가지고 오기
    '''
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://finance.naver.com/item/sise_day.nhn?code=005930')
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(2)

    p = soup.find(class_='type2').find_all('td')
    print(len(p))
    data_list = []
    mid_list = []
    count = 0
    for i in p:
        #print(i)
        print(i.get_text())
        if len(i.get_text().split()) > 0:
            #s = i.get_text()
            #print(s.replace('\n','').replace('\t',''))
            count += 1
            mid_list.append(i.get_text().replace('\n', '').replace('\t', ''))

            if count == 3:
                s = '하락'
                if str(i).find('하락') == -1:
                    s = '상승'
                mid_list[2] = mid_list[2] + s
        if count == 7:
            count = 0
            print(mid_list)
            data_list.append(copy.deepcopy(mid_list))
            mid_list.clear()

    print(len(data_list))
    print('--------결과발표--------')
    for i in range(len(data_list)):
        print(data_list[i])
        print()

    driver.close()

    '''
    '''
#시간함수 활용
    str1 = '2021.04.09'
    str2 = str1.replace('.','-')
    date_time = date.fromisoformat(str2)
    print(date_time)
    date_time = date_time - timedelta(days=10)
    print(date_time.replace(year=date_time.year-3))
    date_time1 = date_time.replace(year=date_time.year-3)
    str1 = '2018.03.29'
    str2 = str1.replace('.','-')
    date_time2 = date.fromisoformat(str2)
    print(date_time1,' ',date_time2)
    print(date_time2-date_time1)
    a = date_time2-date_time1
    print(a)
    print(type(a.days))
    if (date_time2-date_time1).days >= 0:
        print('yes')
    else:
        print('no')
    #print(date_time)

    #date_time = datetime.datetime(int(str2[0]),int(str2[1]),int(str2[2]))
    #print(date_time)

    '''
    '''
    url = "https://finance.naver.com/sise/sise_market_sum.nhn"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")

    #p = soup.find("thead").find_all("th")
    #print(type(p))
    p = str(soup.find("thead").find_all("th"))
    head=[]
    #print(type(s))
    #s.append(str(p[0]))
    #print(s)
    #print(type(s[0]))
    #print(type(p))
    #print(len(p))

    r = re.compile('>.*<')
    #s= str(p[0])
    #print(type(s))
    #print(s)
    #match = r.search(s[0])
    #a = match.group(0)
    #print(len(a))

    print(type(p))
    print(p.split(','))
    p = p.split(',')
    #for i in range(0,len(p)-1):
    #    match = r.search(p)
    print(len(p))
    for i in range(0,len(p)):
        #print(p[i])
        match = r.search(p[i])
        print(match)
        #print(type(match.span()))
        #t=()
        #t=match.span()
        #print(match.group(0))
        #print(match.group(0)[1:len(match.group(0))-1])
        head.append(match.group(0)[1:len(match.group(0))-1])
    print(head)
    result = []
    a = []
    count = 0

    result = []

    #print(result)
    #print(type(result[0][0]))

    q = soup.find(class_='type_2').find_all("td")
    #print(type(a))
    print(len(head))
    print(len(q))

    for i in range(0,len(q)):
        #print('q찍은거야 '+str(q[i]))
        #print(q[i].get_text().split())#코딩 참고
        #print(q[i])
        #print(type(q[i].get_text().split()))
        s = q[i].get_text()
        s = s.replace('\n','')
        s = s.replace('\t','')
        if len(s)>0:
            #print('s를 찍습니다 ',s)
            a.append(s)
            count += 1
        elif str(q[i]).find('a href') != -1:
            #print(q[i])
            #print(str(q[i]).find('a href'))
            r = re.compile('<a href=.*">')
            m = r.search(str(q[i]))
            #print(m.group(0))
            a.append(m.group(0))
            count += 1

        if count == len(head):
            #print('count = ',count)
            #print(a)
            result.append(copy.deepcopy(a))
            a.clear()
            count = 0
    '''

    '''
    if soup.find(class_='Nnavi').find(class_='pgRR') != None:
        z = soup.find(class_='Nnavi').find(class_='on').find('a')
        print(z)
        r = re.compile('/.*"')
        match = r.search(str(z))
        #print(match.group(0).split('page='))
        next_url = match.group(0).split('amp;')[0] + 'page=' + str(int(z.get_text())+1)
        print(next_url)
        print(url.split('.com'))
        url = url.split('.com')[0] + '.com' + next_url
        print(url)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    q = soup.find(class_='type_2').find_all("td")
    print(q)
    '''
    '''
    count = 1
    while soup.find(class_='Nnavi').find(class_='pgRR') != None:
        z = soup.find(class_='Nnavi').find(class_='on').find('a')
        r = re.compile('/.*"')
        match = r.search(str(z))
        next_url = match.group(0).split('amp;')[0] + 'page=' + str(int(z.get_text()) + 1)
        url = url.split('.com')[0] + '.com' + next_url
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        count += 1
        if count == 100:
            break

    print(count)
    '''
    #print(result)
    #print(q[2])
    #print(a)