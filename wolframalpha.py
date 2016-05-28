#!/usr/bin/env python
# coding: utf-8

import requests
import sys
import re
import os
from HTMLParser import HTMLParser
from urllib2 import quote
from builtins import input
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
        parser = HTMLParser()
        title = parser.unescape("".join(title).strip())
        print(Fore.GREEN + title + Fore.RESET).encode(
            sys.stdout.encoding, 'replace'
        )

        for inner in re.findall(r'<plaintext>(.*?)</plaintext>', pod, re.S):
            print(parser.unescape(inner.strip()).encode(
                sys.stdout.encoding, 'replace')
            )

        print('')

if __name__ == '__main__':
    main()
