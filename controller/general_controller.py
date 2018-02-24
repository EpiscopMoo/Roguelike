from globals import Globals


class GeneralController:
    """Get user input and call an appropriate handler to deal with the event. Key event is then passed to this new handler
    which, in its turn, changes the state of the game. After logic update, new handler is returned and boolean response,
    showing whether time-costing move was performed or was it some instant operation instead.
    Example:
        1. - External game loop calls @process_key_event()
        2. - 'i' keypress detected
        3. - GeneralController passes this key action to its current handler - Dungeon class instance
        4. - Dungeon checks internal logic - e.g. prepares to open an inventory
        5. - Dungeon returns a pair (Inventory, false), because new handler will be the Inventory, and false because this action is not treated as player move.
        6. - The control gets back to GeneralController which invokes the displaying of prepared Inventory object."""
    def __init__(self, init_handler):
        self.key = None
        self.current_handler = init_handler

    def process_key_event(self):
        self.current_handler.invoke()
        key = Globals.default_screen.getch()
        handler, moved = self._get_handler(key)
        if handler is not None:
            handler.invoke()
            return moved
        else:
            return None

    def _get_handler(self, key):
        proposed_handler, moved = self.current_handler.process_key_event(key)
        self.current_handler = proposed_handler
        return self.current_handler, moved