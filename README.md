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

## Tip and tricks
The default example config looks like this.
```yaml
# botfather token
token: <bot token as give by BotFather>
# group of people who can interact with bot
group-name: <name of group of admins>
group-id: <group id where to send updates>
# mailman url to parse for getting email info
mailman-url: http://ml.linuxvar.it/pipermail/talking/$Y-$M/date.html
# wheter to use a webserver or polling
webhook-url: False
webhook-port: 8888
# smtp parameters
smtp-address: smtp.gmail.com
smtp-port: 587
smtp-user: <user-email>
smtp-pass: <user-password>
smtp-to: talking@ml.linuxvar.it
```

In order to populate `token` you need to create a bot asking @BotFather on Telegram as describer [here](https://core.telegram.org/bots).

To obtain your group id, you need to follow this procedure.

1. Send a message to the bot, it can be anything.
2. Head your web browser to this address `https://api.telegram.org/bot<TOKEN>/getUpdates`, where `<TOKEN>` is the access token that BotFather gave you.
3. Look at `update.message.chat.id` and copy over that number (don't worry if it is negative, it is completely normal).

## TODO
At this moment, the WebHook feature may not work (as in *may not work at all*).

## License
This work is provided under [MIT License](https://opensource.org/licenses/MIT).
Copyright holder is [Riccardo Macoratti](mailto:r.macoratti@gmx.co.uk).