from . import get_cur, now, check_chat, log_to_lab
from . import patterns
from requests import post
import time, threading, re, traceback
from random import randint
from cachetools import TTLCache, cached
from . import patterns
from .patterns import roles_by_emoji, roles_pattern

game_ids = {}
cached_save_users = set()
group_cache = {}


def get_last_game_id():
    global game_ids
    query = """
    select distinct on (group_id) group_id ,game_id
    from v2.all_games
    where canceled is false and finished_at is null 
        """
    conn, cur = get_cur()
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    if res:
        game_ids = {i[0]: i[1] for i in res}


@check_chat
def add_new_game(group_id, message_id, bot):
    conn, cur = get_cur()
    try:
        query = f"""
INSERT INTO v2.all_games(group_id, message_id, game_bot)

SELECT %(group_id)s, %(message_id)s, %(game_bot)s
WHERE
    NOT EXISTS (
        SELECT 1 FROM v2.all_games WHERE group_id = %(group_id)s and message_id = %(message_id)s
    )
returning game_id;
                """
        cur.execute(query, {
            'group_id': group_id,
            'message_id': message_id,
            'created_at': now(),
            'game_bot': bot})
        res = cur.fetchone()
        conn.commit()
        cur.close()
        if res:
            cancel_game(group_id, for_new=True)
            global game_ids
            game_ids[group_id] = res[0]
        return True
    except Exception as t:
        print(t)
        cur.close()
        return False


@check_chat
def start_game(group_id, players):
    conn, cur = get_cur()
    try:
        game_id = game_ids[group_id]
        if not game_id:
            return True
        query = f"""
update v2.all_games
set started_at = %s , player_count = %s
where game_id in (
    select game_id from v2.all_games
    where group_id=%s and started_at is null
    order by created_at desc limit 1)
                """
        cur.execute(query, (now(), players, group_id))
        conn.commit()
        cur.close()
        return True
    except Exception as t:
        print(t)
        cur.close()
        return False



@check_chat
def cancel_game(group_id, for_new=False):
    global game_ids
    conn, cur = get_cur()
    try:
        query = f"""
                update v2.all_games
                set canceled = %s
                where game_id in (
    select game_id from v2.all_games
    where group_id=%s 
    order by created_at desc {'offset 1' if for_new else ''} limit 1)
and started_at is null and finished_at is null
                """
        cur.execute(query, (True, group_id))
        conn.commit()
        cur.close()
        game_ids[group_id] = None
        return True
    except Exception as e:
        print(e)
        cur.close()
        return False



@check_chat
def finish_game(group_id):
    global game_ids
    conn, cur = get_cur()
    try:
        game_id = game_ids[group_id]
        if not game_id:
            return True
        query = f"""
            update v2.all_games
            set finished_at = %s
            where game_id in (
    select game_id from v2.all_games
    where group_id=%s and finished_at is null
    order by created_at desc limit 1)
                """
        cur.execute(query, (now(), group_id))
        conn.commit()
        cur.close()
        game_ids[group_id] = None
        return True
    except Exception as e:
        print(e)
        cur.close()
        return False





def remove_from_cached_save_users(chat_id):
    global cached_save_users
    time.sleep(10)
    cached_save_users.remove(chat_id)


def cache_save_users(chat_id):
    global cached_save_users
    cached_save_users.add(chat_id)
    threading.Thread(target=remove_from_cached_save_users, args=(chat_id,), daemon=True).start()


