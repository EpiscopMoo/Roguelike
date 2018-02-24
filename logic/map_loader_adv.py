import importlib

from logic import cell
from logic.items import Item


class MapInfo:
    def __init__(self, name, player_position, cells, characters):
        self.name = name
        self.player_position = player_position
        self.cells = cells
        self.characters = characters


class MapLoader:
    def __init__(self):
        self.cells = []
        self.player_position = (-1, -1)
        self.characters = []

    def _reset(self):
        self.cells = []
        self.player_position = (-1, -1)
        self.characters = []

    def _parse_textual(self, lines):
        dimensions = lines[0].split(' ')
        h = int(dimensions[0])
        w = int(dimensions[1])

        for y, line in enumerate(lines[1:h + 1]):
            line = line.rstrip()
            if len(line) < w:
                line += ' ' * (w - len(line))
            row = []
            x = 0
            for ch in line:
                row.append(cell.Cell(ch, y, x))
                x += 1
            self.cells.append(row)

    def _parse_characters(self, bindings, data):
        for char in data:
            key = char['class']
            clazz = bindings[key]
            ActorType = getattr(importlib.import_module("logic.actors.enemies"), clazz)
            character = ActorType(self.characters, self.cells)
            character.y, character.x = char['position']
            self.cells[character.y][character.x].entity = character
            self.characters.append(character)

            if 'drop' in char:
                items = []
                for item_class in char['drop']:
                    item_stats = getattr(importlib.import_module("logic.items"), item_class)
                    item = Item(item_stats)
                    items.append(item)
                character.add_static_drop(items)

    def process_map(self, path, filename):
        self._reset()

        with open(path + filename) as file:
            lines = file.readlines()

        module = importlib.import_module('logic.levels.'+filename)
        props = module.map_params
        cell.CELLS = props['cell2descr_binding']
        self._parse_textual(lines)
        self._parse_characters(props['char2class_binding'], props['chars'])
        self.player_position = props['player_position']
        info = MapInfo(props['name'], self.player_position, self.cells, self.characters)
        return info
