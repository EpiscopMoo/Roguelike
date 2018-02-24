import curses

from engine.guiengine import draw_window, draw_pic, get_dy_dx
from engine.instances.instance import Instance
from engine.screen import Screen

PIC = [
    "   .          _-o#&&*''''?d:>b\_        .            .          .                   .          .                    ",
    "        . _o/\"`''  '',, dMF9MMMMMHo_         .                                                                 .   ",
    "       .o&#'        `\"MbHMMMMMMMMMMMHo.                                 .                              .           ",
    " .   .o\"\" '         vodM*$&&HMMMMMMMMMM?.             В 2234 году человек узнал, что он не одинок во Вселенной.   ",
    "    ,'              $M&ood,~'`(&##MMMMMMH\          .  Чуть менее, чем за столетие, нам удалось покорить десятки    ",
    "   /               ,MMMMMMM#b?#bobMMMMHMMML             звёздных систем и колонизировать около полусотни планет,    ",
    "  &              ?MMMMMMMMMMMMMMMMM7MMM$R*Hk            поддерживая дружеские отношения с представителями инопла-   ",
    " ?$.            :MMMMMMMMMMMMMMMMMMM/HMMM|`*L            нетных рас. \"Содружество\", так мы стали называть наше    ",
    "|               |MMMMMMMMMMMMMMMMMMMMbMH'   T,      .    новое межпланетное сообщество, росло и процветало.         ",
    "$H#:            `*MMMMMMМЯСИКИMMMMMMMMb#}'  `?                                                        .             ",
    "]MMH#             \"\"*\"\"\"\"*#MMMMMMMMMMMMM'      -             .                         .                 .    ",
    "MMMMMb_                   |MMMMMMMMMMMP'     :           Но золотой век продлился недолго: вскоре на планету Земля  ",
    "HMMMMMMMHo                 `MMMMMMMMMT       .        .  высадились войска тогда ещё неизвестного внеземного вида.  ",
    "?MMMMMMMMP                  9MMMMMMMM}       -           Мы совсем не были к этому готовы. Небольшой космический    ",
    "-?MMMMMMM                  |MMMMMMMMM?,d-    '          флот был уничтожен за считанные минуты, крупные города были ",
    " :|MMMMMM-                 `MMMMMMMT .M|.   :          выжжены дотла. Содружество объявило полную мобилизацию, а на ",
    "  .9MMM[                    &MMMMM*' `'    .           Земле в это время начинается партизанская война. Я узнаю об  ",
    "   :9MMk                    `MMM#\"        -           этом одним из первых: на колонию, в которой я живу, напали ",
    "     &M}                     `          .-            гергоны - так мы назвали захватчиков. Мне остаётся лишь попы- ",
    "      `&.                             .       .       таться покинуть планету до того, как её полностью оккупируют. ",
    "        `~,   .                     ./                                                             .                ",
    "  .         . _                  .-                         .                   .          .                      . ",
    "         .    '`--._,dd###pp=\"\"'         .                                                                        ",
    "                                                                                                   .                ",
    "   .             .             .                                            .                               .       ",
    "         .                .                 .                                                                       ",
    "                                                                   .                              .                 ",
    "     .             .                   .                  .                              .                      .   "
]



class IntroInstance(Instance):
    def __init__(self):
        self.screen = Screen(curses.LINES-1, curses.COLS-1)
        self.pad = self.screen.pad
        self.h = 30
        self.w = 124
        self.H = self.screen.H
        self.W = self.screen.W
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)

    def process_key_event(self, key):
        if key == ord(' ') or key == ord('\n'):
            from controller.create_hero_handler import CreateHeroHandler
            return CreateHeroHandler(), False
        from controller.splash_screen_handler import SplashScreenHandler
        return SplashScreenHandler(self), False

    def invoke(self):
        self.screen.clear()
        self.print()
        self.screen.refresh()

    def print(self):
        y = self.dy
        x = self.dx
        h = self.h
        w = self.w

        draw_window(self.pad, y, x, h, w, 'Пролог', 'Нажмите [Enter] или [Space] для продолжения')
        self._print_description()

    def _print_description(self):
        draw_pic(self.pad, self.dy + 2, self.dx + 2, PIC)