def save_users(users, chat_id, message_id):
    try:
        time.sleep(randint(1, 70) / 10)
        if chat_id in cached_save_users:
            print('i saved this list before')
            return
        values = []
        for user in users:
            values.append([message_id, user.user, chat_id, user.status, user.is_winner, user.is_alive, user.role_id])
        query = """
        INSERT INTO v2.users_activity_log_v2("message_id","user_id", "group_id", "status", "is_winner", "is_alive", "role_id")
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        conn, cur = get_cur()
        cur.executemany(query, values)
        conn.commit()
        cur.close()
    except:
        cur.close()
        log_to_lab(str(chat_id) + ' failed on query')


def define(text, users, chat_id, message_id):
    try:
        lines = []
        for line in text.split('\n'):
            if re.search(patterns.game_finish, line):
                continue
            if re.search(patterns.game_list, line):
                continue
            if line.strip():
                lines.append(line)

        for i, user in enumerate(users):
            try:
                line = lines[i]
                if re.search(patterns.death, line):
                    user.is_alive = False
                if not re.search(r'برنده', line):
                    user.is_winner = False
                role = ' '.join(line.split(':')[-1].split('-')[1].split(' ')[:-1]).strip() if len(
                    line.split(':')[-1].split('-')) == 2 else False
                if not role:
                    log_to_lab('not role 326' + str(line))

                if role:
                    if 'کاراگاه' in role:
                        role_id = 11
                    else:
                        g = re.findall(roles_pattern, role)
                        if g[0] == '🕵️':
                            role_id = 11
                        else:
                            role_id = roles_by_emoji[g[0]]['role_id']
                    if role_id == 0:
                        try:
                            log_to_lab('not role 338' + str(line))
                            log_to_lab(f'{str(user.user)} | {str(user.first_name)} | {str(user.status)}  | {str(role_id)} ')
                        except:
                            pass
                    user.role_id = role_id
            except Exception as e:
                print(e)
        save_users(users, chat_id, message_id)
        return True
    except Exception as t:
        log_to_lab(str(chat_id) + ' failed on defining')
        return False
    except:
        log_to_lab((str(chat_id) + ' failed on defining'))
        return False


def save_game_winner(chat_id, message_id, player_count, winner):
    conn, cur = get_cur()
    try:
        query = """INSERT INTO v1.group_games(group_id, message_id, created_at, player_count, winner)
                   VALUES(%s, %s, %s, %s, %s)"""
        cur.execute(query, (chat_id, message_id, now(), player_count, winner))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        cur.close()
        return False


def rec_winner_tim(roles):
    roosta, ferghe, gorgs, ghatel, atish, monaf, bitim = [], [], [], [], [], [], []
    game_roles = {0: roosta, 1: ferghe, 2: gorgs, 3: ghatel, 4: atish, 5: monaf, 6: bitim}
    all_winners = []
    for user, data in roles.items():
        role_indexes = {'فرقه': 1, 'قاتل': 3, 'آتش زن': 4, 'گرگ': 2, 'جادوگر': 2, 'منافق': 5, 'دزد': 6, 'همزاد': 6}
        for ww_role in role_indexes:
            if ww_role in data['role'] and 'نما' not in data['role']:
                game_roles[role_indexes[ww_role]].append(True if 'برنده' in data['role'] else False)
                break
        else:
            game_roles[0].append(True if 'برنده' in data['role'] else False)
        if 'برنده' in data['role']:
            all_winners.append(True)

    for team in game_roles:
        if all(game_roles[team]) and game_roles[team]:
            if not any([any(game_roles[i]) for i in game_roles if game_roles[i] != game_roles[team]]) or len(
                    all_winners) != 2:
                # {0: 'روستاییا👱', 1: 'فرقه گراها👤', 2: 'گرگ ها🐺', 3: 'قاتل زنجیره ای🔪', 4: 'آتش زن🔥',
                # 5: 'منافق👺'}
                return team
    else:
        if len(all_winners) == 2:
            return 6
    return 7


def define_winner(message):
    chat_id = message.chat.id
    text = message.text
    msg_id = message.message_id
    roles = {
        ''.join(i.split(':')[:-1]): {
            'state': i.split(':')[-1].split('-')[0],
            'role':
                i.split(':')[-1].split('-')[1] if len(
                    i.split(':')[-1].split('-')) == 2 else False}
        for i in text.split('\n')[1:-1] if i}
    winner = rec_winner_tim(roles)
    save_game_winner(chat_id, msg_id, len(roles), winner)


def save_afk(chat_id, user_id):
    query = '''INSERT INTO v2.users_afks("chat_id", "user_id", "afk_at") VALUES 
                (%(chat_id)s, %(user_id)s, %(afk_at)s)'''
    conn, cur = get_cur()
    cur.execute(query, {'chat_id': chat_id, 'user_id': user_id, 'afk_at': now()})
    conn.commit()


def save_afk_lu(user_id, message_id):
    web_app_address = 'http://94.130.7.132:5544'
    post('{}/lu/afkUser'.format(web_app_address), json={
        'user_id': user_id,
        'message_id': message_id
    })


def add_message_for_delete_database(message_id, group_id, user_id):
    query = """
    insert into v1.manager_delete_message(group_id,message_id,created_at, user_id)
    values (%s,%s,(now()at time zone 'Asia/Tehran')::timestamp,%s)
    """
    conn, cur = get_cur()
    try:
        cur.execute(query, (group_id, message_id, user_id))
        conn.commit()
        cur.close()
        return True
    except:
        cur.close()
        return False



def set_group_state(chat_id, state):
    conn, cur = get_cur()
    query = """UPDATE v2.group_states SET state=%(state)s , last_update=%(now)s WHERE chat_id=%(chat_id)s;
INSERT INTO v2.group_states (chat_id, state, last_update)
       SELECT %(chat_id)s, %(state)s, %(now)s
       WHERE NOT EXISTS (SELECT 1 FROM v2.group_states WHERE chat_id=%(chat_id)s);"""
    cur.execute(query, {'chat_id': chat_id, 'state': state, 'now':now()})
    conn.commit()


@cached(TTLCache(maxsize=1024, ttl=10))
def get_group_status(chat_id):
    query = """SELECT state FROM v2.group_states WHERE chat_id=%s"""
    conn, cur = get_cur()
    cur.execute(query, (chat_id,))
    res = cur.fetchone()
    return res[0] if res else res


def save_vote(chat_id, voter, voted):
    query = """INSERT INTO v1.player_votes(chat_id, voter, voted, vote_at)
               VALUES(%s, %s, %s, %s)"""
    conn, cur = get_cur()
    cur.execute(query, (chat_id, voter, voted, now()))
    conn.commit()
