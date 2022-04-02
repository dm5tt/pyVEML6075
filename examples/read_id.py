from pyVEML6075 import VEML6075

dev = VEML6075('ftdi:///1')

print(hex(dev.read_id()))