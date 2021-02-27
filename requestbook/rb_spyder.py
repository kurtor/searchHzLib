from rb_input import getListFromTxt
from rb_input import getTimestamp
from rb_get import getSearchResult

from requests_html import HTMLSession
import pandas as pd
import os



if __name__ == "__main__":
    
    useProxy = True #默认开启代理，不开启则置为False
    endPage = 4 #最多搜索到第4页为止，即搜索前3页
    
    session = HTMLSession()

    # title_word_chinese_list = getListFromTxt('./douban.txt')
    output_path = './bookList_' + getTimestamp() + '.xlsx'
    if not os.path.exists(output_path):
        new_pf = pd.DataFrame()
        new_pf.to_excel(output_path,sheet_name='Data1')

    title_word_chinese_list = ['地心游记']

    web_domain = 'http://my1.hzlib.net'
    web_location = '/opac/search?'
    searchWay = 'searchWay=title200a'
    searchSource = '&searchSource=reader&scWay=dim&marcformat='
    sortWay = '&sortWay=score'
    sortOrder = '&sortOrder=desc'
    publicTime = '&startPubdate=&endPubdate=&rows=10'
    libCode_hangzhou = '&logical0=AND&curlibcode=0000'

    for title_word_chinese in title_word_chinese_list:
        q_title = '&q=' + title_word_chinese
        real_url = web_domain + web_location + searchWay + q_title + searchSource + \
            sortWay + sortOrder + publicTime + libCode_hangzhou

        temp_data = pd.DataFrame()
        data_i = getSearchResult(temp_data, real_url, session, web_domain, useProxy, endPage)
        if(data_i.empty):
            print("no result for" + title_word_chinese)
        else:
            df_old = pd.DataFrame(pd.read_excel(output_path,sheet_name='Data1'))
            df_rows = df_old.shape[0] #获取原数据的行数
            data_i.to_excel(output_path, sheet_name='Data1',startcol=df_rows+1, index=False,header=False)
