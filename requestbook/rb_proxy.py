import requests


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

#代理获取返回内容的html属性
def getHtml(url, session, useProxy=True):
    proxies = {}
    if(useProxy):
        proxy = get_proxy().get("proxy")
        if(proxy):
            print("--------------try this proxy-----------------")
            print(proxy)
            proxies = {"http": "http://{}".format(proxy)}
        else:
            print("proxy server failed")
            return False
    retry_count = 2
    while retry_count > 0:
        try:
            if(useProxy):
                html = session.get(
                    url, proxies=proxies, timeout=2).html
                # 使用代理访问
                return html
            else:
                html = session.get(
                    url, timeout=2).html
                # 不使用代理访问
                return html   
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    if(useProxy):
        print("this proxy failed，delete")
        delete_proxy(proxy)
    return getHtml(url, session, useProxy)

#代理获取返回内容的content属性
def getContent(url, session, useProxy=True):
    proxies = {}
    if(useProxy):
        proxy = get_proxy().get("proxy")
        if(proxy):
            print("--------------try this proxy-----------------")
            print(proxy)
            proxies = {"http": "http://{}".format(proxy)}
        else:
            print("proxy server failed")
            return False
    retry_count = 2
    while retry_count > 0:
        try:
            if(useProxy):
                content = session.get(
                    url, proxies=proxies, timeout=2).content
                # 使用代理访问
                return content
            else:
                content = session.get(
                    url, timeout=2).content
                # 不使用代理访问
                return content   
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    if(useProxy):
        print("this proxy failed，delete")
        delete_proxy(proxy)
    return getContent(url, session, useProxy)