import importlib


class Handler:
    def __init__(self, instance=None, overlay=None):
        self.overlay = overlay
        self.next = None
        self.instance = instance

    def invoke(self):
        self.instance.invoke()

    def process_key_event(self, key):
        return self.instance.process_key_event(key)
