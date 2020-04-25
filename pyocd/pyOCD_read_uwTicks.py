# This is the simplest example, a console app, to read live-data and print it to the console.
# It demonstrates the use of pyOCD for data access and for parsing an ELF file to get a symbol's address.
# Blink.elf is a firmware file that runs on an STM32F4 board.
# This example is derived from https://github.com/mbedmicro/pyOCD/blob/master/docs/api_examples.md

# Requires a pip install pyocd
from pyocd.core.helpers import ConnectHelper  # for ST-Link connection.
from pyocd.debug.elf.symbols import ELFSymbolProvider  # for ELF file symbol lookup.
import time # for sleep.

session = ConnectHelper.session_with_chosen_probe(
    return_first=True,      # Assuming that 1 board is attached. Or, we just use the first one.
    connect_mode='attach')  # This will keep the target running. default is 'halt' in which case target.resume() should be called.

session.open()

target = session.board.target

target.elf = "./Blink.elf" # Set ELF file on target.

# Look up address of "uwTick", the millisecond counter in firmware.
provider = ELFSymbolProvider(target.elf)
tick_addr = provider.get_symbol_value("uwTick")
print("uwTick at address: 0x{0:08X}".format(tick_addr))

# Read uwTick and expect it to return a changing tick count.
# It should change roughly 1000 msec each time by virtue of the sleep(1).
# Just loop 10 times while sleeping 1 second and print the millisecond-counter.
for i in range(1, 10):
    val = target.read32(tick_addr)
    print(val)
    time.sleep(1)


