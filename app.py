import os
import random
import sys
from argparse import ArgumentParser

import pyjokes
from flask import Flask, request, abort
from googletrans import Translator
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage)
from pyjokes.jokes_en import jokes_en

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
translator = Translator()


def russian_roulette(event):
    fatal_bullet = random.randint(0, 5)

    message = ''

    if fatal_bullet == 0:
        message += '(X)'
    else:
        message += '(O)'

    for x in range(5):
        if fatal_bullet == x + 1:
            message += ' X'
        else:
            message += ' O'

    if fatal_bullet == 0:
        message += ' Bang your dead!!!'

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=message)
        ]
    )


def pick_option(opt):
    res = opt.split(' ')
    if len(res) > 1:
        return res[random.randint(0, len(res) - 1)]
    else:
        return None


def bot_help(event):
    help_message = """*** SamBot Commands ***
sambot hello <name>
sambot ead <name>
sambot praise <name>
sambot scold <name>
sambot nuke
sambot russian_roulette
sambot decide_for_us <option1> <option2> <option#>
sambot tell_me_a_joke <neutral|chuck|all>
sambot translate <fromlang> <tolang> <content>
"""

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=help_message)
        ]
    )


def command_splitter(message):
    result = message.split(' ')

    if len(result):
        if len(result) >= 3:
            return [result[0].lower(), result[1].lower(), ' '.join(result[2:])]
        elif len(result) == 2:
            return [result[0].lower(), result[1].lower(), None]
        else:
            return [result[0].lower(), None, None]
    else:
        return [None, None, None]


@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'POST':

        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK', 200
    else:
        # We implement GET to allow Line to verify the endpoint
        return '', 200


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    service, command, rest = command_splitter(event.message.text)

    if not service == 'sambot':
        language = translator.detect(event.message.text).lang
        if language != 'en':
            translation = translator.translate(event.message.text, src=language).text

            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=f'Translation (lang: {language}): {translation}')
                ]
            )
        return

    if command:
        if command == 'nuke':
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='boom') for _ in range(5)]
            )

        if command == 'hello':
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=f'Gday {rest}')
                ]
            )

        if command == 'praise':
            if not rest:
                rest = 'Sam'
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=f'{rest} is awesome at everything')
                ]
            )

        if command == 'ead':
            if 'sambot' in rest.lower():
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'Yea Nah, You Eat a Dick')
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'Eat a Dick {rest}')
                    ]
                )

        if command == 'russian_roulette':
            russian_roulette(event)

        if command == 'tell_me_a_joke':
            if rest in jokes_en:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=pyjokes.get_joke(category=rest))
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=pyjokes.get_joke())
                    ]
                )

        if command == 'decide_for_us':
            option = pick_option(rest)

            if option:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'Lets go with {option}')
                    ]
                )

        if command == 'scold':
            if 'sambot' in rest.lower():
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'Yea Nah, Your worthless')
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'{rest} Your Worthless')
                    ]
                )

        if command == 'translate':
            from_lang, to_lang, content = rest.split(" ", 2)
            translation = translator.translate(content, src=from_lang, dest=to_lang).text

            try:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'Translation (From:{from_lang} To: {to_lang}): {translation}')
                    ]
                )
            except ValueError:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=f'Invalid Usage, Expected sambot translate fromlang tolang content')
                    ]
                )

    else:
        bot_help(event)


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
