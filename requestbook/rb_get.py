# -*- coding: utf-8 -*-
from rb_proxy import getHtml,getContent
from pypinyin import lazy_pinyin
from urllib import parse
import os

#获取表格中十本书的编号，用于组成url单独访问每一本书的详情页
def getBooksNoList(allTableSoup):
    book_no_list = []
    foundAllTr = allTableSoup.find("tr")
    for trSoup in foundAllTr:
        foundAllTd = trSoup.find("td")
        td_input = foundAllTd[0].find("input", first=True)
        book_no = td_input.attrs["value"]
        if(book_no):
            book_no_list.append(book_no)
            print("id_value:" + book_no)
    return book_no_list

#按data-sort的值，获取里面的值并判断是否为空
def getDataSortText(allTableSoup,sort_sentence1,sort_sentence2 = "td[class='rightTD']"):
    date_sort_text = ""
    find_text = allTableSoup.find(sort_sentence1,first=True)
    if(type(find_text) != type(None)):
        find_text = find_text.find(sort_sentence2, first=True)
        if(type(find_text) != type(None)):
            date_sort_text = find_text.text
    return date_sort_text

#下载id为bookcover_img的标签下的图片
def downloadImage(html, origin_title, which_book_count, session,useProxy):
    try:
        version_img=""
        file_path = "versionImg/"
        if not os.path.exists("./" + file_path):
            os.makedirs("./" + file_path)
        coverImgSoup = html.find("#bookcover_img", first=True)
        if(type(coverImgSoup) != type(None)):
            coverImgAttrs = coverImgSoup.attrs
            if 'src' in coverImgAttrs.keys():
                img_src = coverImgAttrs['src']
                middle_str = '_'
                img_name = file_path + middle_str.join(lazy_pinyin(origin_title))+ middle_str + str(which_book_count)
                print("download_img_src" + img_src)
                if(".jpg" in img_src):
                    version_img = img_name + ".jpg"            
                elif(".jpeg" in img_src):
                    version_img = img_name + ".jpeg"
                elif(".png" in img_src):
                    version_img = img_name + ".png"
                if(version_img != ""):
                    filename = "./" + version_img
                    img_content = getContent(img_src, session, useProxy)
                    with open(filename, 'wb') as f:
                        f.write(img_content)
                    print("图片下载到： " +  filename)
                print(version_img)
        return version_img
    except Exception as ex:
        print("-----下载图片出错，继续-----")
        print(ex)
        pass

def getBookInventoryArray(allInventoryTableSoup):
    book_inventory_array = []
    libList = ["杭州图书馆","杭少图分馆","萧山图书馆","余杭图书馆","拱墅区图书馆",
                        "上城区图书馆","西湖区图书馆","滨江区图书馆","下城区图书馆","江干区图书馆"]
    #筛选馆藏
    for inventoryTable in allInventoryTableSoup[1:]:
        allInventoryTr = inventoryTable.find("td")
        book_inventory = {}
        call_number = allInventoryTr[0].text
        status = allInventoryTr[2].text
        lib_name = ""
        lib_room = allInventoryTr[6].text
        temp_lib_name = allInventoryTr[5].text
        if((allInventoryTr[5].text == "杭州图书馆") and ('少儿分馆' in lib_room)):
            lib_name = "杭州少年儿童图书馆"
        elif((allInventoryTr[5].text == "杭州图书馆") and ('财商主题分馆' in lib_room)):
            lib_name = "杭财商分馆"
        elif((allInventoryTr[5].text == "杭州图书馆") and ('浣纱馆外借' in lib_room)):
            lib_name = "杭浣纱分馆"
        elif((allInventoryTr[5].text == "杭州图书馆") and ('运动分馆' in lib_room)):
            lib_name = "杭运动分馆"
        elif((allInventoryTr[5].text == "杭州图书馆") and ('康养分馆' in lib_room)):
            lib_name = "杭康养分馆"
        elif((allInventoryTr[5].text == "杭州图书馆") and ('专题文献中心' in lib_room)):
            lib_name = "杭州图书馆"
        elif((allInventoryTr[5].text == "滨江区图书馆分馆") and ('网易蜗牛读书馆' in lib_room)):
            lib_name = "网易蜗牛读书馆"
        elif((allInventoryTr[5].text == "西湖区图书馆分馆") and ('古荡街道西湖书房' in lib_room)):
            lib_name = "西湖书房古荡分馆"
        elif((allInventoryTr[5].text == "西湖区图书馆分馆") and ('转塘街道西湖书房' in lib_room)):
            lib_name = "西湖书房转塘分馆"
        elif((allInventoryTr[5].text == "西湖区图书馆分馆") and ('蒋村街道西湖书房' in lib_room)):
            lib_name = "西湖书房蒋村分馆"
        elif((allInventoryTr[5].text == "西湖区图书馆分馆") and ('留下街道西湖书房' in lib_room)):
            lib_name = "西湖书房留下分馆"
        elif((allInventoryTr[5].text == "西湖区图书馆分馆") and ('西湖区文新街道' in lib_room)):
            lib_name = "西湖文新分馆"
        elif((temp_lib_name in libList) and (('借' in lib_room) or ('西湖' in lib_room) or ('少儿' in lib_room))):
            lib_name = allInventoryTr[5].text
        
        if(lib_name != ""):
            book_inventory ={
                "call_number": call_number,
                "status": status,
                "lib_name": lib_name,
                "lib_room": lib_room
            }
            book_inventory_array.append(book_inventory)
    
    return book_inventory_array

