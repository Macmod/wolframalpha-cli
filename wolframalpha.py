#!/usr/bin/env python
# coding: utf-8

import requests
import sys
import re
import os
from builtins import input
from lxml import etree
from lxml.html import soupparser

try:
    from urllib.request import quote
except ImportError:
    from urllib2 import quote
try:
    from colorama import init, Fore
    init()
except Exception as e:
    class Fore():
        GREEN = "** "
        RESET = " **"
try:
    with open(os.path.expanduser("~/.wolfram_key"), "r") as _file:
        wolfram_alpha_key = "".join(_file.readlines())
except Exception as e:
    print("""Invalid API key!
Get one at https://developer.wolframalpha.com/portal/apisignup.html""")
    api_key = input('Enter your WolframAlpha API key: ')
    wolfram_alpha_key = api_key
    with open(os.path.expanduser("~/.wolfram_key"), "w") as _file:
        _file.writelines(api_key)

__version__ = '0.3'


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input('Enter query: ')

    url = u'http://api.wolframalpha.com/v2/query?input={q}'\
          '&appid={API_KEY}&format=plaintext'.format(
            API_KEY=wolfram_alpha_key, q=quote(query)
          )

    resp = requests.get(url)

    for pod in re.findall(r'<pod.+?>.+?</pod>', resp.text, re.S):
        title = re.findall(r'<pod.+?title=[\'"](.+?)[\'"].*>', pod, re.S)
        parser = soupparser
        title = parser.unescape("".join(title).strip())
        print(Fore.GREEN + title + Fore.RESET)

        for inner in re.findall(r'<plaintext>(.*?)</plaintext>', pod, re.S):
            print(parser.unescape(inner.strip()))
        print('')

if __name__ == '__main__':
    main()
