from pyVEML6075 import VEML6075


def print_sensor_values(dev):
    uva = dev.read_uva()
    uvb = dev.read_uvb()
    uva_comp = dev.read_uva_comp()
    uvb_comp = dev.read_uvb_comp()
    print("uva: " + str(uva))
    print("uvb: " + str(uvb))
    print("uva_comp: " + str(uva_comp))
    print("uvb_comp: " + str(uvb_comp))
    print("--")


dev = VEML6075('ftdi:///1')

dev.configure(False, False, VEML6075.UV_IT_50MS)
print_sensor_values(dev)

dev.configure(False, False, VEML6075.UV_IT_100MS)
print_sensor_values(dev)

dev.configure(False, False, VEML6075.UV_IT_200MS)
print_sensor_values(dev)

dev.configure(False, False, VEML6075.UV_IT_400MS)
print_sensor_values(dev)

dev.configure(False, False, VEML6075.UV_IT_800MS)
print_sensor_values(dev)