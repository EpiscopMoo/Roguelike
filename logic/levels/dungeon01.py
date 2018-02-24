map_params = {
    'name': 'Уитне: равнины',
    'map': 'dungeon01',
    'player_position': (34, 56),
    'char2class_binding': {
        'G': 'Guano',
        'F': 'Fahgro',
        'H': 'HergonScout',
        'M': 'Monokh'
    },

    'chars': [
        {
            'class': 'G',
            'type': 'enemy',
            'position': (13, 30),
            'drop': ['hp_potion', 'cloak', 'hat']
        },
        {
            'class': 'G',
            'type': 'enemy',
            'position': (11, 81),
            'drop': ['hp_potion']
        },
        {
            'class': 'G',
            'type': 'enemy',
            'position': (30, 77),
            'drop': ['hp_potion', 'cloak', 'hat']
        },
        {
            'class': 'F',
            'type': 'enemy',
            'position': (10, 32),
            'drop': ['hp_potion', 'cloak', 'hat']
        },
        {
            'class': 'F',
            'type': 'enemy',
            'position': (8, 26),
            'drop': ['hp_potion']
        }
    ],


    'cell2descr_binding': {
        '*': {'name': 'Ядовитый колючий кустарник', 'walkable': False, 'destructible': False,
              'description': 'Густые заросли ядовитого колючего кустарника. Попытка продраться через них будет равносильна самоубийству.',
              'pic': [
                  "    * *  **   ",
                  "  *_\*\_/ /*   ",
                  " *\_*\*\_/_/*  ",
                  "   ** *_ * *  ",
                  "    \_|__/"
              ]
              },
        'x': {'name': 'Колючее дерево', 'walkable': False, 'destructible': False,
              'description': 'Высокое дерево, ветви которого полностью покрыты колючками. Древесина совсем никудышная, но зато из сока местные научились гнать умопомрачительный (в буквальном смысле) самогон.',
              'pic': [
                  "   xxXXxx  ",
                  "  xx\X|XXxx ",
                  "    xx/xxx  ",
                  "  xx ||      ",
                  " XX\\\\//",
                  "    || ",
                  "    /|\\"

              ]
              },
        'o': {'name': 'Камни', 'walkable': False, 'destructible': False,
              'description': 'Груда немного заплесневевших камней. Плесень шевелится.',
              'pic': [
                  "               _   ",
                  "             _/_)_   ",
                  "      __    (  __ \  ",
                  "     (. )  (  _()  ) ",
                  "   ('    \/  ( ) \/ )",
                  "  /_______|__/__\_\__)"

              ]
            },
        '#': {'name': 'Заброшенный жилой модуль', 'walkable': False, 'destructible': False,
              'description': 'Отсек от мобильного жилого модуля. После колонизации такие модули часто использовались охотниками и путешественниками как дома на колёсах. Этот отсек насквозь проржавел и для эксплуатации непригоден.',
              'pic': [
                  "       _\/_____\/___",
                  "      /             \ ",
                  "    _/  LIFE  o======|",
                  " ==L     MODULE ~~~~ |",
                  "   I__.._________.._/",
                  "  "" (__)       (__) "

              ]
            },
        ' ': {'name': 'Земля', 'walkable': True, 'destructible': False,
              'description': 'Ничего интересного.'
            }
    }
}
