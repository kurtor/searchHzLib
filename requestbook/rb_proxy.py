import requests


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHtml(url, session, useProxy):
    
    proxies = {}

    if(useProxy):
        proxy = get_proxy().get("proxy")
        if(proxy):
            print("--------------get proxy success-----------------")
            print(proxy)
            proxies = {"http": "http://{}".format(proxy)}
        else:
            print("proxy server failed")
            return False
    
    retry_count = 3
    while retry_count > 0:
        try:
            if(useProxy):
                html = session.get(
                    url, proxies=proxies, timeout=0.8).html
                # 使用代理访问
                return [html, useProxy] 
            else:
                html = session.get(
                    url, timeout=0.8).html
                # 使用代理访问
                return [html, useProxy]        
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    if(useProxy):
        print("this proxy failed，delete")
        delete_proxy(proxy)

    return getHtml(url, session,useProxy)