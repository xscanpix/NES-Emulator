# binary.py

def bin(s: str):
    return str(s) if s<=1 else bin(s>>1) + str(s&1)

def bin_list(s: str):
    return list([int(x) for x in bin(s)])

class Binary:
    def __init__(self, data: int, size: int, endianness: str='little'):
        assert(size % 2 == 0)
        assert(data >= 0 and data < pow(size, 2))
        assert(endianness == 'little' or endianness == 'big')

        self.size = size
        self.endianness = endianness

        if endianness == 'little':
            self.data = bin_list(data)[::-1]
        else:
            self.data = bin_list(data)

    def __repr__(self):
        return '<Binary "{}", {}>'.format(''.join(str(e) for e in self.data[::-1]), self.endianness)

    def __iter__(self):
        return self.data.iter()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        assert(value in [0, 1])

        self.data[key] = str(value)

    def flip_bit(self, index):
        val = self.data[index]
        self.data[index] = 0 if val == 1 else 1
