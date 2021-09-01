#!/usr/bin/env python3

# -*- coding utf-8 -*-
import os
import time
import urllib.request
import urllib.parse
from collections import deque
import re
from bs4 import *
import requests
import http.cookiejar
from time import sleep 

__version__='v0.1.3'
__author__='vLeeH'

class Colors: 
    red = "\033[91;1m"
    reset = "\033[0m"
    green = "\033[92;1m"
    cyan = "\033[96;1m"
    yellow = "\033[93;1m"
    magenta = "\033[95;1m"
    blue = "\033[94;1m"
    white = "\033[97;1m"
    blink = "\033[5m"

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f'''\033[31m
        | |__ | |_| |_ _ __  _ __ ___   __ _ _ __  _ __   ___ _ __ 
        | '_ \| __| __| '_ \| '_ ` _ \ / _` | '_ \| '_ \ / _ \ '__|
        | | | | |_| |_| |_) | | | | | | (_| | |_) | |_) |  __/ |   
        |_| |_|\__|\__| .__/|_| |_| |_|\__,_| .__/| .__/ \___|_|   
                      |_|                   |_|   |_|  
        {Colors.cyan}       
        Github: https://github.com/vLeeH/httpmapper
        By: {__author__}
        Version: {__version__}
   
    \033[0m''')


# Identify which browser is being used - Windows
# You can change that for Linux
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

def extract_websites(alvo):
    '''Extract source codes of websites.'''
    print('+------------------------------------------+')
    print('[+] Extacting WebServer:')
    print()
    if alvo.startswith('http'): 
        try: 
            source = requests.get(alvo).text
            soup = BeautifulSoup(source, 'lxml')
            print(soup.prettify())
            with open("extract_websites.html", "at+", encoding="utf8") as h:
                h.write(str(soup.prettify))

        except Exception as e:
            print(e)

    else: 
        print()
        print('[-] Enter a valid URL.')


def extract_title(content):
    '''Get HTML title of an URL.'''
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find("title", text=True)
    if not tag:
        return None
    return tag.string.strip()


def extract_links(content):
    '''Get links of URL's'''
    print('+------------------------------------------+')
    print('[+] Extacting links:')
    print()
    soup = BeautifulSoup(content, "lxml")
    links = set()  # Array but don't allow multiples elements
    for tag in soup.find_all("a", href=True):
        if tag["href"].startswith("http"):
            links.add(tag["href"])
    return links


def get_links(alvo):
    '''Create a log for links that are in the URL'''
    print('+------------------------------------------+')
    print('[+] Analyzing links:')
    print()
    page = requests.get(alvo)
    links = extract_links(page.text)
    for link in links: 
        print(link)
        with open('links.txt', 'at+', encoding="utf8") as t: 
            t.write(f"{link} \n\r")


def navigate_links(alvo):
    '''Function that navigate websites just using one URL.'''
    print('+------------------------------------------+')
    print('[+] Starting the navigate function.:')
    print()
    seen_urls = [alvo]
    available_urls = [alvo]
    while available_urls:
        url = available_urls.pop()
        try:
            content = requests.get(url, timeout=3).text

        except Exception:
            continue

        title = extract_title(content)

        if title:
            print("[+] Title: "+title)
            print("[+] URL: "+url)
            with open("links-titles.txt", "at+", encoding="utf8") as la:
                la.write("[+] Title: "+title+"\n\r [+] URL:"+url)

            time.sleep(0.5)
            print()

        for link in extract_links(content):
            if link not in seen_urls:
                seen_urls.append(link)
                available_urls.append(link)


def extract_emails(alvo):
    '''See URL's and emails.'''
    global emails
    try:
        print('+------------------------------------------+')
        print('[+] Extacting emails.:')
        print()
        if alvo.startswith('http'):
            try:
                urls = deque([alvo])
                count = 0
                scraped_urls = set()
                emails = set()
                while len(urls):
                    count += 1
                    if count == 100:
                        break
                    url = urls.popleft()
                    scraped_urls.add(url)

                    parts = urllib.parse.urlsplit(url)
                    base_url = "{0.scheme}://{0.netloc}".format(parts)

                    path = url[: url.rfind("/") + 1] if "/" in parts.path else url

                    print("[%d] Processing %s" % (count, url))
                    try:
                        response = requests.get(url)
                    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                        continue

                    new_emails = set(re.findall(r"[a-z0-9\.\-+]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
                    emails.update(new_emails)

                    soup = BeautifulSoup(response.text, features="lxml")

                    for anchor in soup.find_all("a"):
                        link = anchor.attrs["href"] if "href" in anchor.attrs else ""
                        if link.startswith("/"):
                            link = base_url + link

                        elif not link.startswith("http"):
                            link = path + link

                        if not link in urls and not link in scraped_urls:
                            urls.append(link)
                        
            except KeyboardInterrupt:
                print("[-] Closing")
                print()

            for mail in emails:
                print(mail)
                with open("emails.txt", "at+", encoding="utf8") as e: 
                    e.write(emails+" \n\r")

        else: 
            print('[-] Enter a avaible URL.')
            print()
    
    except Exception: 
        print('[ERROR]')


def extract_cookies(alvo):
    '''Get name and values of emails.'''
    if alvo.startswith('http'):
        try: 
            cookie_jar = http.cookiejar.CookieJar()
            url_opner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

            url_opner.open(alvo)
            for cookie in cookie_jar: 
                print("[+] Cookie Name = %s - Cookie Value = %s" % (cookie.name, cookie.value))
                with open("cookie.txt", "at+", encoding="utf8") as c: 
                    c.write(
                        "[+] Cookie Name = %s - Cookie Value = %s \n\r" % (cookie.name, cookie.value))

        except Exception: 
            print()
            print('[ERROR]')
        
        finally: 
            sleep(1)
            print('[-] Cookie extracter finished!')

    else: 
        print('[-] Enter an avaible URL.')


def website_grabber(alvo, cookie):
    '''Grab metadatas using URL and the Cookie.'''
    print('+------------------------------------------+')
    print('[+] Analyzing Metadatas.')
    print()
    if alvo.startswith('http'):
        try: 
            esc = str(input("[*] GET or POST: ")).strip().lower() 
            if esc == 'post':
                req = requests.post(alvo, cookies={'Cookie':cookie}, headers=header)
            elif esc == 'get':
                req = requests.get(alvo, cookies={'Cookie':cookie}, headers=header)
            else: 
                print('[!] Enter an avaible anwser.')

            code = req.status_code
            if code == 200:
                html = req.text
                print("\n[+] Request Succefully!\n")
                print(html.encode('utf-8'))
                with open("extract_grabs1.txt", "at+", encoding="utf8") as g: 
                    g.write(
                        f"{html.encode('utf-8')}") 
            else:
                print("[!] Request Failed, Exiting Program...\n")
                exit(1)
        
        except Exception as e: 
            print(f'[ERROR]{e}')
        
        finally: 
            sleep(1)
            print('[-] Website grabber finished!')
    else: 
        print('[-] Invalid URL.')

