import sys,os
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
url=[]
queueLock = threading.Lock()
upload_path = ["/admin/file","/admin/file.php","/admin/fileupload","/admin/fileupload.asp","/admin/fileupload.aspx","/admin/fileupload.jsp","/admin/fileupload.php","/admin/upload","/admin/upload.asp","/admin/upload.aspx","/admin/upload.do","/admin/upload.jsp","/admin/upload.php","/admin/uploads","/admin/uploads.asp","/admin/uploads.aspx","/admin/uploads.jsp","/admin/uploads.php","/api/addFile","/api/upload","/api/uploadFile","/file_upload","/upfile.php","/file_upload.asp","/file_upload.aspx","/file_upload.jsp","/file_upload.php","/fileupload","/fileupload.asp","/fileupload.aspx","/fileupload.jsp","/fileupload.php","/ispirit/im/upload.php","/system/upload.php","/upload","/upload.asp","/upload.aspx","/upload.do","/upload.jsp","/upload.php","/upload/upload.asp","/upload/upload.aspx","/upload/upload.jsp","/upload/upload.php","/uploadfile","/file","/filedata","/file1","/files","/up","/upload1","/upload2","/upfile","/uploadimg","/uploadimage","/uploadimages","/fileup","/fileuploads","/text","/img","/upimg","/upimages","/upimage","/pcimg","/phoneimg","/strFile","/uploadForm","/MicroWebsiteIndex","/picture","/photo","/fileBlank","/fileFixture","/filename","/fileUploader"]


def check_vul(target_url):
    try:
        if target_url.endswith('/'):
            target_url = target_url[:-1]
        file_name = "upload.cpyup"
        for upload in upload_path:
            target_url_change = target_url + upload
            check_upload(target_url_change,file_name)
    except Exception as e:
        print('[-]????????????????????????????????????' + str(e))

def check_upload(target_url,file_name):
    try:
        target_url = check_url_http(target_url)
        files = {'file': open(file_name, 'rb')}
        headers["User-Agent"] = choice(USER_AGENTS)
        if "https" in target_url:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # ??????SSL???????????????
            res = requests.post(target_url, files=files, verify=False ,timeout=5)
        else:
            res = requests.post(target_url, files=files,timeout=5)
        text = res.text
        res = res.status_code
        if res == 200 and 'cpyup' in text:
            cprint('[+]' + target_url + '?????????????????????????????????????????????????????????', 'red')
            with open('???????????????????????????.txt', 'a', encoding='utf-8') as f:
                f.writelines(target_url)
                f.write('\n')
        else:
            print("[-]?????????????????????????????????")
    except:
        print('[-]????????????????????????????????????' + target_url)
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.writelines(target_url)
            f.write('\n')


def start_jobs(data, num):
    """
    ????????????????????????
    argument: data -> ???????????? num -> ?????????
    """
    is_alive = [True]

    def job():
        """????????????"""
        while is_alive[0]:
            try:
                ip = data.get()
                if ip is None:
                    break  # ??????????????????
                queueLock.acquire()  # ?????????,????????????????????????????????????????????????
                check_vul(ip)  # ????????????
                queueLock.release()  # ????????????????????????????????????????????????
            except:
                is_alive[0] = False
        data.put(None)  # ????????????

    jobs = [Thread(target=job) for i in range(num)]  # ??????????????????
    for j in jobs:
        j.setDaemon(True) # ???????????????????????????
        j.start()  # ????????????

    for j in jobs:
        j.join()  # ???????????????????????????????????????????????????????????????


def check_url_http(url):
    isHTTPS = True
    if "http" not in url:
        try:
            target_url = "https://" + url
            """
            requests????????????????????????????????????????????????????????????,????????????verify?????????False??????????????????,????????????verify=False???????????????InsecureRequestWarning?????????
            """
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # ??????SSL???????????????
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
    file_name = str(sys.argv[2])  # ???????????????
    for line in open(file_name):
        ip = line.strip()         #????????????????????????????????????,????????????????????????,??????????????????????????????
        if ip:
            url.append(ip)

def create_file():
    current_path = os.getcwd()
    path = current_path + '\\upload.cpyup'
    if os.path.exists(path):
        print('exist')
    else:
        with open('upload.cpyup', 'a', encoding='utf-8') as f:
            f.write('11111')


def main():
    cprint('''
                 .__                .__                       .__                    .___
  ____   ____    |  |   ____   ____ |__| ____     __ ________ |  |   _________     __| _/
 /    \ /  _ \   |  |  /  _ \ / ___\|  |/    \   |  |  \____ \|  |  /  _ \__  \   / __ | 
|   |  (  <_> )  |  |_(  <_> ) /_/  >  |   |  \  |  |  /  |_> >  |_(  <_> ) __ \_/ /_/ | 
|___|  /\____/   |____/\____/\___  /|__|___|  /  |____/|   __/|____/\____(____  /\____ | 
     \/                     /_____/         \/         |__|                   \/      \/ 

        ''', "yellow")
    if len(sys.argv) != 3:  # ??????????????????????????????
        cprint('''Explain:
        -h      show this help message and exit
        -u      Target URL
        ''', "blue")
        cprint('''Example:
        python3 nologin_upload.py -h 10.10.10.10
        python3 nologin_upload.py -r ip.txt''', "magenta")
        return
    a = str(sys.argv[1])  # ????????????
    if a == '-u':
        target_url = str(sys.argv[2])  # ??????ip??????
        url.append(target_url)
    if a == '-r':
        ip_read()
    create_file()  # ???????????????????????????
    """???????????????"""
    data = Queue()
    for ip in url:
        data.put(ip) # ????????????
    data.put(None)  # ????????????
    num = 100  # ??????100??????
    begin = time()
    start_jobs(data, num)  # ??????????????????
    end = time()
    print('??????????????? %ss' % str(end - begin))


if __name__ == '__main__':
    main()
