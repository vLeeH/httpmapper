#!/usr/bin/env python3

# -*- coding utf-8 -*-
from os import system
try:
    import requests
    import http.cookiejar
except ImportError: 
    system("python -m pip install -r requirements.txt")
else: 
    system("python packages/main.py")
