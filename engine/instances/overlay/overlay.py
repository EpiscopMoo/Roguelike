class Overlay:
    def __init__(self):
        self.screen = None

    def process_key_event(self, key):
        pass

    def invoke(self):
        self.screen.clear()
        self.print()
        self.screen.refresh()

    def print(self):
        pass