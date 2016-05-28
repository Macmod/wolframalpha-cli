#!/usr/bin/env python
# coding: utf-8

import requests
import sys
import os
import click
import readline
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
        GREEN = '** '
        RESET = ' **'
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


def sendQuery(query):
    url = u'http://api.wolframalpha.com/v2/query?input={q}'\
          '&appid={API_KEY}&format=plaintext'.format(
            API_KEY=wolfram_alpha_key, q=quote(query)
          )

    return requests.get(url)


def content(tag):
    return tag.text + ''.join(etree.tostring(e, encoding=str) for e in tag)


def output(query):
    resp = sendQuery(query)
    root = etree.fromstring(resp.content)
    out = []

    for pod in root.iterfind('.//pod'):
        title = pod.get('title')
        parser = soupparser

        sub_out = [Fore.GREEN + title + Fore.RESET]
        for inner in pod.iterfind('.//plaintext'):
            podstr = content(inner)

            clean_podstr = parser.unescape(podstr.strip())
            if clean_podstr:
                sub_out.append(clean_podstr)

        out.append('\n'.join(sub_out))

    return '\n\n'.join(out) + '\n'


@click.command()
@click.option('-q', help='Perform standalone query.')
def main(q):
    """Simple command-line interface to run queries on WolframAlpha."""
    if len(sys.argv) > 1:
        print(output(q))
    else:
        while 1:
            query = input('>> ')
            print(output(query))

if __name__ == '__main__':
    main()
