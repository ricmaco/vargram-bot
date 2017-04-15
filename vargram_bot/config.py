#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

import yaml

from vargram_bot.exceptions import ConfigException

"""Config loader module, which act as interface for raw PyYAML.

Every filename is ``filenames`` is checked to see if it exists.
It is then opened and config is read a made available to user.

Attributes:
    filenames (tuple): tuple of possible filenames to check against.
    config (dict): dictionary resulting from reading config.

"""

config = {
  'token': None,
  'mailman-url': 'http://ml.linuxvar.it/pipermail/talking/$Y-$M/date.html',
  'webhook': False,
  'webhook-domain': 'https://example.com/',
  'webhook-path': 'vargram',
  'webhook-port': 8443,
  'webhook-key': '/etc/ssl/private.key',
  'webhook-cert': '/etc/ssl/cert.pem',
  'smtp-address': 'smtp.gmail.com',
  'smtp-port': 587,
  'smtp-user': None,
  'smtp-pass': None,
  'smtp-to': 'talking@ml.linuxvar.it'
}

filenames = (
  'config.yml',
  '/etc/vargram.yml'
)

try:
  for f in filenames:
    if path.isfile(f):
      user_config = yaml.safe_load(open(f, 'r'))
      config.update(user_config)
  if not config:
    raise ConfigException('Cannot find a suitable config file')
except:
  raise ConfigException('Cannot find a suitable config file')
