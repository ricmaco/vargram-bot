#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from emoji import emojize

def __(string):
  """Emojize a text, wrapping ``use_aliases``.

  Args:
    string (str): string to emojize.

  Returns:
    An emojized string.

  """
  return emojize(string, use_aliases=True)

START = \
"""
:penguin: Ciao! Sono il bot del [LinuxVar](http://www.linuxvar.it), il LUG \
della provincia di Varese.
Digita /help per sapere la lista dei comandi e chiedimi qualcosa.
""".strip()
START = __(START)

RECAP = \
"""
:penguin: Questo mese abbiamo inviato <b>{emails} messaggi</b> all'interno di \
<b>{threads} thread</b>.

Abbiamo parlato di:
{recap}
""".strip()
RECAP = __(RECAP)

HELP = \
"""
/start mostra il messaggio di benvenuto.
/help mostra questo messaggio di aiuto.
/author fornisce qualche notizia sull'autore.
/recap fornisce un riassunto dell'attività di questo mese in mailing list.
/ml <nome>, <oggetto>, <testo> invia una mail in mailing list con queste \
caratteristiche (nel campo <testo> usa \\\\ per andare a capo).
/rlinux mostra gli ultimi dieci post da \
[/r/linux](https://www.reddit.com/r/linux).
/runixporn mostra gli ultimi dieci post da \
[/r/unixporn](https://www.reddit.com/r/unixporn).
/phoronix mostra gli ultimi dieci articoli di \
[Phoronix](http://www.phoronix.com).
""".strip()
HELP = __(HELP)

AUTHOR = \
"""
:penguin: VarGram Bot - versione {version}
Creato da [Riccardo Macoratti](https://ricma.co) :moyai:
""".strip()
AUTHOR = __(AUTHOR)

UNKNOWN = \
"""
:sweat_smile: Scusa, non credo di aver capito il comando, prova a riscriverlo \
meglio.
""".strip()
UNKNOWN = __(UNKNOWN)

ML = \
"""
:wink: Uso: /ml <nome>, <oggetto>, <testo>
""".strip()
ML = __(ML)

MAIL = \
"""
:heavy_check_mark: L'email _{subject}_ di *{name}* è stata inviata con \
successo.
""".strip()
MAIL = __(MAIL)

REDDIT = \
"""
:penguin: Ecco gli ultimi post di \
<a href="https://www.reddit.com/r/{name}">/r/{name}</a>:

{subreddit}
""".strip()
REDDIT = __(REDDIT)

FEED = \
"""
:penguin: Ecco gli ultimi articoli di <a href="{url}">{name}</a>:

{feed}
""".strip()
FEED = __(FEED)
