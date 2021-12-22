import time
import requests
import json
import os
import random
import string
import pprint

if __name__ == '__main__':
    page = 100
    keyword = input('输入关键字')
    keyword_true = keyword
    for m in range(1, page):
        if 0 == (m % 2):
            continue
            keyword = random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
        else:
            keyword = keyword_true
        print(keyword)
