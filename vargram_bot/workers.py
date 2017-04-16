#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading, smtplib, html
from os import path
from email.mime.text import MIMEText

import requests, feedparser
from lxml import html

from vargram_bot.version import VERSION
from vargram_bot.model import (
  Mail,
  Threads,
  Post,
  Subreddit,
  Article,
  Feed
)
from vargram_bot.exceptions import (
  ParseException,
  InternetException
)
from vargram_bot.strings import (
  RECAP,
  MAIL,
  REDDIT,
  FEED
)

class MLWorker(threading.Thread):

  def __init__(self, bot, update, url):
    threading.Thread.__init__(self)
    self.bot = bot
    self.update = update
    self.url = url

  def __parse_page(self, url):
    try:
      page = requests.get(url)
      tree = html.fromstring(page.content)

      mails = Threads()
      for x, ul in enumerate(tree.iter('ul')):
        # the only information provided: the second ul is the one of mails
        if x == 1:
          for mail in ul.iter('li'):
            subject = mail[0].text_content().strip()
            url = path.join(path.dirname(url), mail[0].get('href'))
            author = mail[2].text_content().strip()
            mails.append(Mail(subject, author, url))

      return mails
    except:
      raise ParseException(f'Cannot parse <{url}>')

  def run(self):
    threads = self.__parse_page(self.url)
    _recap = RECAP.format(
      emails = threads.count_mails(),
      threads = threads.count_threads(),
      recap = threads.html()
    )
    self.update.message.reply_text(parse_mode='HTML',
        disable_web_page_preview=True, text=_recap)


class EmailWorker(threading.Thread):

  def __init__(self, bot, update, email_data, ml_data):
    threading.Thread.__init__(self)
    self.bot = bot
    self.update = update
    self._from = ml_data['from']
    self.to = ml_data['to']
    self.smtp = ml_data
    self.name = email_data['name']
    self.subject = email_data['subject']
    self.text = email_data['text']

  def __sendmail(self, smtp, subject, from_name, from_mail, to, text):
    # smtp server parameters
    addr = smtp['server']
    port = smtp['port']
    passw = smtp['password']
    
    # compose message
    msg = MIMEText(text)
    msg['Subject'] = '[Gruppo Telegram] {}'.format(subject)
    msg['From'] = '{} <{}>'.format(from_name, from_mail)
    msg['To'] = to

    # authenticate to smtp
    serv = smtplib.SMTP(addr, port)
    serv.ehlo()
    serv.starttls()
    serv.ehlo()
    serv.login(from_mail, passw)

    # send message
    serv.send_message(msg)


  def run(self):
    # send mail
    self.__sendmail(self.smtp, self.subject, self.name, self._from, self.to,
        self.text)

    # write confirmation to bot
    self.update.message.reply_text(parse_mode='Markdown', 
        text=MAIL.format(subject=self.subject, name=self.name))

class RedditWorker(threading.Thread):
  
  def __init__(self, bot, update, subreddit):
    threading.Thread.__init__(self)
    self.bot = bot
    self.update = update
    self.subreddit = subreddit

  def __parse_subreddit(self, subreddit):
    URL = f'https://www.reddit.com/r/{subreddit}/top/.json?limit=10&raw_json=1'
    try:
      json = requests.get(
        URL,
        headers = {'User-agent': 'VarGram Bot {VERSION}'}
      ).json()
      sub = Subreddit(subreddit)
      for el in json['data']['children']:
        post = el['data']
        if post['is_self']:
          sub.append(Post(post['title'], post['url'], True))
        else:
          sub.append(Post(post['title'], post['url'], False, post['permalink']))
      return sub
    except:
      raise InternetException(f'Cannot retrieve data from /r/{subreddit}')

  def run(self):
    subreddit = self.__parse_subreddit(self.subreddit)

    _reddit = REDDIT.format(
      name=subreddit.name,
      subreddit=subreddit.html()
    )
    self.update.message.reply_text(parse_mode='HTML',
        disable_web_page_preview=True,
        text=_reddit)

class RSSWorker(threading.Thread):

  def __init__(self, bot, update, url):
    threading.Thread.__init__(self)
    self.bot = bot
    self.update = update
    self.url = url

  def __parse_rss(self, url):
    try:
      parsed = feedparser.parse(url)
      feed = Feed(parsed['feed']['title'])
      for el in parsed['items'][:10]:
        feed.append(Article(
          el['title'],
          el['description'],
          el['link'],
          el['published_parsed']
        ))
      return feed
    except:
      raise ParseException(f'Cannot parse feed at <{url}>')
    
  def run(self):
    feed = self.__parse_rss(self.url)

    _feed_text = FEED.format(
      name = feed.title,
      url = self.url,
      feed = feed.html()
    )
    self.update.message.reply_text(parse_mode='HTML',
        disable_web_page_preview=True,
        text=_feed_text)
