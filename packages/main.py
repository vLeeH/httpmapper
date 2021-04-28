#!/usr/bin/env python3

# -*- coding utf-8 -*-
from httpmapper import *
import time

banner()
alvo = str(input('[*] Enter the website URL: ')).lower().strip()

def main():
    time.sleep(0.5)
    ask = str(input('[*] What do you want to know?[Website/Links/Navigate/Emails/Cookies/Grabbing] ')).lower().strip()

    if ask == 'website': 
        extract_websites(alvo)
    elif ask == 'links': 
        get_links(alvo)
    elif ask == 'navigate':   
        navigate_links(alvo)
    elif ask == 'emails':
        extract_emails(alvo)
    elif ask == 'cookies':
        extract_cookies(alvo)
    elif ask == 'grabbing':
        cookie = str(input('[*] Enter the website cookie: '))
        website_grabber(alvo, cookie)
    else: 
        print('[-] Enter a valid answer.')

    print()
    options = str(input('Do you want to make a consultation again?[Y/N] ')).upper().strip()
    if options == 'Y':
        banner()
        main()
    
    elif options == 'N': 
        banner()
        print('\033[31m [+] Thanks for using the tool.\033[0m')
        exit()

    else: 
        banner()
        print('Invalid option!')


if __name__ == '__main__':
    main()
