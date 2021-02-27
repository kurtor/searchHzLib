# -*- coding: utf-8 -*-
from rb_proxy import getHtml
import time
import random
import pandas as pd


def get_value_list(allTableSoup):
    id_value_list = []
    foundAllTr = allTableSoup.find("tr")
    for trSoup in foundAllTr:
        foundAllTd = trSoup.find("td")
        td_input = foundAllTd[0].find("input", first=True)
        id_value = td_input.attrs["value"]
        if(id_value):
            foundBookMeta = foundAllTd[3].find(
                "div[class='bookmeta']", first=True)
            if(foundBookMeta):
                bookInfo = foundBookMeta.find("div")
                title = bookInfo[1].find(
                    "a[class='title-link']", first=True).text.strip()
                author = bookInfo[2].find(
                    "a[class='author-link']", first=True).text.strip()
                publisher = bookInfo[3].find(
                    "a[class='publisher-link']", first=True).text.strip()
                callnosSpan = bookInfo[4].find(
                    "span[class='callnosSpan']", first=True).text.strip()
                callnosSpan_short = callnosSpan[0:callnosSpan.find(
                    '/')]
                id_name_value = [id_value, title,
                                 author, publisher, callnosSpan_short]
                id_value_list.append(id_name_value)
                print("id_value:" + id_value)
    return id_value_list


def get_book_code(bookTableSoup, id_value):
    foundBookTr = bookTableSoup.find("tr")
    # print(foundBookTr)
    all_info: list = []
    for trSoup in foundBookTr:
        foundTableTd = trSoup.find("td")
        bookLocation = foundTableTd[1].text
        if(bookLocation == '杭州图书馆'):
            bookNumber = foundTableTd[0].text
            bookRoom = foundTableTd[2].text
            bookCount: str = foundTableTd[3].text
            print("----------")
            print(bookLocation)
            print(bookRoom)
            print(id_value[1])
            print(bookNumber)
            print(bookCount)
            book_count_arrow = bookCount.split(r'/')
            book_can_be_borrow = 'no'
            if(int(book_count_arrow[0]) < int(book_count_arrow[1])):
                book_can_be_borrow = 'yes'
            all_info.append([bookLocation, bookRoom, id_value[1], bookNumber,
                             bookCount, book_can_be_borrow])
    return all_info


def getSearchResult(temp_data, url, session, web_domain, useProxy, endPage):
    html_proxy = getHtml(url, session, useProxy)
    html = html_proxy[0]
    if(html == False):
        print("stop getSearchResult function")
    else:
        contentDivSoup = html.find("#contentDiv", first=True)
        allTableSoup = html.find("table[class='resultTable']", first=True)
        retry_count = 0
        while((type(contentDivSoup) == type(None) or type(allTableSoup) == type(None)) and retry_count<25):
            print("no table information in this html")
            html_proxy = getHtml(url, session, useProxy)
            html = html_proxy[0]
            contentDivSoup = html.find("#contentDiv", first=True)
            allTableSoup = html.find("table[class='resultTable']", first=True)
            retry_count += 1

        PageResultSoup = html.find("div[class='meneame']", first=True)
        if(type(PageResultSoup) == type(None)):
            return temp_data
        id_value_list = get_value_list(allTableSoup)
        print("render begin")
        html.render()
        print("render finish")
        new_data = pd.DataFrame()
        pd_book_location = []
        pd_book_room = []
        pd_book_title = []
        pd_book_number = []
        pd_book_count = []
        pd_book_borrow = []
        for id_value in id_value_list:
            book_borrow_id = '#holdingPreviewDiv_' + id_value[0]
            bookTableSoup = html.find(book_borrow_id, first=True)
            # print(bookTableSoup.html)
            all_info = get_book_code(bookTableSoup, id_value)
            for info in all_info:
                pd_book_location.append(info[0])
                pd_book_room.append(info[1])
                pd_book_title.append(info[2])
                pd_book_number.append(info[3])
                pd_book_count.append(info[4])
                pd_book_borrow.append(info[5])
        new_data['Location'] = pd_book_location
        new_data['Room'] = pd_book_room
        new_data['Title'] = pd_book_title
        new_data['No.'] = pd_book_number
        new_data['allowance'] = pd_book_count
        new_data['can be borrow?'] = pd_book_borrow
        temp_data = pd.concat((temp_data, new_data))
        pageSoup = html.find("div[class='meneame']", first=True)
        next_page = pageSoup.find("a")[-2]
        print(next_page)
        next_url: str = web_domain + next_page.attrs["href"]
        if next_url[-1] == url[-1] and next_url[-2] == url[-2] and next_url[-3] == url[-3] and next_url[-4] == url[-4]:
            print("last page have been finished!")
            return temp_data
        else:
            if next_url.endswith("&page=1") or next_url.endswith("&page=" + str(endPage)):
                print("last page have been finished!")
                return temp_data
            else:
                time_slot = random.uniform(0.8, 1.5)
                print(time_slot)
                time.sleep(time_slot)
                return getSearchResult(temp_data, next_url, session, web_domain, useProxy, endPage)
