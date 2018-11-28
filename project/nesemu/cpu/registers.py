class Registers:
    def __init__(self):
        self.A = Register(size=8)
        self.X = Register(size=8)
        self.Y = Register(size=8)
        self.SP = Register(size=8)
        self.PC = Register(size=16)
        self.P = Register(size=8)

    def __repr__(self):
        return "<Register>\nA:\t%s\nX:\t%s\nY:\t%s\nSP:\t%s\nPC:\t%s\nP:\t%s\n" \
               % (self.A, self.X, self.Y, self.SP, self.PC, self.P)


class Register:
    def __init__(self, size: int, data: int = 0):
        assert (size % 2 == 0)
        assert (0 <= data < pow(size, 2))

        self.size = size
        self.bits = list(int(x) for x in format(data, '0{}b'.format(size)))[::-1]

    def __repr__(self):
        return "".join(str(x) for x in self.bits[::-1])

    def __iter__(self):
        return iter(self.bits)

    def __getitem__(self, key):
        return self.bits[key]

    def __setitem__(self, key, value):
        assert (value in [0, 1])
        self.bits[key] = str(value)

    def __add__(self, other):
        self.add_const(int(other, 2))
        return self

    def __int__(self):
        return int(str(self), 2)

    def flip_bit(self, index: int):
        val = self.bits[index]
        self.bits[index] = 0 if val == 1 else 1

    def add_const(self, const: int):
        self.bits = list(int(x) for x in format(int(str(self), 2) + const, '0{}b'.format(self.size)))[::-1]

    def inc(self):
        self.add_const(1)

    def dec(self):
        self.add_const(-1)
