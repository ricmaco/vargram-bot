#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from vargram_bot.version import VERSION

setup(
    name = 'vargram-bot',
    version = VERSION,
    description = 'The official Telegram bot for the LinuxVar LUG.',
    url = 'https://github.com/imko92/vargram-bot',
    author = 'Riccardo Macoratti',
    author_email = 'r.macoratti@gmx.co.uk',
    license = 'MIT',
    packages = [
      'vargram_bot'
    ],
    install_requires=[
      'python-telegram-bot',
      'lxml',
      'PyYAML',
      'requests',
      'emoji'
    ],
    zip_safe = False,
    scripts = [
      'scripts/vargram'
    ],
    data_files = [
      ('/etc/systemd/system', ['scripts/vargram.service'])
    ]
)
