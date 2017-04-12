#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import timedelta

import yaml, emoji
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters,
  Job
)

from vargram_bot.version import VERSION
from vargram_bot.strings import (
  START,
  HELP,
  RECAP,
  AUTHOR,
  MAIL,
  ML,
  UNKNOWN
)

class TelegramBot:
  """Instantiate a telegram bot to communicate in the group.

  The bot is characterized by a token, which acts as access control.

  Attributes
    updater (telegram.update.Update): telegram bot updater.
    dispatcher (telegram.dispatcher.Dispatcher): telegram bot dispatcher.
    job_queue (telegram.ext.JobQueue): telegram bot job queue.

  """

  def __init__(self, token):
    """Create a bot with an access token.

    Args:
      token (str): token give by BotFather.

    """
    self.updater = Updater(token)
    self.dispatcher = self.updater.dispatcher
    self.job_queue = self.updater.job_queue

  def initialize(self, recap_func, group, ml_data):
    """Initializes bot with all functions to answer user commands.

    Args:
      recap_func (function): function that returns a ``Thread`` that contains all
          emails partitioned by thread.
      group (dict): group of admins who can interact with bot and to send recap
          updates.
      ml_data (dict): dictionary containing stmp address, mailing list address
          and subscripted mail address and password.

    """

    def start(bot, update):
      update.message.reply_text(parse_mode='Markdown', text=START)

    def recap(bot, update_or_job):
      threads = recap_func()
      _recap = RECAP.format(
        emails = threads.count_mails(),
        threads = threads.count_threads(),
        recap = threads.markdown()
      )

      if not isinstance(update_or_job, Job):
        update_or_job.message.reply_text(parse_mode='Markdown', text=_recap)
      else:
        bot.sendMessage(chat_id=group_id, text=_recap, parse_mode='Markdown')

    def help(bot, update):
      update.message.reply_text(parse_mode='Markdown', text=HELP)

    def author(bot, update):
      _author = AUTHOR.format(version=VERSION)
      update.message.reply_text(parse_mode='Markdown', text=_author)

    def ml(bot, update, args):
      if len(args) < 3:
        update.message.reply_text(parse_mode='Markdown', text=ML)
      else:
        split_args = ' '.join(args).split(',')
        if len(split_args) < 3:
          update.message.reply_text(parse_mode='Markdown', text=ML)
        else:
          tmp = ','.join(split_args[2:]).strip()
          EmailThread(
            bot,
            update.message.chat_id,
            {
              'name': split_args[0].strip(),
              'subject': split_args[1].strip(),
              'text': re.sub('[\\\\]+\s+', '\n', tmp)
            },
            ml_data
          ).start()

    def unknown(bot, update):
      update.message.reply_text(parse_mode='Markdown', text=UNKNOWN)

    start_handler = CommandHandler('start', start)
    self.dispatcher.add_handler(start_handler)

    recap_handler = CommandHandler('recap', recap)
    self.dispatcher.add_handler(recap_handler)

    help_handler = CommandHandler('help', help)
    self.dispatcher.add_handler(help_handler)

    author_handler = CommandHandler('author', author)
    self.dispatcher.add_handler(author_handler)

    ml_handler = CommandHandler('ml', ml, pass_args=True)
    self.dispatcher.add_handler(ml_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    self.dispatcher.add_handler(unknown_handler)

    # queue job every monday
    job = Job(recap, timedelta(days=1), repeat=True, days=(0,))
    self.job_queue.put(job)

  def start(self, webhook=False, port=8888):
    """Start bot with either polling or webhook.

    First start bot with either polling method, for testing, or with a http
    internal web server which will be externally proxied to https.
    Then put updater into idle, waiting for stop signal.

    Args:
      webhook (str): address for webhook server.
      port (int): port where to start internal server.

    """
    if webhook:
      self.updater.start_webhook(port=port, bootstrap_retries=3,
          webhook_url=webhook)
    else:
      self.updater.start_polling()
    self.updater.idle()

import threading, smtplib
from email.mime.text import MIMEText

class EmailThread(threading.Thread):

  def __init__(self, bot, chat_id, email_data, ml_data):
    threading.Thread.__init__(self)
    self.bot = bot
    self.chat_id = chat_id
    self._from = ml_data['from']
    self.to = ml_data['to']
    self.smtp_serv = ml_data['server']
    self.smtp_port = ml_data['port']
    self.smtp_pass = ml_data['password']
    self.name = email_data['name']
    self.subject = email_data['subject']
    self.text = email_data['text']

  def run(self):
    # compose message
    msg = MIMEText(self.text)
    msg['Subject'] = '[Gruppo Telegram] {}'.format(self.subject)
    msg['From'] = '{} <{}>'.format(self.name, self._from)
    msg['To'] = self.to

    # authenticate to smtp
    serv = smtplib.SMTP(self.smtp_serv, self.smtp_port)
    serv.ehlo()
    serv.starttls()
    serv.ehlo()
    serv.login(self._from, self.smtp_pass)

    # send message
    serv.send_message(msg)

    # write confirmation to bot
    self.bot.sendMessage(chat_id=self.chat_id, parse_mode='Markdown',
        text= MAIL.format(subject=self.subject, name=self.name))
