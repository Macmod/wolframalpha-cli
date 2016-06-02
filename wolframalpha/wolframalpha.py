#!/usr/bin/env python
# coding: utf-8

import requests
import click
import yaml
import readline  # NOQA
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
        self.last_pics = []

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

    def show_picture(self, pic):
        pic_req = requests.get(pic.get('src'))
        Image.open(BytesIO(pic_req.content)).show()

    def output(self, query):
        if self.show_url:
            wolfram = 'http://www.wolframalpha.com/input/?i='
            url = '\n(' + wolfram + quote(query) + ')'
        else:
            url = ''

        if query.startswith(':'):
            cmd = query.split(' ')
            if cmd[0] == ':p':
                if cmd[1].isdigit():
                    fp = int(cmd[1])
                    if fp > 0 and fp <= len(self.last_pics):
                        pic = self.last_pics[fp-1]
                        self.show_picture(pic)

                        return 'Done.'
                    else:
                        return 'Invalid picture.'
                else:
                    return 'NaN.'
            elif cmd[0] == ':allpics':
                for pic in self.last_pics:
                    self.show_picture(pic)

                return 'Done.'
            else:
                return 'Unknown command.'
        else:
            try:
                resp = self.send_query(query)
                root = etree.fromstring(resp.content)
                out = self.parse_etree(root)

                return '\n\n'.join(out) + url
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

                if plaintext:
                    if subtitle:
                        podstr = self.fore.subpod(subtitle) + '\n'
                    podstr += plaintext

                    clean_podstr = soupparser.unescape(podstr.strip())
                    sub_out.append(clean_podstr)
                elif self.fetch_pics:
                    pics = subpod.findall('img')
                    self.last_pics += pics
                    sub_out.append('(Type :p ' + str(len(self.last_pics)) +
                                   ' to see picture)')

            return sub_out if sub_out else None
        else:
            return None

    def parse_etree(self, root):
        self.last_pics = []

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
@click.option('--set-key', help='Set API key.')
@click.option('--repl', 'mode', flag_value='repl',
              default=True, help='Read, eval, print, loop mode.')
@click.option('--config', 'mode', flag_value='config',
              help='Open config file.')
def main(mode, q, set_key):
    """Simple command-line interface to run queries on WolframAlpha."""
    config_path = path.join(
        path.dirname(path.abspath(__file__)),
        'data', 'config.yaml'
    )

    config_file = None
    try:
        config_file = open(config_path, 'r')
        config = yaml.safe_load(config_file)
    finally:
        if config_file is not None:
            config_file.close()

    if set_key:
        key_path = path.expanduser(config['key_path'])
        key_file = open(key_path, 'w')

        key_file.write(set_key)
        key_file.truncate()
    elif mode == 'config':
        call([environ.get('EDITOR', 'vim'), config_path])
    else:
        key_file = None
        try:
            key_path = path.expanduser(config['key_path'])
            if not path.isfile(key_path):
                key_file = open(key_path, 'w')
                print('It seems you don\'t have an API key yet.')
                print('Get one at https://'
                      'developer.wolframalpha.com/portal/apisignup.html')
                api_key = input('WolframAlpha API Key: ')

                key_file.write(api_key)
                key_file.truncate()
            else:
                key_file = open(key_path, 'r')
                api_key = key_file.readline()
        finally:
            if key_file is not None:
                key_file.close()

        wc = WolframCli(
            api_key,
            config['fetch_pics'],
            config['show_url'],
            config['colors']
        )

        if q:
            print(wc.output(q) + '\n')
        elif mode == 'repl':
            while 1:
                query = input('>> ')
                print(wc.output(query) + '\n')

if __name__ == '__main__':
    main()
