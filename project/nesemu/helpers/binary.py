class Binary:
    def __init__(self, data: int, size: int):
        self.data = data
        self.size = size
        self.bits = list()
        for i in range(self.size):
            self.bits.append((data >> i) & 1)

    def __iter__(self):
        return iter(self.bits)

    def __getitem__(self, item):
        return self.bits[item]

    def __repr__(self):
        return format(self.data, "0{}b".format(self.size))
