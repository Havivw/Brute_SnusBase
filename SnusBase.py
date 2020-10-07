import re
import sys
import csv
import time
import requests
from random import randint

from bs4 import BeautifulSoup

cfduid = "d59bef7ceb19c37c30ec371e52e6386691602055968"
a = "1bsjsjsomgvs2oqe51bjdjgn0c"
lg ="482679411110375b32789f353dc7fc5b2d70129b8484574bca65bc39edac6834"
rm = "U1gza0szUXhmdG1YR3ZHd2QzT3BqQT09%3A%3AMRMfqT6tJAi827eVzKnsxw%3D%3D"
csrf_token = "bc1d0ffb24060741fd2e0a8e840c5061525264"


burp0_url = "https://snusbase.com:443/search"
burp0_cookies = {"__cfduid": f"{cfduid}", "a": f"{a}", "lg": f"{lg}", "rm": f"{rm}"}
burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                 "Origin": "https://snusbase.com", "Content-Type": "application/x-www-form-urlencoded",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                 "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document",
                 "Referer": "https://snusbase.com/search", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}

def serach(file_name):
    with open(file_name, encoding='utf-8', errors='ignore') as dump_file:
        with open('Credentials_File.csv', mode='w') as credentials_file:
            credentials_writer = csv.writer(credentials_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            credentials_writer.writerow(['Mail Address', 'Hash', 'Password', 'Dump'])
        for remail in dump_file:
            remail = remail.rstrip()
            burp0_data = {"csrf_token": f"{csrf_token}", "term": remail, "wildcard": "on", "searchtype": "email"}
            response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
            parsed_html = BeautifulSoup(response.content, 'html.parser')
            span = parsed_html.find("span", id="result_count")
            try:
                Count = int(span.text)
            except:
                try:
                    time.sleep(randint(1, 3))
                    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies,
                                             data=burp0_data)
                    parsed_html = BeautifulSoup(response.content, 'html.parser')
                    span = parsed_html.find("span", id="result_count")
                    Count = int(span.text)
                except:
                    Count = 0
                    with open('errors.txt', encoding='utf-8', errors='ignore', mode='a') as error_file:
                        error_file.write(str(remail))

            if (Count != 0):
                print(f"{remail} found {Count} results.".format(span.text, remail))
                data = parsed_html.find("div", {"id": "contentArea"})
                ndata = re.split(r'<div class="searchtools">', str(data))
                del ndata[0]
                for n in ndata:
                    try:
                        Dump = re.findall(r'<div id="topBar">[\w\d_\-.]+[\s]?<', n)
                        Dump1 = Dump[0].split(">")
                        Dump2 = Dump1[1].split("<")
                        lDump = Dump2[0]
                    except:
                        lDump = 'None'
                    try:
                        eMail = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', n)
                        leMail= eMail[0]
                    except:
                        leMail = 'None'
                    try:
                        Hash = re.findall(r'<td>hash </td><td class="datatable" id=.*', n)
                        Hash1 = Hash[0].split('>')
                        Hash2 = Hash1[3].split('<')
                        lHash = Hash2[0].rstrip()
                    except:
                        lHash = 'None'

                    try:
                        Password = re.findall(r'<td>password </td><td class="datatable" id=.*', n)
                        Password1 = Password[0].split('>')
                        Password2 = Password1[3].split('<')
                        lPassword = Password2[0].rstrip()
                    except:
                        lPassword = 'None'
                    with open('Credentials_File.csv', mode='a') as credentials_file:
                        credentials_writer = csv.writer(credentials_file, delimiter=',', quotechar='"',
                                                        quoting=csv.QUOTE_MINIMAL)
                        credentials_writer.writerow([leMail, lHash, lPassword, lDump])
            time.sleep(randint(1, 5))

serach(file_name="mail.txt")