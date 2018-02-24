class Instance:
    def invoke(self):
        raise Exception("Calling invoke() on abstract instance is not allowed")

    def process_key_event(self, key):
        raise Exception("Processing key event is impossible for abstract instance")
