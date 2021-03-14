searchHzLib-书单爬虫【杭州图书馆馆藏信息】
=======

<br>

输入：书单（txt文件）

输出：杭州图书馆馆藏信息和书籍图片（输出为json格式文件和versionImg图片文件夹）

【涉及】python，request_html，pyppeteer，代理池

【作用】作为图书项目中后端的导入数据

<br>

###  准备工作

- 1.安装python的Anaconda环境

  官网：https://www.anaconda.com/products/individual#Downloads

  清华镜像站：https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

<br>

- 2.打开Anaconda Prompt工具，pip安装依赖requests_html

  ```
  pip install requests_html
  ```

  【注意】调用requests_html的render时，可能会有问题，需要如下操作：

  ```
  找到以下源码位置：
  $python\Lib\site-packages\requests_html.py
  
  //搜索headless关键字，把后面的True改成False
  ```

<br>

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

<br>  

###  配置代理池

默认使用代理爬虫，需要自己本地构建代理池。

（也可以不用，只要把入口文件rb_spyder.py中useProxy变量改为False即可）

<br>

构建来源参考：https://github.com/jhao104/proxy_pool

构建后获取代理：http://127.0.0.1:5010/get/

<br>

【注意】如果访问后无法获取到代理，那可能需要低版本python3.5

1.创建虚拟环境

```
conda create -n py35 python=3.5
```

<br>

2.进入proxy_pool目录找到requirements.txt，打开删掉lxml和redis相关的两行

<br>

3.激活虚拟环境，安装依赖

```
【安装】先activate py35切换到环境，再cd到下载文件所在目录
pip install -r requirements.txt
```

<br>

4.自行安装依赖lxml

打开https://www.lfd.uci.edu/~gohlke/pythonlibs/，

网页内搜索lxml，下载为虚拟环境python3.5准备的lxml包

```
【安装】先切换到py35环境，再cd到下载文件所在目录
pip install ./lxml-4.4.3-cp35-cp35m-win_amd64.whl
```

<br>

5.自行安装redis

打开https://github.com/microsoftarchive/redis/releases ，

下载msi包安装redis，注意官网无win版本

<br>

###  运行

1.如果配了代理池，先手动开启

（也可把proxy_pool文件夹放到根目录下，点击proxy_pool_open.bat脚本自动用py35环境运行）

<br>

2.配置书单，文件是douban.txt

书名一行一个，格式参考：《书名》作者名 

（作者名也可省略，外国作者只写后半部分的姓）

<br>

3.运行activate.bat脚本开始爬虫（默认一本书最多爬3页，可通过endPage变量更改，结果输出到根目录下）

<br>

【如果anaconda装在个人用户下，替换脚本在文件夹内，拿出来替换掉外面的】
