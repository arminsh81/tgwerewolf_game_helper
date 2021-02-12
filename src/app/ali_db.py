import psycopg2
from . import ali_conn as con


def add_start(chat_id, link, user_id):
    try:
        cur = con.cursor()
        cur.execute('''UPDATE ali_ag_db.joinlink SET link= %(link)s WHERE chat_id= %(chat_id)s ANd user_id= %(user_id)s;
        INSERT INTO ali_ag_db.joinlink (chat_id , link,user_id)
           SELECT %(chat_id)s, %(link)s ,%(user_id)s
           WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.joinlink WHERE chat_id= %(chat_id)s and user_id= %(user_id)s);''',
                    {'chat_id': chat_id, 'user_id': user_id, 'link': f'{link}'})
        con.commit()
        cur.close()
    except Exception as e:
        print(e)


def delete_link(chat_id):
    try:
        cur = con.cursor()
        cur.execute('''DELETE FROM ali_ag_db.joinlink
                     WHERE chat_id = %(chat_id)s''', {'chat_id': chat_id})

        con.commit()
        cur.close()
    except Exception as e:
        print(e)

