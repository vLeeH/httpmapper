#!/usr/bin/env python3

# -*- coding utf-8 -*-
from os import system
try:
    import requests
    import http.cookiejar
    import bs4
except ImportError: 
    system("python3 -m pip install -r requirements.txt")
else: 
    system("python3 packages/main.py")
