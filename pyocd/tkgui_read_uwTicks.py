# This is the simplest example, a console app, to read live-data and print it to the console.
# It demonstrates the use of pyOCD for data access and for parsing an ELF file to get a symbol's address.
# Blink.elf is a firmware file that runs on an STM32F4 board.
# This example is derived from https://github.com/mbedmicro/pyOCD/blob/master/docs/api_examples.md

import tkinter
import os

# Requires a pip install pyocd
from pyocd.core.helpers import ConnectHelper  # for ST-Link connection.
from pyocd.debug.elf.symbols import ELFSymbolProvider  # for ELF file symbol lookup.


class App:

    class DebugInterface:

        def __init__(self, elf_filepath):
            self.session = ConnectHelper.session_with_chosen_probe(
                return_first=True,  # Assuming that 1 board is attached. Or, we just use the first one.
                connect_mode='attach')  # This will keep the target running. default is 'halt' in which case target.resume() should be called.

            self.target = self.session.board.target

            self.target.elf = elf_filepath

            self.provider = ELFSymbolProvider(self.target.elf)

        def open(self):
            self.session.open()

        def read32(self, address):
            return self.target.read32(address)

        def write32(self, address, val):
            return self.target.write32(address, val)

    def __init__(self):

        self.root = tkinter.Tk()
        self.root.title(os.path.basename(__file__))
        self.main_grid = tkinter.Frame(self.root, padx=5, pady=5)
        self.main_grid.grid(column=0, row=0, sticky=tkinter.NSEW)

        self.debug_interface = App.DebugInterface("./Blink.elf")

        # Get address of variable uwTick from the .elf file.
        self.tick_addr = self.debug_interface.provider.get_symbol_value("uwTick")
        print("uwTick at address: 0x{0:08X}".format(self.tick_addr))

        tkinter.Label(self.main_grid, text='uwTicks', width=15).grid(row=1, column=0, sticky=tkinter.E)
        self.uwTicks = tkinter.IntVar()
        tkinter.Label(self.main_grid, textvariable=self.uwTicks, relief=tkinter.SUNKEN, width=15).grid(row=1, column=1, sticky=tkinter.W)

        self.btnClear = tkinter.Button(self.main_grid, text='Clear', command=lambda: self.debug_interface.write32(self.tick_addr, 0))
        self.btnClear.grid(row=2, column=1, pady=5)

        self.root.after(1, self.update)
        self.root.mainloop()

    def update(self):
        self.root.after(1000, self.update)
        if self.debug_interface.session.is_open:
            self.uwTicks.set(self.debug_interface.read32(self.tick_addr))
        else:
            self.uwTicks.set('?')
            self.debug_interface.open()

app = App()







