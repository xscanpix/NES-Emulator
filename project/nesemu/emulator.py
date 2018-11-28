from nesemu.rom.rom import Rom


def main():
    rom = Rom()
    rom.load_rom("C:/dev/NES-Emulator/project/roms/Super Mario World.nes")

    print(rom)


if __name__ == '__main__':
    main()
