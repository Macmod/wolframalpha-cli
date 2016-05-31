#!/usr/bin/env python
# coding: utf-8

import requests
import click
import yaml
import readline
from PIL import Image
from os import path, environ
from subprocess import call
from builtins import input
from lxml import etree
from lxml.html import soupparser
from colorama import init, Fore
from io import BytesIO
init()

try:
    from urllib.request import quote
except ImportError:
    from urllib2 import quote


class _Fore():
    def __init__(self, colors):
        self.colors = colors
        self.fallback = (not self.colors['pod'] in dir(Fore) or
                         not self.colors['subpod'] in dir(Fore))

    def pod(self, text):
        if not self.fallback:
            return getattr(Fore, self.colors['pod']) + text + Fore.RESET
        else:
            return '** ' + text + ' **'

    def subpod(self, text):
        if not self.fallback:
            return getattr(Fore, self.colors['subpod']) + text + Fore.RESET
        else:
            return '(' + text + ')'


def content(tag):
    if tag is not None and tag.text is not None:
        return tag.text + ''.join(etree.tostring(e, encoding=str) for e in tag)
    else:
        return ''


class WolframCli:
    def __init__(self, api_key, fetch_pics, show_url, colors):
        self.api_key = api_key
        self.fetch_pics = fetch_pics
        self.show_url = show_url
        self.fore = _Fore(colors)

    def send_query(self, query):
        raw_url = u'http://api.wolframalpha.com/v2/query?input={q}'\
                  '&appid={API_KEY}'.format(
                    API_KEY=self.api_key, q=quote(query)
                  )

        url = raw_url
        if not self.fetch_pics:
            url += u'&format=plaintext'

        resp = requests.get(url)
        return resp

    def output(self, query):
        if self.show_url:
            wolfram = 'http://www.wolframalpha.com/input/?i='
            url = '\n(' + wolfram + quote(query) + ')'
        else:
            url = ''

        try:
            resp = self.send_query(query)
            root = etree.fromstring(resp.content)
            out = self.parse_etree(root)

            return '\n\n'.join(out) + url + '\n'
        except Exception as e:
            return repr(e)

    def parse_subpods(self, pod):
        subpods = pod.findall('.//subpod')
        sub_out = []
        if len(subpods) >= 1:
            for subpod in subpods:
                podstr = ''
                subtitle = subpod.get('title', '')
                plaintext = content(subpod.find('plaintext'))
                if self.fetch_pics:
                    pics = subpod.findall('img')
                    for pic in pics:
                        pic_req = requests.get(pic.get('src'))
                        Image.open(BytesIO(pic_req.content)).show()

                if plaintext:
                    if subtitle:
                        podstr = self.fore.subpod(subtitle) + '\n'
                    podstr += plaintext

                    clean_podstr = soupparser.unescape(podstr.strip())
                    sub_out.append(clean_podstr)

            return sub_out
        else:
            return None

    def parse_etree(self, root):
        out = []
        success = root.get('success')

        if success == 'true':
            for pod in root.iterfind('.//pod'):
                title = pod.get('title')

                subpods = self.parse_subpods(pod)
                if subpods is not None:
                    section = [self.fore.pod(title)]
                    section += subpods
                    out.append('\n'.join(section))
        else:
            error = root.find('error')
            if error is not None:
                out.append('Error #' + content(error.find('code')) +
                           ': ' + content(error.find('msg')))
            else:
                out.append('No result.')

        return out


@click.command()
@click.option('-q', help='Perform a single query.')
@click.option('--repl', 'mode', flag_value='repl',
              default=True, help='Read, eval, print, loop mode.')
@click.option('--config', 'mode', flag_value='config',
              help='Open config file.')
def main(mode, q):
    """Simple command-line interface to run queries on WolframAlpha."""
    config_path = path.join(
        path.dirname(path.abspath(__file__)),
        'data', 'config.yaml'
    )

    config_file = None
    try:
        config_file = open(config_path, 'r+')
        config = yaml.safe_load(config_file)
        if not config['api_key']:
            print('It seems you don\'t have an API key yet.\nGet one at '
                  'https://developer.wolframalpha.com/portal/apisignup.html')
            config['api_key'] = input('WolframAlpha API Key: ')

            config_file.seek(0)
            config_file.write(yaml.dump(config, indent=4))
            config_file.truncate()
    finally:
        if config_file is not None:
            config_file.close()

    wc = WolframCli(
        config['api_key'],
        config['fetch_pics'],
        config['show_url'],
        config['colors']
    )

    if q:
        print(wc.output(q))
    elif mode == 'repl':
        while 1:
            query = input('>> ')
            print(wc.output(query))
    elif mode == 'config':
        call([environ.get('EDITOR', 'vim'), config_path])

if __name__ == '__main__':
    main()
