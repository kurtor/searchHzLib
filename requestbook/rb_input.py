import time

def getListFromTxt(path):
    book_name_list = []
    with open(path,'r', encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            if (len(line.strip()) != 0 ):
                name_author = line.strip().split('《')[1].split("》")
                if(len(name_author) == 2):
                    book_name_list.append([name_author[0].strip(),name_author[1].strip()])
                elif(len(name_author) == 1):
                    book_name_list.append([name_author[0].strip(),""])
    return book_name_list

def getTimestamp():
    now = int(round(time.time()*1000))
    timestamp = time.strftime('%Y%m%d_%H%M%S',time.localtime(now/1000))
    return timestamp

def getRealurl(book_title,book_author):
    #按书名单独检索
    web_domain = 'http://my1.hzlib.net'
    web_location = '/opac/search?'
    searchWay = 'searchWay=title200a'
    q = '&q='
    searchSource = '&searchSource=reader&scWay=dim&marcformat='
    sortWay = '&sortWay=score'
    sortOrder = '&sortOrder=desc'
    publicTime = '&startPubdate=&endPubdate=&rows=10'

    #按书名+作者检索
    mul_web_domain = 'http://my1.hzlib.net'
    mul_web_location = '/opac/search?'
    mul_searchWay0 = 'searchWay=title'
    mul_q0 = '&q0='
    mul_logical0 = '&logical0=AND'
    mul_searchWay1 = '&searchWay1=author'
    mul_q1 = '&q1='
    mul_logical1 = '&logical1=AND'
    mul_searchWay2 = '&searchWay2='
    mul_q2 = '&q2='
    mul_searchSource = '&searchSource=reader&marcformat='
    mul_sortWay = '&sortWay=score'
    mul_sortOrder = '&sortOrder=desc'
    mul_publicTime = '&startPubdate=&endPubdate=&rows=10'

    real_url= ''
        
    if(book_author != ''):
        #按书名+作者检索
        real_url =  mul_web_domain + mul_web_location + \
                    mul_searchWay0 + mul_q0 + book_title  + mul_logical0 + \
                    mul_searchWay1 + mul_q1 + book_author + mul_logical1 + \
                    mul_searchWay2 + mul_q2 + mul_searchSource + mul_sortWay + mul_sortOrder + mul_publicTime
    else:
        #按书名单独检索
        real_url = web_domain + web_location + searchWay + q + book_title + searchSource + \
            sortWay + sortOrder + publicTime

    return real_url