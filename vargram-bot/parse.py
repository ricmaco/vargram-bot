#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

import requests
from lxml import html

from exceptions import ParseException

def parse_page(page_url):
  try:
    page = requests.get(page_url)
    tree = html.fromstring(page.content)

    mails = []
    for x, ul in enumerate(tree.iter('ul')):
      # the only information provided: the second ul is the one of mails
      if x == 1:
        for mail in ul.iter('li'):
          subject = mail[0].text_content().strip()
          url = path.join(path.dirname(page_url), mail[0].get('href'))
          author = mail[2].text_content().strip()
          mails.append((subject, url, author))
    
    return mails
  except:
    raise ParseException('Cannot parse <{}>'.format(page_url))

if __name__ == '__main__':
  page = 'http://ml.linuxvar.it/pipermail/talking/2017-April/date.html'
  res = parse_page(page)
  print(res)
