#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        subject: email subject to sanitize

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

  def __repr__(self):
    return ', '.join((self.subject, self.author, self.url))

  def __str__(self):
    return 'Subject: {}\nAuthor: {}\nURL: {}'.format(self.subject, self.author,
        self.url)


class Thread:
  """Represents a set of emails partitioned by subject.

  Attributes:

  
  """

  def __init__(self):
    self.thread = {}

  def append(self, email):
    pass
