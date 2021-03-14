from rb_input import getListFromTxt, getTimestamp, getRealurl
from rb_get import getSearchResult
from requests_html import HTMLSession
from pypinyin import lazy_pinyin
import pandas as pd
import os
import json

if __name__ == "__main__":
    
    useProxy = True #默认开启代理，不开启则置为False
    endPage = 3 #最多搜索到第4页为止，即搜索前2页
    web_domain = 'http://my1.hzlib.net'
    input_path = './douban.txt'
    output_path = './bookList_' + getTimestamp() + '.json'
    
    session = HTMLSession()
    title_author_list = getListFromTxt(input_path)
    all_obj_array = []
    
    for item in title_author_list:
        title = item[0]
        author = item[1]
        print("downloading " + title + "  "  + author)
        obj_array = []
        which_book_count = 0 
        max_try = 25
        url = getRealurl(title, author)   
         
        obj_array = getSearchResult(obj_array, url, title, author, which_book_count, session, web_domain, useProxy, endPage, max_try)
        book = {
            "title": item[0],
            "author": item[1],
            "main_img": "mainImg/"+'_'.join(lazy_pinyin(title)) + ".jpg",
            "content":"简介",
            "classification": "分类",
            "borrow_info": obj_array
        }
        all_obj_array.append(book)

        json_file = open(output_path,'w',encoding='utf-8')
        print(json.dumps(all_obj_array,ensure_ascii=False),file = json_file)
        json_file.close()