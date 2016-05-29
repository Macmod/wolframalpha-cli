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
        BLUE = '** '
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

    try:
        resp = requests.get(url)
    except Exception as e:
        resp = repr(e)

    return resp


def content(tag):
    if tag is not None and tag.text is not None:
        return tag.text + ''.join(etree.tostring(e, encoding=str) for e in tag)
    else:
        return ''


def output(query):
    resp = sendQuery(query)
    root = etree.fromstring(resp.content)
    out = []

    for pod in root.iterfind('.//pod'):
        title = pod.get('title')
        colored_title = Fore.GREEN + title + Fore.RESET

        subpods = pod.findall('.//subpod')
        if len(subpods) >= 1:
            sub_out = [colored_title]
            for subpod in subpods:
                subtitle = subpod.get('title', '')
                colored_subtitle = Fore.BLUE + subtitle + Fore.RESET
                plaintext = content(subpod.find('plaintext'))

                if plaintext:
                    podstr = colored_subtitle + '\n' if subtitle else ''
                    podstr += plaintext

                    clean_podstr = soupparser.unescape(podstr.strip())
                    sub_out.append(clean_podstr)

            if len(sub_out) > 1:
                out.append('\n'.join(sub_out))

    url = '(http://www.wolframalpha.com/input/?i=' + quote(query) + ')'
    return '\n\n'.join(out) + '\n' + url + '\n'


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
