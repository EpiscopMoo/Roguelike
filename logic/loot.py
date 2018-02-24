from engine.guiengine import YLW_BLK


class Loot:
    def __init__(self, items):
        if len(items) < 1:
            raise Exception("Cannot instantiate Loot object with zero items.")
        self.items = items
        self.name = "Предметы"
        self.description = ", ".join([x.name for x in items])
        self.skin = '%'
        self.color = YLW_BLK
        self.type = 'loot'
        self.pic = None

    def extend(self, items):
        if items is None or len(items) == 0:
            return
        else:
            self.items.extend(items)
            self.description = ", ".join([x.name for x in items])