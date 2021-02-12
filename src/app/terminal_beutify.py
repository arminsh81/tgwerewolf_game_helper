from . import now
from os import system

setup_time = now()
game_list = 0
game_start = 0
game_started = 0
game_finish = 0
game_cancel = 0
groups = set([])
users = set([])


def console_update():
    return
    # \033[31m]
    num_color = '\033[37m'
    log_time = now()
    text = f"""
-----------{setup_time}-----------

\033[95m detected Game list     :{num_color} %s 
\033[95m detected Game start    :{num_color} %s 
\033[95m detected Game finish   :{num_color} %s 
\033[95m detected Game cancel   :{num_color} %s
\033[95m detected Game begin    :{num_color} %s

\033[95m detected Users         :{num_color} %s
\033[95m detected Groups        :{num_color} %s

-----------{log_time}-----------
""" % (game_list, game_start, game_finish, game_cancel, game_started, len(users), len(groups))

    system('clear')
    print(text)


def add_group(group):
    groups.add(group)

