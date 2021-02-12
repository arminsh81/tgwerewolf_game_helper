from . import data_database_queries, helper_database_queries, ali_db, main_bot, beta_bot, log_to_lab
from . import rs_bot, web_app_address
import time
from requests import post
from pyrogram.errors import UserNotParticipant, FloodWait

class Chat:

    def __init__(self, client, chat_id):
        self.client = client
        self.id = self.chat_id = chat_id

    @property
    def setting(self):
        return helper_database_queries.get_group_setting(self.id)

    @staticmethod
    def is_spy(client):
        try:
            return client.is_spy
        except:
            return False

    def set_group_state(self, state):
        data_database_queries.set_group_state(self.id, state)

    class UserData:
        def __init__(self, user, first_name):
            self.user = user
            self.first_name = first_name
            self.is_alive = True
            self.is_winner = True
            self.status = 'member'
            self.role_id = 0

    def add_new_game(self, msg_id, user):
        data_database_queries.add_new_game(self.id, msg_id, user)
        self.set_group_state('jointime')
        print(self.id, ' new game')

    def join_time_pin(self, message):
        settings = self.setting
        if settings and not Chat.is_spy(self.client):
            if settings['jointime_pin']:
                try:
                    rs_bot.pin_chat_message(message.chat.id, message.message_id)
                except Exception as e:
                    print(e)
                    message.reply_text("/pinn@ExecutrixBot")
            time.sleep(5)
            if settings['is_fillit_enable']:
                message.reply_text("/fillit@TsWwPlus_Bot")

    def send_next_pin(self):
        settings = self.setting
        if settings and not Chat.is_spy(self.client):
            try:
                if settings.game_started_pin:
                    try:
                        res = post('{}/v1/game_started_pin'.format(web_app_address), json={'chat_id': self.id})
                        res = res.json()
                        if not res['error']:
                            return
                    except Exception as e:
                        print(e)
                    self.client.send_message(
                        chat_id=self.id,
                        text="#next")
            except:
                pass
        self.set_group_state('ingame')


    def delete_join_link(self):
        ali_db.delete_link(self.id)

    def first_list(self, message):
        users_data = [ent.user.id for ent in message.entities if ent.type == 'text_mention']
        try:
            settings = self.setting
            if settings and not Chat.is_spy(self.client):
                if self.id in helper_database_queries.manager_chats:
                    message.reply_text("/tag_del@manage_ww_bot", quote=False)
                if settings.role_saver:
                    if settings.role_saver == 1:
                        res = post('{}/v1/uploadFirstList'.format(web_app_address), json={
                            'chat_id': self.id,
                            'message_id': message.message_id,
                            'text': message.text,
                            'users': users_data
                        })
                        try:
                            res = res.json()
                            if not res['error']:
                                return
                        except Exception as e:
                            print(e)
                        message.reply_text("/up@role_ww_bot")
                    elif settings.role_saver == 2:
                        message.reply_text("/new@TsWwPlus_Bot")
        except:
            pass
        print(self.id, ' first list')
        self.set_group_state('ingame')

    def start_game(self, message):
        players = [ent.user.id for ent in message.entities if ent.type == 'text_mention']
        print(self.id, ' game star t', players, len(players))
        data_database_queries.start_game(self.id, len(players))

    def game_list(self, message):
        settings = self.setting
        if settings and not Chat.is_spy(self.client):
            if settings.role_saver:
                if settings.role_saver == 1:
                    users_data = [ent.user.id for ent in message.entities if ent.type == 'text_mention']
                    res = post('{}/v1/uploadGameList'.format(web_app_address), json={
                        'chat_id': self.id,
                        'message_id': message.message_id,
                        'text': message.text,
                        'users': users_data
                    })
                    try:
                        res = res.json()
                        if not res['error']:
                            return
                    except Exception as e:
                        print(e)
                    message.reply_text("/up@role_ww_bot")
                elif settings.role_saver == 2:
                    message.reply_text("/tsup@TsWwPlus_Bot")
        print(self.id, ' game list')

    def game_finish(self, message):
        settings = self.setting
        user = message.from_user.id
        if settings and not Chat.is_spy(self.client):
            try:
                res = post('{}/v1/finishGame'.format(web_app_address), json={
                    'chat_id': self.id,
                    'message_id': message.message_id
                })
                try:
                    res.json()
                except Exception as e:
                    print(e)

                if self.id in [-1001232594917, -1001414470547]:
                    message.reply_text("/getpoints")
                    time.sleep(1)

                if settings.is_confirm_tsww_enable:
                    message.reply_text("/confirm@TsWwPlus_Bot")
                    time.sleep(1)

                if settings.is_startnewgame_enable:
                    if settings.start_mode == 1:
                        msg = "/startchaos"
                    else:
                        msg = "/startgame"
                    if user == main_bot:
                        msg += "@werewolfbot"
                    elif user == beta_bot:
                        msg += "@werewolfbot"
                    message.reply_text(msg, quote=False)
            except Exception as e:
                print(e)
        self.set_group_state('idle')

    def game_finish_db(self, message):
        data_database_queries.finish_game(self.id)
        try:
            users = [self.UserData(entity.user.id, entity.user.first_name) for entity in message.entities
                     if entity.type in ('mention', 'text_mention')]
            for user in users:
                try:
                    r = self.client.get_chat_member(self.id, user.user)
                    user.status = r.status
                except UserNotParticipant as e:
                    user.status = 'left'
                except:
                    user.status = 'Error'
            print('game finish db start save')
            data_database_queries.define(message.text, users, self.id, message.message_id)
            data_database_queries.define_winner(message)
            print('game finish db end save')
        except Exception as e:
            log_to_lab(str(self.id) + ' failed on adding')
            log_to_lab(' '.join(e.args))
            log_to_lab(message.text.markdown)

    def cancel_game(self, message):
        settings = self.setting
        if settings and not Chat.is_spy(self.client):
            if self.id in helper_database_queries.manager_chats:
                message.reply_text("/tag_del@manage_ww_bot", quote=False)
        self.delete_join_link()
        data_database_queries.cancel_game(self.id)
        self.set_group_state('idle')

    def grey_next(self, message):
        msg_id = message.message_id
        rep = message.reply_to_message
        if rep.text and not Chat.is_spy(self.client):
            if rep.from_user.is_self:
                if rep.text == '#next':
                    settings = self.setting
                    if (settings and settings.game_started_pin) or not settings:
                        try:
                            time.sleep(4)
                            try:
                                rs_bot.pin_chat_message(self.id, msg_id, disable_notification=True)
                            except Exception as e:
                                print(e)
                                message.reply_text("/pin@ExecutrixBot")
                        except FloodWait as e:
                            pass

    def add_gp(self, message):
        title = message.chat.title
        text = message.text
        link = text.replace('add gp ', '').replace('Add gp', '')
        if link:
            try:
                group_title = self.client.get_chat(link).title
            except:
                message.reply_text('لینک داده شده معتبر نمیباشد')
                return
            if title != group_title:
                message.reply_text('لینک داده شده برای این گروه نمیباشد')
                return
            admins = self.client.get_chat_members(self.id, filter='administrators')
            creator = None
            for admin in admins:
                if admin.status == 'creator':
                    creator = admin.user.id
            helper_database_queries.add_group(self.id, title, creator, link)
            message.reply_text('گروه نصب شد', quote=False)
        else:
            message.reply_text('لینک و یادت رفت بزاری')

    def add_message_as_mention(self, message):
        message_id = message.message_id
        user_id = message.from_user.id
        entities = message.entities
        if entities and not Chat.is_spy(self.client):
            group_info = data_database_queries.get_group_status(self.id)
            if group_info:
                if group_info == 'idle':
                    status = 0
                elif group_info =='ingame':
                    status = 2
                elif group_info == 'jointime':
                    status = 1
                else:
                    status = 0
            else:
                return
            if status == 1:
                entity_length = 0
                message_length = len(message.text)
                for entity in entities:
                    if entity['type'] in ['text_mention', 'mention']:
                        entity_length += entity['length']
                if entity_length / message_length >= 0.4:
                    data_database_queries.add_message_for_delete_database(message_id, self.id, user_id)

    def save_game_link(self, message):
        user_id = message.from_user.id
        try:
            url = message.click(0)
            ali_db.add_start(self.id, url, user_id)
        except ValueError as e:
            pass
        except Exception as e:
            log_to_lab(' '.join(e.args))

    def save_afk(self, message):
        afked_players = list(set([ent.user.id for ent in message.entities if ent.type == 'text_mention']))
        [data_database_queries.save_afk(self.id, u) for u in afked_players]
        if self.id == -1001476763360:
            try:
                [data_database_queries.save_afk_lu(u, message.message_id) for u in afked_players]
            except:
                pass

    def save_vote(self, message):
        votes = [ent.user.id for ent in message.entities if ent.type == 'text_mention']
        tmp = []
        for vote in votes:
            tmp.append(vote)
            if len(tmp) == 2:
                voter, voted = tmp
                data_database_queries.save_vote(self.id, voter, voted)
                tmp = []
