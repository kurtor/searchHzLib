import time

def getListFromTxt(path):
    book_name_list = []
    with open(path,'r', encoding='UTF-8') as f:
        data = f.readlines()

        for line in data:
            if len(line.strip()) != 0 :
                name = line.split('《')[1].split("》")[0]
                book_name_list.append(name)

    return book_name_list

def getTimestamp():
    now = int(round(time.time()*1000))
    timestamp = time.strftime('%Y%m%d_%H%M%S',time.localtime(now/1000))
    return timestamp