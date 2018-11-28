from nesemu.cpu.registers import Registers


class CPU:
    def __init__(self):
        self.registers = Registers()

    def __repr__(self):
        return "<CPU>\n{}".format(self.registers)
