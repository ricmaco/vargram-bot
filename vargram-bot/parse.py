#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

import requests
from lxml import html

from model import Mail, Threads
from exceptions import ParseException

def parse_page(page_url):
  try:
    page = requests.get(page_url)
    tree = html.fromstring(page.content)

    mails = Threads()
    for x, ul in enumerate(tree.iter('ul')):
      # the only information provided: the second ul is the one of mails
      if x == 1:
        for mail in ul.iter('li'):
          subject = mail[0].text_content().strip()
          url = path.join(path.dirname(page_url), mail[0].get('href'))
          author = mail[2].text_content().strip()
          mails.append(Mail(subject, author, url))
    
    return mails
  except:
    raise ParseException('Cannot parse <{}>'.format(page_url))
