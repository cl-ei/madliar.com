class GBCore(object):

    def __init__(self, black, white, current_pos):
        self.black = black
        self.white = white
        self.current_pos = current_pos

        self._next = 0 if bool(black[current_pos & 0xf] & (current_pos << (current_pos >> 4))) else 1

    def _calc_next(self):
        self._next = 1