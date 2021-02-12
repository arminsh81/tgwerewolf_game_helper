from cachetools import TTLCache, cached
from . import check_chat, get_cur, log_to_lab, now
import traceback


chats = manager_chats = []
group_cache = {}

class AttributeDict(dict):
    def __getattr__(self, item):
        return self.get(item)

def return_attr(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, dict):
            return AttributeDict(res)
        return res
    return wrapper


@return_attr
@check_chat
@cached(TTLCache(maxsize=1024, ttl=30))
def get_group_setting(group_id):
    conn, cur = get_cur()
    try:
        query = f"""
select jointime_pin as jtp,
       game_started_pin as stp,
       is_confirm_tsww_enable as cts,
       is_confirm_score_enable as cs,
       is_startnewgame_enable as stn,
       start_mode as stm,
       disabled_by
from v1.all_group_helper
where group_id = %s
        """
        cur.execute(query, (group_id,))
        res = cur.fetchone()
        cur.close()
        if res:
            return dict(
                jointime_pin=res[0],
                game_started_pin=res[1],
                is_confirm_tsww_enable=res[2],
                is_fillit_enable=res[3],
                is_startnewgame_enable=res[4],
                start_mode=res[5],
                role_saver=res[6]
            )
        return res
    except Exception as e:
        log_to_lab(e)
        cur.close()
        return False




def add_group(group_id, title, creator, link):
    conn, cur = get_cur()
    try:
        query = f"""
                insert into v1.all_group_helper(group_id, title, creator, link, created_at,is_confirm_score_enable, is_startnewgame_enable) 
                values (%s, %s, %s, %s, %s, 1, TRUE)
                """
        cur.execute(query, (group_id, title, creator, link, now()))
        conn.commit()
        cur.close()
        return True
    except Exception as t:
        log_to_lab(t)
        cur.close()
        return False


def dis_group(group_id, user):
    conn, cur = get_cur()
    try:
        query = f"""
                update v1.all_group_helper
                set is_disabled= %s, disabled_at= %s, disabled_by= %s
                where group_id = %s
                """
        cur.execute(query, (False, now(), user, group_id))
        conn.commit()
        cur.close()
        return True
    except Exception as t:
        log_to_lab(t)
        cur.close()
        return False





def get_chats_with_manager():
    conn, cur = get_cur()
    try:
        query = f"""
select distinct chat_id
from v1.manager_join_setting_1
        """
        # cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        if res:
            global manager_chats
            manager_chats = [i[0] for i in res]
            return
        if not res: return res
    except:
        cur.close()
        return False


def get_all_group_id():
    conn, cur = get_cur()
    try:
        query = f"""
        select group_id
        from v1.all_group_helper  
        """
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        if res:
            return set([i[0] for i in res])
        if not res:
            return res
    except:
        cur.close()
        return False


def get_all_groups_status():
    query = """
select distinct on (group_id) created_at, started_at, finished_at,game_bot,group_id
from v2.all_games
where canceled is false
order by group_id,created_at desc
    """
    conn, cur = get_cur()
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    if res:
        return {i[4]: AttributeDict(created_at=i[0], started_at=i[1], finished_at=i[2], bot=i[3]) for i in res}
    return res


def group_status_cache():
    res = get_all_groups_status()
    if res:
        global group_cache
        group_cache = res

