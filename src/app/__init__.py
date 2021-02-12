from pyrogram import Client
import psycopg2
import psycopg2.extensions
from psycopg2._psycopg import cursor, connection
from telegram import Bot
from pytz import timezone
from datetime import datetime

from json import loads
from dotenv import load_dotenv
from os import getenv
from os import getenv
lupine_guy_token = getenv("TG_LUPINE_GUY", '')


load_dotenv()

helpers = getenv('HELPERS', '')
# print(helpers)
helpers = helpers.split(' ')
helpers = {helper.split(',')[0]: helper.split(',')[1] for helper in helpers}
# helpers = loads(helpers)
rs_token = getenv("ROLE_SAVER_TOKEN", '')
web_app_address = ''
lab = -1001444185267
main_bot = 175844556
beta_bot = 198626752
game_bots = [main_bot, beta_bot, 1202084863, 1147334296]
tools_bot = [491459293]
admins = [660462150, 951153044, 1056496370, 638994540, 941773249, 1184814450, 1082983562, 1336429978, 1327834355,631720252]

bot = Bot(token=lupine_guy_token)

apps_free = []
apps = []
spies = []
api_id =getenv("HELPER_API_ID", '')
api_hash= getenv("HELPER_API_HASH", '')
for session_name, session_str in helpers.items():
    session_str: str
    if session_name.startswith('helper_free_'):
        apps_free.append(Client(
            session_str,
            api_id=api_id,
            api_hash=api_hash
        ))
    elif session_name.startswith('helper_'):
        apps.append(Client(
            session_str,
            api_id=api_id,
            api_hash=api_hash
        ))
    elif session_name.startswith('spy_'):
        spies.append(Client(
            session_str,
            api_id=api_id,
            api_hash=api_hash
        ))

for c in spies:
    c.is_spy = True

# sessions_dir = 'app/sessions/'
# apps_free = [Client(sessions_dir + "helper_free_{}".format(i),
#                     api_id=930623,
#                     api_hash="9f716af9750f532e1c33259e4bc55c50"
#                     ) for i in [1, 2, 3, 4]]
# apps = [Client(sessions_dir + "helper_{}".format(i),
#                api_id=1038622,
#                api_hash="87ca332fa9f9b84d89c28a02a2abd0dc"
#                ) for i in [1, 2, 3]]
app1 = apps[0]

rs_bot = Client(':memory:', bot_token=rs_token,
                api_id=api_id,
                api_hash=api_hash
                )

game_ids = {}

database_kw = eval(getenv('DATABASE'))

ali_conn = psycopg2.connect(**database_kw)


def get_cur() -> (connection, cursor):
    if not hasattr(get_cur, 'conn') or get_cur.conn.closed != 0:
        get_cur.conn = psycopg2.connect(**database_kw)
    if get_cur.conn.status == psycopg2.extensions.STATUS_IN_TRANSACTION:
        get_cur.conn.rollback()
    cur: cursor = get_cur.conn.cursor()
    conn: connection = get_cur.conn
    return conn, cur


def check_chat(func):
    def check_in_in_game_users(chat_id):
        global game_ids
        if chat_id not in game_ids:
            game_ids.update({chat_id: None})

    def wrapper_check(group_id, *args, **kwargs):
        check_in_in_game_users(group_id)
        return func(group_id, *args, **kwargs)

    return wrapper_check


def now():
    iran = timezone('Asia/Tehran')
    sa_time = datetime.now(iran)
    return sa_time.strftime('%Y-%m-%d %H:%M:%S')


log_to_lab = lambda msg: bot.send_message(lab, str(msg))
