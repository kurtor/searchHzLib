searchHzLib-书单爬虫【杭州图书馆馆藏信息】并输出
=======



根据给定的【书单txt文件】，爬虫查询杭州图书馆馆藏信息，并输出为详细的表格文件，最后一列为yes代表可借

涉及：python，request_html，pyppeteer，代理池



###  准备工作



- 1.安装python的Anaconda环境

  官网：https://www.anaconda.com/products/individual#Downloads

  清华镜像站：https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

  

- 2.打开Anaconda Prompt工具，pip安装依赖requests_html

  ```
  pip install requests_html
  ```

  【注意】调用requests_html的render时，会有问题，需要如下操作：

  ```
  找到以下源码位置：
  $python\Lib\site-packages\requests_html.py
  
  //搜索headless关键字，把后面的True改成False
  ```

  

- 3.pip安装依赖pyppeteer

  ```
  pip install pyppeteer
  ```

  【注意】首次调用puppeteer时会默认下载chromium，由于要访问谷歌源，无代理无法下载。所以要提前按下面把谷歌源改成淘宝源

  ```
  //找到pyppeteer源码所在位置:
  $python\Lib\site-packages\pyppeteer\chromium_downloader.py
  
  //找到DEFAULT_DOWNLOAD_HOST字段的值，改成淘宝源:
  https://npm.taobao.org/mirrors
  ```

  【注意】pyppeteer依赖的urllib3是1.25以上，而request老版本2.20依赖的urllib3包是老版本1.24，所以要把request强制更新到2.23版本。

  

###  配置代理池

默认使用代理爬虫，需要自己本地构建代理池。

（也可以不用，只要把useProxy变量改为False即可）



构建来源参考：https://github.com/jhao104/proxy_pool

以下几点注意：
1.需要低版本python3.5运行,创建虚拟环境

```
conda create -n py35 python=3.5
```
2.需要依赖lxml包

打开https://www.lfd.uci.edu/~gohlke/pythonlibs/，
网页内搜索lxml，下载为虚拟环境python3.5准备的lxml包

```
【安装】先切换到py35环境，再cd到下载文件所在目录
pip install ./lxml-4.4.3-cp35-cp35m-win_amd64.whl
```

3.需要依赖windows版本的redis

打开https://github.com/microsoftarchive/redis/releases
下载msi包安装redis，注意官网无win版本



###  运行

1.如果配了代理池，把proxy_pool文件夹放到根目录下，点击proxy_pool_open.bat自动用py35环境运行

2.配置书单，文件是douban.txt（书名一行一个，用《》括起来）

3.运行activate.bat开始爬虫（默认一本书最多爬3页，可通过endPage变量更改，结果输出到根目录下）



【如果anaconda装在个人用户下，替换脚本在文件夹内，拿出来替换掉外面的】