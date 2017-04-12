#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vargram_bot.util import capitalize_no_sym as capitalize

from emoji import emojize

class Mail:
  """Class representing an email.

  Email should be characterized by a subject, an author and a reference url in
  the mailing list web interface.
  """
  
  def __init__(self, subject, author, url):
    """Creates a mail with a subject, author and a reference url.

    The url passed is raw as received from the constructor, that is no check if
    a real url is inserted.
    """
    self.__subject = self.__sanitize_subject(subject)
    self.__author = author
    self.__url = url

  def __sanitize_subject(self, subject):
    """Removes mailman mailing list tag from subject if present.

    Args:
        subject (str): email subject to sanitize

    Returns:
        Sanitized subject with only relevant text.
    
    """
    try:
      return subject[subject.index(']')+2:]
    except:
      return subject

  @property
  def subject(self):
    """Email subject
    
    """
    return self.__subject

  @property
  def author(self):
    """Email author

    """
    return self.__author

  @property
  def url(self):
    """Email url

    """
    return self.__url

  def __eq__(self, other):
    """Equality is based on url (which contains email id for mailing list)

    Args:
        other (Mail): email object to compare with self

    Returns:
        True if this email url is equal to other email url, else False

    """
    return self.url == other.url

  def __repr__(self):
    return '{}({})'.format(self.__class__.__name__,
        ', '.join((self.subject, self.author, self.url)))

  def __str__(self):
    return 'Subject: {}\nAuthor: {}\nURL: {}'.format(self.subject, self.author,
        self.url)


class Threads:
  """Represents a set of emails partitioned by subject.

  Every list of emails (characterized by a single subject) is stored togheter,
  with subject as a key.
  An email is added to ``Threads`` if it does not collide with other already
  added emails.

  Attributes:
      thread (dict): a dictionary to contain the various list of email separated
      by subject.
  
  """

  def __init__(self):
    """Create a fresh, empty thread container.

    """
    self.thread = {}

  def append(self, email):
    """Add an email to thread.

    Email is added only if it does not collide with already present email.
    If provided email subject does not exist it is created and inserted into
    thread.

    Args:
        email (Mail): email to add.

    Returns:
        True is insertion is successful, else otherwise.
    """
    if email.subject in self.thread:
      emails = self.thread[email.subject]
      if email in emails:
        return False
    else:
      emails = []
      self.thread[email.subject] = emails

    emails.append(email)
    return True
  
  def count_threads(self):
    """Count complessive number of threads.

    Returns:
      Number of threads.
    
    """
    return len(self.thread)

  def count_mails(self):
    """Count complessive number of emails present.

    Returns:
        Number of present emails.
    
    """
    total = 0
    for k, v in self.thread.items():
      total += len(v)
    return total

  def __repr__(self):
    return repr(self.thread)

  def __str__(self):
    s = ''
    for k, v in reversed(list(self.thread.items())):
      s += '{}:\n'.format(k)
      for el in reversed(v):
        s += '\t{} - <{}>\n'.format(el.author, el.url)
      s += '\n'
    return s

  def markdown(self):
    """Like ``str()`` but with added Markdown formatting and (if available)
    emojis.

    Returns:
        A string representing this ``Threads``, formatted in Markdown (and
        optionally emojis).

    """
    try:
      from emoji import emojize
      dash = emojize(':point_right:', use_aliases=True)
    except ImportError:
      dash = '-'

    s = ''
    for k, v in reversed(list(self.thread.items())):
      s += '{} *{}*\n'.format(dash, capitalize(k))
      for el in reversed(v):
        s += '    [{}]({})\n'.format(el.author, el.url)
    return s
