from nesemu.helpers.binary import Binary

SIZE_HEADER = 16
SIZE_TRAINER = 512
SIZE_PRG_BLOCK = 16384
SIZE_CHR_BLOCK = 8192
SIZE_PC_INST_ROM = 8192
SIZE_PC_PROM = 32
SIZE_TITLE = 128

class Rom:
    def __init__(self):
        self.data = None
        self.header = None
        self.trainer = None
        self.prg_rom_data = None
        self.chr_rom_data = None
        self.pc_inst_rom = None
        self.pc_prom = None
        self.rest = None

    def __repr__(self):
        rv = ""
        rv += "<Header>\n"
        for key, val in self.header.items():
            rv += "<{} => {}>\n".format(key, val)
        return rv

    def load_rom(self, path):
        with open(path, "rb") as file:
            self.data = file.read()

        cursor = 0
        header_data = self.data[cursor:cursor + SIZE_HEADER]
        self.header = {
            "bytes": header_data,
            "header_const": header_data[0:3].decode("utf-8"),
            "size_prgrom": int.from_bytes(header_data[3:4], 'little'),
            "size_chrrom": int.from_bytes(header_data[4:5], 'little'),
            "flags6": Binary(int.from_bytes(header_data[5:6], 'little'), 8),
            "flags7": Binary(int.from_bytes(header_data[6:7], 'little'), 8),
            "size_prgram": int.from_bytes(header_data[7:8], 'little'),
            "flags9": Binary(int.from_bytes(header_data[8:9], 'little'), 8),
            "flags10": Binary(int.from_bytes(header_data[9:10], 'little'), 8),
            "zero_pad": header_data[10:16]
        }
        cursor += SIZE_HEADER

        assert self.header['flags6'][0] == 0, "Mirroring is not 0"
        assert self.header['flags6'][1] == 0, "ROM contains PRG RAM, not handled yet"
        assert self.header['flags6'][3] == 0, "Ignore mirroring bit is not 0"
        assert self.header['flags6'][4:] == [0, 1, 0, 0], "Lower nybble of ROM Mapper"

        assert self.header['flags7'][0] == 1, "Non VS Unisystem not supported"
        assert self.header['flags7'][1] == 0, "PlayChoice-10 not supported"
        assert self.header['flags7'][2:4] == [0, 0], "NES 2.0 format not supported"
        assert self.header['flags7'][4:] == [0, 1, 0, 1], "Upper nybble of ROM Mapper"

        assert self.header['flags9'][0] == 0, "Not NTSC"
        assert self.header['flags9'][1:] == [0, 0, 0, 0, 0, 0, 0], "Reserved"

        assert self.header['flags10'][0:] == [0, 0, 0, 0, 0, 0, 0, 0], "Flags 10 bad"

        if self.header['flags6'][2] == 1:  # Contains trainer
            self.trainer = self.data[cursor:cursor + SIZE_TRAINER]
            cursor += SIZE_TRAINER

        self.prg_rom_data = self.data[cursor:cursor + (SIZE_PRG_BLOCK * self.header['size_prgrom'])]
        cursor += SIZE_PRG_BLOCK

        self.chr_rom_data = self.data[cursor:cursor + (SIZE_CHR_BLOCK * self.header['size_chrrom'])]
        cursor += SIZE_CHR_BLOCK


