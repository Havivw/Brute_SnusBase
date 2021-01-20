import re
import csv
import time
import string
import logging
import requests
from os.path import isfile
from random import shuffle
from random import randint

import click
from bs4 import BeautifulSoup
from colorlog import ColoredFormatter

from hashid import check_hash


# Setting up a logger
def setup_logger(verbose=False):
    """Return a logger with a default ColoredFormatter."""
    logging.addLevelName(21, 'SUCCESS')
    logging.addLevelName(11, 'PROCESS')
    logging.addLevelName(12, 'FAIL')
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s - %(name)-5s -  %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'ERROR':    'red',      # LEVEL: 40
            'CRITICAL': 'red',      # LEVEL: 50
            'INFO':     'cyan',     # LEVEL: 20
            'FAIL':     'red',      # LEVEL: 12
            'DEBUG':    'white',    # LEVEL: 10
            'SUCCESS':  'green',    # LEVEL: 21
            'PROCESS':  'purple',   # LEVEL: 11
            'WARNING':  'yellow'})  # LEVEL: 30

    logger = logging.getLogger('SnusBrute')
    setattr(logger, 'success', lambda *args: logger.log(21, *args))
    setattr(logger, 'process', lambda *args: logger.log(11, *args))
    setattr(logger, 'fail', lambda *args: logger.log(12, *args))
    fh = logging.FileHandler('SnusBrute.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(handler)
    if not verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    return logger



def extrct_cookies_csrf(logger, user, password):
    logger.info("Extract Cookies and CSRF_Token Details.")
    login_url = "https://snusbase.com:443/login"
    headers = {"Connection": "close", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "https://snusbase.com",
                     "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document",
                     "Referer": "https://snusbase.com/login", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}

    response = requests.get(login_url, headers=headers)
    cfduid = response.cookies["__cfduid"]
    a = response.cookies["a"]

    cookies = {"__cfduid": cfduid, "a": a}
    data = {"login": user, "password": password, "action_login": ''}
    response = requests.post(login_url, headers=headers, cookies=cookies, data=data, allow_redirects=False)
    lg = response.cookies["lg"]

    cookies = {"__cfduid": cfduid, "a": a, "lg": lg}
    response = requests.get("https://snusbase.com/search", headers=headers, cookies=cookies)
    parsed_html = BeautifulSoup(response.content, 'html.parser')
    csrf = parsed_html.find("input", attrs={'name': 'csrf_token', 'type': 'hidden'})
    csrf = re.split(r'value="', str(csrf))
    csrf_token = csrf[1].split('"')[0]
    return cfduid, a, lg, csrf_token, headers

def get_brute_latter():
    letters = list(i+b for i in string.ascii_lowercase for b in string.ascii_lowercase)
    shuffle(letters)
    return letters

def get_password(data):
    try:
        Password = re.findall(r'<td>password </td><td class="datatable" id=.*', data)
        Password1 = Password[0].split('>')
        Password2 = Password1[3].split('<')
        lPassword = Password2[0].rstrip()
    except:
        lPassword = ''
    return lPassword

def get_Hash_data(data):
    try:
        Hash = re.findall(r'<td>hash </td><td class="datatable" id=.*', data)
        Hash1 = Hash[0].split('>')
        Hash2 = Hash1[3].split('<')
        lHash = Hash2[0].rstrip()
        tHash = check_hash(hash_string=lHash)
    except:
        lHash = ''
        tHash = ''
    return lHash, tHash

def get_user_and_domain(data):
    try:
        eMail = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', data)
        leMail = eMail[0]
        userName, domainName = leMail.split('@')
    except:
        userName = ''
        domainName = ''
    return userName, domainName

def get_dump_name(data):
    try:
        Dump = re.findall(r'<div id="topBar">[\w\d_\-.]+[\s]?<', data)
        Dump1 = Dump[0].split(">")
        Dump2 = Dump1[1].split("<")
        lDump = Dump2[0]
    except:
        lDump = ''
    return lDump

def write_result_file(domain, data=None):
    with open(f'Credentials_File_{domain}.csv', mode='a') as credentials_file:
        credentials_writer = csv.writer(credentials_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if data:
            credentials_writer.writerow(data)
        else:
            credentials_writer.writerow(['User Name', 'Domain Name', 'Hash', 'Hash Type', 'Password', 'Dump'])

def get_and_aprsed_content(url, headers, cookies, req_data):
    response = requests.post(url, headers=headers, cookies=cookies, data=req_data)
    parsed_html = BeautifulSoup(response.content, 'html.parser')
    span = parsed_html.find("span", id="result_count")
    return span, parsed_html

def serach(brute_letters, domain, cfduid, a, lg, csrf_token, headers, logger):
    logger.info("Start BruteForce on SnusBase.")
    url = "https://snusbase.com:443/search"
    cookies = {"__cfduid": f"{cfduid}", "a": f"{a}", "lg": f"{lg}"}
    write_result_file(domain=domain)
    for letters in brute_letters:
        remail = f"{letters}%@%{domain}%"
        req_data = {"csrf_token": f"{csrf_token}", "term": remail, "wildcard": "on", "searchtype": "email"}
        span, parsed_html = get_and_aprsed_content(url, headers, cookies, req_data)
        try:
            Count = int(span.text)
        except:
            try:
                time.sleep(randint(1, 3))
                span, parsed_html = get_and_aprsed_content(url, headers, cookies, req_data)
                Count = int(span.text)
            except:
                Count = 0
                logger.fail(f"{letters} Failed!")
        if (Count != 0):
            logger.success(f"{letters} found {Count} results on {domain}.".format(span.text, remail))
            content = parsed_html.find("div", {"id": "contentArea"})
            data_list = re.split(r'<div class="searchtools">', str(content))
            del data_list[0]
            for data in data_list:
                lDump = get_dump_name(data)
                userName, domainName = get_user_and_domain(data)
                lHash, tHash = get_Hash_data(data)
                lPassword = get_password(data)

                all_data = [userName, domainName, lHash, tHash, lPassword, lDump]
                write_result_file(domain=domain, data=all_data)
        time.sleep(randint(1, 5))

def file_to_list(pathfile):
    with open(pathfile, "r") as file_content:
        content_list = [line.strip() for line in file_content.readlines()]
    return content_list


def parse_domain_input(domain):
    domain_list = []
    domain = domain.replace(' ', '')
    if isfile(domain):
        domain_list = file_to_list(pathfile=domain)
    else:
        domain_list.append(domain)
    return domain_list

###################################CLICK- CLI########################################

CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda param: param.lower(),
    ignore_unknown_options=True)


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('-u',
              '--user', help="SnusBase user name.")
@click.option('-p',
              '--password',
              help='SnusBase password.')
@click.option('-d',
              '--domain',
              help='Domain name for BruteForce or file with domains list (only domain name like: google). search regex (aa*@*domain*) ')
@click.option('-v',
              '--verbose',
              is_flag=True,
              help="Display run log in verbose mode.")

def SnusBaseBrute(user, password, domain, verbose):

    """ Run BruteForce on SnusBase using aa*@*domain* """
    logger = setup_logger(verbose=verbose)
    brute_letters = get_brute_latter()
    domain_list = parse_domain_input(domain)
    for domain_name in domain_list:
        cfduid, a, lg, csrf_token, headers = extrct_cookies_csrf(user=user, password=password, logger=logger)
        serach(brute_letters=brute_letters, domain=domain_name, cfduid=cfduid, a=a,
               lg=lg, csrf_token=csrf_token, headers=headers, logger=logger)


