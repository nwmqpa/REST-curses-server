"""Map class file."""


class Map(object):
    """Map class for managing inner map object."""

    def __init__(self, filename):
        self.can_push = {
            '1': ['X'],
            '2': ['X']
        }
        self.empty = [' ', 'O']
        with open(filename, 'r') as file_map:
            self.map = file_map.read()

    def move_at(self, x, y, x_offset, y_offset):
        print(x, y, x_offset, y_offset)
        try:
            to_move = self.pos_to_index(x, y)
            to_push = self.pos_to_index(x + x_offset, y + y_offset)
            after_push = self.pos_to_index(x + (x_offset * 2), y + (y_offset * 2))
            if self.is_empty(to_push):
                old_moved = self.replace(to_move, ' ')
                self.replace(to_push, old_moved)
            elif self.map[to_push] in self.can_push[self.map[to_move]] and self.is_empty(after_push):
                old_moved = self.replace(to_move, ' ')
                old_pushed = self.replace(to_push, old_moved)
                self.replace(after_push, old_pushed)
        except IndexError:
            return "index_error"

    def replace(self, index, char):
        try:
            old_char = self.map[index]
            temp_str = list(self.map)
            temp_str[index] = char
            self.map = "".join(temp_str)
            return old_char
        except:
            pass

    def is_empty(self, index):
        return self.map[index] in self.empty

    def get_player_1(self):
        for i in range(len(self.map)):
            if self.map[i] == '1':
                return (self.index_to_pos(i))

    def get_player_2(self):
        for i in range(len(self.map)):
            if self.map[i] == '2':
                return (self.index_to_pos(i))

    def index_to_pos(self, index):
        try:
            y = 0
            x = 0
            for i in range(len(self.map)):
                if i == index:
                    return (x, y)
                elif self.map[i] == '\n':
                    y = y + 1
                    x = 0
                else:
                    x = x + 1
        except IndexError:
            return 0

    def pos_to_index(self, x, y):
        try:
            old_x = x
            for i in range(len(self.map)):
                if x == 0 and y == 0:
                    return (i)
                elif self.map[i] == '\n':
                    y = y - 1
                    x = old_x
                else:
                    x = x - 1
        except IndexError:
            return (0, 0)

    def get_display(self):
        return self.map.replace('1', 'P').replace('2', 'P')
