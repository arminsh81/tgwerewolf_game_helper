from .methods import Chat

from . import terminal_beutify
import sys


stdout = sys.stdout
stderr = sys.stderr


def console_update(func):
    def wrapper(client, message):
        chat_id = message.chat.id
        terminal_beutify.add_group(chat_id)
        return func(client, message)
    return wrapper


@console_update
def detect_game_start(client, message):
    msg_id = message.message_id
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    user = message.from_user.id
    chat.join_time_pin(message)
    chat.add_new_game(msg_id, user)


@console_update
def detect_game_started(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.send_next_pin()
    chat.delete_join_link()


@console_update
def detect_game_started_message(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.first_list(message)
    chat.start_game(message)


@console_update
def detect_game_list(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.game_list(message)

@console_update
def detect_game_finished(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.game_finish(message)
    chat.game_finish_db(message)


@console_update
def detect_game_canceled(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.cancel_game(message)


@console_update
def grey_next(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.grey_next(message)


@console_update
def add_gp(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.add_gp(message)


@console_update
def define_message_as_mention(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.add_message_as_mention(message)


@console_update
def game_start_save_link(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.save_game_link(message)


@console_update
def afked_players(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.save_afk(message)


@console_update
def player_votes(client, message):
    chat_id = message.chat.id
    chat = Chat(client, chat_id)
    chat.save_vote(message)


def count_gaps(client, message):
    from . import apps, apps_free, bot, lab
    text = 'آمار تعداد دایالوگای هلپرا:/\n'
    all_dias = 0
    for app_ in apps + apps_free:
        try:
            app_name = app_.get_me()
            name = app_name.first_name
            if app_name.last_name:
                name += app_name.last_name
            count = app_.get_dialogs_count()
            all_dias += count
            text += f'[{name}](tg://user?id={app_name.id}) ➸ {count}\n'
        except Exception as e:
            bot.send_message(lab, str(e))
    text += f'Total ➸ {all_dias}'
    bot.send_message(lab, text, parse_mode='markdown')


def sort_key_dialogs(dia):
    try:
        if dia.chat.members_count:
            return -dia.chat.members_count
        else:
            return 0
    except:
        return 0


def gapatoon(client, message):
    dialogs = client.iter_dialogs()
    text = ''
    i = 1
    for dialog in sorted(dialogs, key=sort_key_dialogs):
        chat = dialog.chat
        if chat.title:
            chat_id = chat.id
            text += f"\n\n{i} - `{chat.title}` ➸ `{chat_id}` | {chat.members_count}"
            i += 1
    message.reply_text(text)

def exec_command(client, message):
    code = message.text[6:]

    class OutputListener:
        def __init__(self):
            self.output = ''
        def write(self, text):
            self.output += text
        def __str__(self):
            return self.output


    ExecuteTemplate = '''**Executed Code:**
```{}```
**Output:**
`{}`'''

    listener = sys.stdout = sys.stderr = OutputListener()

    try:
        exec(code)

    except Exception:
        traceback.print_exc()
        listener.output += ''

    sys.stdout = stdout
    sys.stderr = stderr

    try:
        message.reply_text(ExecuteTemplate.format(code, listener.output), parse_mode='markdown')
    except Exception as e:
        message.reply_text(ExecuteTemplate.format(code, e), parse_mode='markdown')






