from controller.general_controller import GeneralController
from controller.main_menu_handler import MainMenuHandler


class Interaction:
    def invoke(self):
        controller = GeneralController(MainMenuHandler())
        game_finished = False
        while game_finished is False:
            event_result = controller.process_key_event()
            if event_result is None:
                game_finished = True