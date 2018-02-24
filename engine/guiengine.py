import curses

BLK_WHT = 1
RED_BLK = 2
GRN_BLK = 3
BLU_WHT = 4
YLW_BLK = 5
WHT_BLK = 6


def init_colors():
    curses.init_pair(BLK_WHT, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(RED_BLK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(GRN_BLK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(BLU_WHT, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(YLW_BLK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(WHT_BLK, curses.COLOR_WHITE, curses.COLOR_BLACK)


def draw_window(pad, y, x, h, w, title=None, tooltip=None, selected=False):
    vchar = '*' if selected else '|'
    hchar = '*' if selected else '-'

    pad.addstr(y, x, '+')
    pad.addstr(y, x + w, '+')
    pad.addstr(y + h, x, '+')
    pad.addstr(y + h, x + w, '+')

    pad.addstr(y, x + 1, hchar * (w - 1))
    pad.addstr(y + h, x + 1, hchar * (w - 1))
    for i in range(1, h):
        pad.addstr(y + i, x, vchar)
        pad.addstr(y + i, x + w, vchar)

    if title is not None:
        ln = len(title)
        middle = w // 2
        start = middle - ln // 2 - 1
        pad.addstr(y, x + start, ' ' + title + ' ')

    if tooltip is not None:
        ln = len(tooltip)
        middle = w // 2
        start = middle - ln // 2 - 1
        pad.addstr(y + h, x + start, '(' + tooltip + ')')


def draw_overlay_window(pad, y, x, h, w, title=None, tooltip=None, selected=False, color=BLU_WHT):
    color_pair = curses.color_pair(color)
    for dy in range(y, y+h+1):
        pad.addstr(dy, x, ' '*w, color_pair)

    y += 1
    x += 2
    h -= 2
    w -= 4

    vchar = '*' if selected else '|'
    hchar = '*' if selected else '-'

    pad.addstr(y, x, '+', color_pair)
    pad.addstr(y, x + w - 1, '+', color_pair)
    pad.addstr(y + h, x, '+', color_pair)
    pad.addstr(y + h, x + w - 1, '+', color_pair)

    pad.addstr(y, x + 1, hchar * (w - 2), color_pair)
    pad.addstr(y + h, x + 1, hchar * (w - 2), color_pair)
    for i in range(1, h):
        pad.addstr(y + i, x, vchar, color_pair)
        pad.addstr(y + i, x + w - 1, vchar, color_pair)

    if title is not None:
        ln = len(title)
        middle = w // 2
        start = middle - ln // 2 - 1
        pad.addstr(y, x + start, ' ' + title + ' ', color_pair)

    if tooltip is not None:
        ln = len(tooltip)
        middle = w // 2
        start = middle - ln // 2 - 1
        pad.addstr(y + h, x + start, '(' + tooltip + ')', color_pair)


def draw_hero_stats(pad, y, x, hero):
    hp = hero.hp
    maxhp = hero.maxhp
    mp = hero.mp
    maxmp = hero.maxmp
    name = hero.name
    hppart = (int)(hp / maxhp * 20)
    mppart = (int)(mp / maxmp * 20)
    pad.addstr(y, x, name + " (%s)" % hero.class_name)
    pad.addstr(y + 1, x, 'HP: [' + '=' * hppart + (20 - hppart) * ' ' + '] ' + str(hp) + '/' + str(maxhp))
    pad.addstr(y + 2, x, 'MP: [' + 'o' * mppart + (20 - mppart) * ' ' + '] ' + str(mp) + '/' + str(maxmp))

    strn = hero.clazz.strength
    dext = hero.clazz.dexterity
    endr = hero.clazz.endurance
    knwg = hero.clazz.knowledge
    char = hero.clazz.charisma
    sprt = hero.clazz.spiritual
    pad.addstr(y + 3, x, "СИЛА : %d" % strn)
    pad.addstr(y + 3, x + 12, "ЗНАН.: %d" % knwg)
    pad.addstr(y + 4, x, "ЛОВК.: %d" % dext)
    pad.addstr(y + 4, x + 12, "ХАР. : %d" % char)
    pad.addstr(y + 5, x, "ВЫНС.: %d" % endr)
    pad.addstr(y + 5, x + 12, "ДУХ. : %d" % sprt)


def draw_class_stats(pad, y, x, clazz):
    strn = clazz.strength
    dext = clazz.dexterity
    endr = clazz.endurance
    knwg = clazz.knowledge
    char = clazz.charisma
    sprt = clazz.spiritual
    pad.addstr(y + 0, x, "СИЛА:         %d" % strn)
    pad.addstr(y + 1, x, "ЛОВКОСТЬ:     %d" % dext)
    pad.addstr(y + 2, x, "ВЫНОСЛИВОСТЬ: %d" % endr)
    pad.addstr(y + 3, x, "ЗНАНИЯ:       %d" % knwg)
    pad.addstr(y + 4, x, "ХАРИЗМА:      %d" % char)
    pad.addstr(y + 5, x, "ДУХОВНОСТЬ:   %d" % sprt)


def draw_enemy_stats(pad, y, x, enemy):
    hero = enemy
    hp = hero.hp
    maxhp = hero.maxhp
    mp = hero.mp
    maxmp = hero.maxmp
    name = hero.name
    hppart = (int)(hp / maxhp * 20)
    mppart = (int)(mp / maxmp * 20)
    pad.addstr(y, x, name + ' [враг]', curses.color_pair(2))
    pad.addstr(y + 1, x, 'HP: [' + '=' * hppart + (20 - hppart) * ' ' + '] ' + str(hp) + '/' + str(maxhp), curses.color_pair(2))
    pad.addstr(y + 2, x, 'MP: [' + 'o' * mppart + (20 - mppart) * ' ' + '] ' + str(mp) + '/' + str(maxmp), curses.color_pair(2))


def draw_text(pad, y, x, h, w, text, color=None):
    words = text.split()
    chunks = [words[0]]
    for word in words[1:]:
        if len(chunks[-1]) + len(word) < w:
            chunks[-1] += ' ' + word
        else:
            chunks.append(word)
    for dy, line in enumerate(chunks[:h]):
        if color is not None:
            pad.addstr(y + dy, x, line, curses.color_pair(color))
        else:
            pad.addstr(y + dy, x, line)
    return min(len(chunks), h)


def draw_messages(pad, y, x, h, w, messages):
    dy = 0
    for msg in messages:
        text = msg.text
        color = msg.color
        dy += draw_text(pad, y+dy, x, h-dy, w, text, color)
        if dy >= h-1:
            break


def draw_pic(pad, y, x, pic):
    i = 0
    for s in pic:
        pad.addstr(y+i, x, s)
        i += 1


def get_dy_dx(H, W, h, w):
    dy = max(0, H // 2 - h // 2)
    dx = max(0, W // 2 - w // 2)
    return dy, dx