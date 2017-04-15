#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
from datetime import timedelta

import yaml, emoji
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters
)
from telegram.error import (
  TelegramError,
  Unauthorized,
  BadRequest, 
  TimedOut,
  ChatMigrated,
  NetworkError
)

from vargram_bot.version import VERSION
from vargram_bot.strings import (
  START,
  HELP,
  AUTHOR,
  ML,
  UNKNOWN
)
from vargram_bot.workers import (
  MLWorker,
  EmailWorker,
  RedditWorker
)

class TelegramBot:
  """Instantiate a telegram bot to communicate in the group.

  The bot is characterized by a token, which acts as access control.

  Attributes:
      token (str): access token by BotFather.
      updater (telegram.update.Update): telegram bot updater.
      dispatcher (telegram.dispatcher.Dispatcher): telegram bot dispatcher.

  """

  def __init__(self, token):
    """Create a bot with an access token.

    Args:
      token (str): token give by BotFather.

    """
    self.token = token
    self.updater = Updater(token)
    self.dispatcher = self.updater.dispatcher

  def initialize(self, recap_url, ml_data):
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

    def recap(bot, update):
      MLWorker(
        bot,
        update,
        recap_url
      ).start()

    def help(bot, update):
      update.message.reply_text(parse_mode='Markdown',
          disable_web_page_preview=True, text=HELP)

    def author(bot, update):
      _author = AUTHOR.format(version=VERSION)
      update.message.reply_text(parse_mode='Markdown', text=_author)

    def ml(bot, update, args):
      split_args = ' '.join(args).split(',')
      if len(split_args) < 3:
        update.message.reply_text(parse_mode='Markdown', text=ML)
      else:
        tmp = ','.join(split_args[2:]).strip()
        EmailWorker(
          bot,
          update,
          {
            'name': split_args[0].strip(),
            'subject': split_args[1].strip(),
            'text': re.sub('[\\\\]+\s+', '\n', tmp)
          },
          ml_data
        ).start()

    def rlinux(bot, update):
      RedditWorker(
        bot,
        update,
        'linux'
      ).start()

    def unknown(bot, update):
      update.message.reply_text(parse_mode='Markdown', text=UNKNOWN)

    def error(bot, update, error):
      try:
        raise error
      except Unauthorized:
        pass
      except BadRequest:
        pass
      except TimedOut:
        pass
      except NetworkError:
        pass
      except ChatMigrated:
        pass
      except TelegramError:
        pass

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

    rlinux_handler = CommandHandler('rlinux', rlinux)
    self.dispatcher.add_handler(rlinux_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    self.dispatcher.add_handler(unknown_handler)

    self.dispatcher.add_error_handler(error)

  def start(self, webhook=None, port=None, heroku_url=None):
    """Start bot with either polling or webhook.

    First start bot with either polling method, for testing, or with a http
    internal web server which will be externally proxied to https.
    Then put updater into idle, waiting for stop signal.

    Args:
      webhook (str): address for webhook server.
      port (int): port where to start internal server.

    """
    # decide port based on precedence
    if webhook and (not port):
      port = int(os.environ.get('PORT', '5000'))

    if webhook:
      self.updater.start_webhook(
        listen = '0.0.0.0',
        port = port,
        url_path = self.token,
        bootstrap_retries = 3
      )
      self.updater.bot.setWebhook(heroku_url)
    else:
      self.updater.start_polling()
    self.updater.idle()
