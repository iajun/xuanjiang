import requests
from requests.exceptions import RequestException #请求出现异常的模块
from pyquery import PyQuery as pq #解析模块
import threading #多线程模块
from queue import Queue #队列模块
class ProXiesAD(threading.Thread): #创建一个线程类
    def __init__(self,set_queue):
        super(ProXiesAD, self).__init__()
        self.set_queue = set_queue
    def run(self):
        global KY_HOST
        while not PARSE_EXIT: #循环取队列一直将队列取空
            try:
                host = self.set_queue.get()
                proxies = {'https':host,'http':host}
                get_code = requests.get(url='https://www.baidu.com/',proxies=proxies,timeout=5,headers=headers).status_code #返回请求百度的状态码
            except RequestException:
                print("不可用")
            else:
                if get_code == 200:
                    KY_HOST.append(host)
                    print('可用'+host)
                else:
                    print('请求超时')
        print(KY_HOST)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'} #头
HOST = []
KY_HOST = []
PARSE_EXIT = False

def url_text(url):
    try:
        texts = requests.get(url,headers=headers)
    except RequestException:
        print('请求错误')
    else:
        if texts.status_code==200: #状态码为200说明请求成功
            return texts.text

def re_response(text):
    global HOST#全局变量声明
    doc = pq(text)
    for i in doc('tr').items():
        ip = i('tr td:lt(3)').text().replace(' ',"",1).replace(' ',':')#解析
        if ip.find("."):
            HOST.append(ip)#存到列表里面
    del HOST[0]

def get_pool(ints):
    url = 'http://www.xicidaili.com/nn/'+ints
    text = url_text(url)
    re_response(text)
    pagequeue = Queue()#创建队列
    threadkeep=[]
    for i in HOST:
        pagequeue.put(i)#将ip放到队列里面去
    keepList = ["保存线程一号","保存线程二号","保存线程三号"]
    for threadName in keepList: #创建三个线程
        thread = ProXiesAD(pagequeue)
        thread.start()
        threadkeep.append(thread)

    while not pagequeue.empty(): #等待队列为空
        pass
    global PARSE_EXIT
    PARSE_EXIT = True #队列为空循环结束
    for thread in threadkeep:#主线程等待子线程结束在结束
        thread.join()
# if __name__ == '__main__':
#     main("1")