#输入单本书的编号，可获取此书详细信息
def getBookDetail(book_no, origin_title, which_book_count, session, web_domain, useProxy):
    search_url = web_domain + "/opac/book/" + book_no
    html = getHtml(search_url, session, useProxy)
    allTableSoup = html.find("#bookInfoTable", first=True)

    #检查是否成功拿到表格数据，拿不到则重复调用，最多25次
    retry_count = 0
    if(type(allTableSoup) == type(None)):
        while(type(allTableSoup) == type(None) and retry_count<25):
            print("no table information in this html")
            html = getHtml(search_url, session, useProxy)
            allTableSoup = html.find("#bookInfoTable", first=True)
            retry_count += 1
        if(retry_count>=25):
            print("25 times failed")
            return None

    print("render begin")
    html.render(timeout=60)
    print("render finish")

    #下载此书的图片
    version_img = downloadImage(html, origin_title, which_book_count, session, useProxy)
    print(version_img)
    #获取此书的书目信息
    title = getDataSortText(allTableSoup,"tr[data-sort='0']","h2")
    author = getDataSortText(allTableSoup,"tr[data-sort='40']").split(r"/")
    if(len(author)>=2):
        author = author[1]
    elif(len(author)==1):
        author = author[0]
    price = getDataSortText(allTableSoup,"tr[data-sort='10']").split(r"CNY")
    if(len(price)>=2):
        price = price[1]
    else:
        price = getDataSortText(allTableSoup,"tr[data-sort='10']").split(r"TWD")
        if(len(price)>=2):
            price = price[1]
        else:
            price = getDataSortText(allTableSoup,"tr[data-sort='10']").split(r"￥")
            if(len(price)>=2):
                price = price[1]
            else:
                price = price[0]
    page_count = getDataSortText(allTableSoup,"tr[data-sort='60']").split(r";")
    if(len(page_count)>=1):
        page_count = page_count[0]
    publisher = getDataSortText(allTableSoup,"tr[data-sort='50']")
    content = getDataSortText(allTableSoup,"tr[data-sort='70']")
    
    real_version_obj ={
        "title": title,
        "author": author,
        "price": price,
        "page_count": page_count,
        "publisher": publisher,
        "content": content,
        "origin_title": origin_title,
        "version_img":version_img,
        "hz_lib_code":book_no
    }

    #获取此书的馆藏信息
    allInventoryTableSoup = html.find("table[class='dgrid-row-table']")
    book_inventory_array = getBookInventoryArray(allInventoryTableSoup)
        
    bookDetail={
        "real_version": real_version_obj,
        "inventory": book_inventory_array
    }
    return bookDetail

#获取到含指定内容的正确html
def getCorrectHtml(url, title, session, max_try, useProxy):
    html = getHtml(url, session, useProxy)
    allTableSoup = html.find("table[class='resultTable']", first=True)
    allHyperLinkSoup = html.find("div[class='meneame']", first=True)
    
    while((type(allTableSoup) == type(None)) or (type(allHyperLinkSoup) == type(None))):
        max_try -= 1
        print("max_try - 1")
        print("allTableSoup:")
        print(allTableSoup)
        print("allHyperLinkSoup:")
        print(allHyperLinkSoup)
        if(type(allHyperLinkSoup) == type(None)):
            max_try -= 2
        print("max_try - 2")
        if(max_try > 0):
            html = getCorrectHtml(url, title, session, max_try, useProxy)
            allTableSoup = html.find("table[class='resultTable']", first=True)
            allHyperLinkSoup = html.find("div[class='meneame']", first=True)
        else:
            return None        

    hyper_link = allHyperLinkSoup.find("a")[-2]
    print(hyper_link)
    url_params = parse.parse_qs(parse.urlparse(hyper_link.attrs["href"]).query)
    result_title = url_params['q0'][0]
    print("result_title: " + result_title)
    while(result_title != title):
        print("max_try - 1" )
        max_try -=1
        if(max_try > 0):
            html = getCorrectHtml(url, title, session, max_try, useProxy)
            hyper_link = html.find("div[class='meneame']", first=True).find("a")[-2]
            url_params = parse.parse_qs(parse.urlparse(hyper_link.attrs["href"]).query)
            result_title = url_params['q0'][0]
            if(result_title == title):
                break
        else:
            return None

    return html

#输入一个书名和其作者，可获取单页十本相关书籍的详细信息，输出到obj_array对象中
#此函数将递归调用填充obj_array对象
def getSearchResult(obj_array, url ,title, author, which_book_count, session, web_domain, useProxy, endPage, max_try):
    html = getCorrectHtml(url, title, session, max_try, useProxy)
    
    if(html == None):
        return obj_array

    allTableSoup = html.find("table[class='resultTable']", first=True)
    book_no_list = getBooksNoList(allTableSoup)
    print(book_no_list)
    for book_no in book_no_list:
        print("------------------begin search:"+ book_no + "  ----------------------")
        book_detail = getBookDetail(book_no, title, which_book_count, session, web_domain, useProxy)
        print(book_detail)
        if(book_detail != None):
            obj_array.append(book_detail) 
            which_book_count += 1

    #检查是否到下一页的url是否等于此页，也就是检查是否最后一页
    allHyperLinkSoup = html.find("div[class='meneame']", first=True)
    hyper_link = allHyperLinkSoup.find("a")[-2]
    next_url: str = web_domain + hyper_link.attrs["href"]
    if next_url[-1] == url[-1] and next_url[-2] == url[-2] and next_url[-3] == url[-3] and next_url[-4] == url[-4]:
        print("last page have been finished!")
        return obj_array
    else:
        if next_url.endswith("&page=1") or next_url.endswith("&page=" + str(endPage)):
            print("given page have been finished!")
            return obj_array
        else:
            max_try = 25
            return getSearchResult(obj_array, next_url, title, author, which_book_count, session, web_domain, useProxy, endPage, max_try)
