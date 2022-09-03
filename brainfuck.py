import sys


try:
    import msvcrt
    getch = msvcrt.getch

except ImportError:
    # refer to: https://github.com/pocmo/Python-Brainfuck/blob/master/getch.py
    import termios
    import tty

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class BrainFuck(object):

    def __init__(self):
        self._ram = [0] * 0x10000
        self._rom = ''
        self._ram_i = 0
        self._rom_i = 0

    def load(self, rom):
        self._rom_i = 0
        self._rom = rom

    def run(self):
        rom_len = len(self._rom)
        while self._rom_i < rom_len:
            self._execute_once()

    def _move_ram_i(self, offset):
        self._ram_i += offset
        self._ram_i = self._ram_i % len(self._ram)

    def _goto_token(self, token):
        rom_i = self._rom_i
        rom = self._rom
        if token == ']':
            self._rom_i += rom[rom_i:].index(token)
        elif token == '[':
            self._rom_i = rom[:rom_i].rindex(token)
        else:
            pass

    def _execute_once(self):
        ch = self._rom[self._rom_i]

        if ch == '+':
            self._ram[self._ram_i] += 1
            if self._ram[self._ram_i] > 0xFF:
                self._ram[self._ram_i] = 0
        elif ch == '-':
            self._ram[self._ram_i] -= 1
            if self._ram[self._ram_i] < 0:
                self._ram[self._ram_i] = 0xFF
        elif ch == '>':
            self._move_ram_i(1)
        elif ch == '<':
            self._move_ram_i(-1)
        elif ch == '[':
            if self._ram[self._ram_i] == 0:
                self._goto_token(']')
        elif ch == ']':
            if self._ram[self._ram_i] != 0:
                self._goto_token('[')
        elif ch == '.':
            sys.stdout.write(chr(self._ram[self._ram_i]))
        elif ch == ',':
            self._ram[self._ram_i] = ord(getch())

        self._rom_i += 1


if __name__ == '__main__':
    file_path = sys.argv[1]
    with open(file_path) as fd:
        file_data = fd.read()
    bf = BrainFuck()
    bf.load(file_data)
    bf.run()

