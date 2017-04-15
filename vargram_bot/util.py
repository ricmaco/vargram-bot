#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string

def capitalize_no_sym(text):
  try:
    start = text.rindex(']') + 1
  except:
    start = 0

  return '{}{}{}'.format(
    text[:start].strip(),
    '' if start == 0 else ' ',
    text[start:].strip().capitalize()
  )
