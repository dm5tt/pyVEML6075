from pyVEML6075 import VEML6075

dev = VEML6075('ftdi:///1')

dev.configure(False, True, VEML6075.UV_IT_800MS)

dev.start_measurement()

print(dev.read_uvb())