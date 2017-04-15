# VarGram Bot
This is the official Telegram bot for the LinuxVar LUG.

## Dependencies
There are some common available dependencies to download (which are automatically installed by setup utility), but where possible, the standard library is used.

- `Python >= 3.6`
- `python-telegram-bot >= 5.3.0`
- `lxml >= 3.7.3`
- `PyYAML >= 3.12`
- `requests >= 2.13.0`
- `emoji >= 0.4.5`

## Installation
To install the software execute the following procedure.

1. Clone repository to your hard drive.
```shell
$ git clone https://github.com/imko92/vargram-bot.git
$ cd vargram-bot
```
2. Install software with setup utility.
```shell
$ python3 setup.py install
```
3. Copy configuration to `/etc/vargram.yml` and edit it.
```shell
# cp docs/config.yml /etc/vargram.yml
# vi /etc/vargram.yml
```

4. Start VarGram Bot.
```bash
$ vargram
```

5. Optionally you can enable ``vargram`` to start at boot or start it using
   Systemd commands.
```
# systemctl enable vargram
# systemctl start vargram
```

## Tip and tricks
The default example config looks like this.
```yaml
# botfather token
token: <bot token as give by BotFather>
# mailman url to parse for getting email info
mailman-url: http://ml.linuxvar.it/pipermail/talking/$Y-$M/date.html
# wheter to use a webserver or polling
webhook: null
webhook-port: null
heroku-url: https://vargram-bot.herokuapp.com/
# smtp parameters
smtp-address: smtp.gmail.com
smtp-port: 587
smtp-user: <user-email>
smtp-pass: <user-password>
smtp-to: talking@ml.linuxvar.it
```

In order to populate `token` you need to create a bot asking @BotFather on Telegram as describer [here](https://core.telegram.org/bots).

## License
This work is provided under [MIT License](https://opensource.org/licenses/MIT).
Copyright holder is [Riccardo Macoratti](mailto:r.macoratti@gmx.co.uk).
