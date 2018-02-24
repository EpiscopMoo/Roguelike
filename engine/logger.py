def logged(func):
    def wrapper(*args, **kw):
        Logger.enable()
        val = func(*args, **kw)
        Logger.disable()
        return val
    return wrapper


class Logger:
    file = None
    enabled = False

    @staticmethod
    def initialize(filename='log.txt'):
        Logger.file = open(filename, 'a+')

    @staticmethod
    def debug(str):
        if Logger.enabled:
            Logger.file.write(str + '\n')

    @staticmethod
    def enable():
        Logger.enabled = True

    @staticmethod
    def disable():
        Logger.enabled = False