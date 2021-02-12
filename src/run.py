from pyrogram import MessageHandler, Filters
from app import apps, apps_free, rs_bot, lab, game_bots, tools_bot, admins, spies, lupine_guy_token
import schedule
from app.data_database_queries import get_last_game_id
from app.helper_database_queries import get_chats_with_manager
from app.terminal_beutify import console_update
from time import sleep
from app import handlers, patterns
import sys


def main():
    get_chats_with_manager()
    schedule.every(5).seconds.do(console_update)
    schedule.every(10000).seconds.do(get_chats_with_manager)
    get_last_game_id()
    rs_bot.start()

    apps[0].add_handler(MessageHandler(handlers.count_gaps, filters=Filters.chat(lab) & Filters.regex(r'^/amar$')))
    apps[0].add_handler(MessageHandler(handlers.exec_command, Filters.user([660462150, 1147334296, 951153044, 1327834355, 1372089184]) & Filters.command('exec')))
    handler_list = [MessageHandler(handlers.detect_game_finished, filters=Filters.user(game_bots) & Filters.regex(patterns.game_finish) & ~Filters.edited),
                MessageHandler(handlers.detect_game_started_message,
                               filters=Filters.user(game_bots) &
                                       Filters.regex(patterns.game_list) & ~Filters.regex(
                                   patterns.death) & ~Filters.edited),
                MessageHandler(handlers.detect_game_list,
                               filters=Filters.user(game_bots) &
                                       Filters.regex(patterns.game_list) & ~Filters.edited),

                MessageHandler(handlers.detect_game_start,
                               filters=Filters.user(game_bots) &
                                       Filters.regex('#players') & ~Filters.edited),
                MessageHandler(handlers.detect_game_started,
                               filters=Filters.user(game_bots) &
                                       Filters.regex(patterns.game_started) & ~Filters.edited),
                MessageHandler(handlers.detect_game_canceled,
                               filters=Filters.user(game_bots) &
                                       Filters.regex(patterns.game_canceled) & ~Filters.edited
                               ),
                MessageHandler(handlers.afked_players,
                               filters=Filters.user(game_bots) &
                                       Filters.regex(patterns.player_afk) & ~Filters.edited
                               ),
                MessageHandler(handlers.player_votes,
                               filters=Filters.user(game_bots) &
                                       Filters.regex(r'خب .+ نظرش اینه که .+ اعدام بشه') & ~Filters.edited
                               ),
                MessageHandler(handlers.grey_next,
                               filters=Filters.user(tools_bot) & Filters.reply),
                MessageHandler(handlers.add_gp,
                               filters=Filters.user(admins) & Filters.regex(r'^[a|A]dd gp')),
                MessageHandler(handlers.define_message_as_mention,
                               filters=Filters.bot & Filters.group & ~Filters.user(game_bots)),
                MessageHandler(handlers.game_start_save_link, filters=Filters.user(game_bots) & Filters.regex(
                    pattern=patterns.jointime_started) & ~Filters.edited),
                MessageHandler(handlers.gapatoon, filters=Filters.chat(lab) & Filters.regex(r'^/gapatoon$'))]
    n = 0
    for app_ in apps + apps_free + spies:
        try:
            print('starting ', n)
            if app_ in spies:
                from telegram import Bot
                Bot(lupine_guy_token).send_message(-1001444185267, 'starting that goodness')
            app_.start()
            if app_ in spies:
                from telegram import Bot
                Bot(lupine_guy_token).send_message(-1001444185267, 'started that goodness')
            n += 1
            if '-j' in sys.argv:
                try:
                    app_.join_chat('https://t.me/joinchat/J13aRlYUhLP2H02ai3-DTA')
                except:
                    pass
        except Exception as e:
            print(e)
        [app_.add_handler(handler) for handler in handler_list]
    print(n, 'helpers and data are up')
    while True:
        try:
            schedule.run_pending()
            sleep(1)
        except KeyboardInterrupt:
            break
    rs_bot.stop()
    [app_.stop() for app_ in apps + apps_free]


if __name__ == '__main__':
    main()
