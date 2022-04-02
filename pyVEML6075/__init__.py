import time

from pyftdi.i2c import I2cController


def set_bit(val, pos):
    mask = 1 << pos
    return val | mask


def clear_bit(val, pos):
    mask = 1 << pos
    return val & ~mask


class VEML6075:
    """
    Class resembling a Vishay VEML6075 sensor and its methods
    """

    I2C_ADDR_A = 0x10

    REG_UV_CONF = 0x00
    REG_UVA_DATA = 0x07  # 2 Bytes: LSB -> MSB
    REG_UVB_DATA = 0x09  # 2 Bytes: LSB -> MSB
    REG_UVCOMP1_DATA = 0x0A  # 2 Bytes: LSB -> MSB
    REG_UVCOMP2_DATA = 0x0B  # 2 Bytes: LSB -> MSB
    REG_ID = 0x0C  # 2 Bytes: LSB -> MSB

    UV_IT_50MS = 0
    UV_IT_100MS = 1
    UV_IT_200MS = 2
    UV_IT_400MS = 3
    UV_IT_800MS = 4
    UV_IT_GROUP = [UV_IT_50MS, UV_IT_100MS, UV_IT_200MS, UV_IT_400MS, UV_IT_800MS]

    def __init__(self, ftdi_uri, uv_it=UV_IT_50MS, hdr=False, uv_af=False):
        """
        :param uv_it: Sets the integration time of the sensor (UV_IT_50MS, UV_IT_100MS, UV_IT_200MS, UV_IT_400MS, UV_IT_800MS)
        :type uv_it: int
        :param hdr: Switches On/Off HDR Mode
        :type hdr: bool
        :param uv_af: Switches On/Off Active Force Mode
        :type uv_af: bool
        """

        if uv_it not in self.UV_IT_GROUP:
            raise ValueError("Invalid integration time")

        self.i2c_addr = self.I2C_ADDR_A
        self.i2c = I2cController()
        self.i2c.configure(ftdi_uri)

        self.configure(hdr, uv_af, uv_it)

    def configure(self, hdr, uv_af, uv_it):
        """
        :param uv_it: Sets the integration time of the sensor (UV_IT_50MS, UV_IT_100MS, UV_IT_200MS, UV_IT_400MS, UV_IT_800MS)
        :type uv_it: int
        :param hdr: Switches On/Off HDR Mode
        :type hdr: bool
        :param uv_af: Switches On/Off Active Force Mode
        :type uv_af: bool
        """

        config = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_UV_CONF, self.I2C_ADDR_A], 1)[0]

        # Bit positions see Page 7 of the datasheet - as this IC is only having a single configuration register
        # I'm not going to spend an hour copy&pasting it

        # No match/case before Python 3.10 :-(
        if uv_it == self.UV_IT_50MS:
            config = clear_bit(config, 6)
            config = clear_bit(config, 5)
            config = clear_bit(config, 4)

        if uv_it == self.UV_IT_100MS:
            config = clear_bit(config, 6)
            config = clear_bit(config, 5)
            config = set_bit(config, 4)

        if uv_it == self.UV_IT_200MS:
            config = clear_bit(config, 6)
            config = set_bit(config, 5)
            config = clear_bit(config, 4)

        if uv_it == self.UV_IT_400MS:
            config = clear_bit(config, 6)
            config = set_bit(config, 5)
            config = set_bit(config, 4)

        if uv_it == self.UV_IT_800MS:
            config = set_bit(config, 6)
            config = clear_bit(config, 5)
            config = clear_bit(config, 4)

        if hdr:
            config = set_bit(config, 3)
        else:
            config = clear_bit(config, 3)

        if uv_af:
            config = set_bit(config, 1)
        else:
            config = clear_bit(config, 1)

        self.i2c.write(self.I2C_ADDR_A, [self.REG_UV_CONF, config, 0])

        # The sensor needs some time to settle after a configuration change
        time.sleep(1)

    def read_id(self):
        id = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_ID, self.I2C_ADDR_A], 2)
        id_merged = id[1] | id[0] << 8
        return id_merged

    def read_uva(self):
        uva = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_UVA_DATA, self.I2C_ADDR_A], 2)
        uva_merged = uva[1] | uva[0] << 8
        return uva_merged

    def read_uvb(self):
        uvb = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_UVB_DATA, self.I2C_ADDR_A], 2)
        uvb_merged = uvb[1] | uvb[0] << 8
        return uvb_merged

    def read_uva_comp(self):
        uva_comp = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_UVCOMP1_DATA, self.I2C_ADDR_A], 2)
        uva_comp_merged = uva_comp[1] | uva_comp[0] << 8
        return uva_comp_merged

    def read_uvb_comp(self):
        uvb_comp = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_UVCOMP2_DATA, self.I2C_ADDR_A], 2)
        uvb_comp_merged = uvb_comp[1] | uvb_comp[0] << 8
        return uvb_comp_merged

    def start_measurement(self):
        """
        Triggers a measurement.

        We cannot pull a "sampling finished"-flag here as UV_TRIG jumps to 0 immediately.
        """
        config = self.i2c.exchange(self.I2C_ADDR_A, [self.REG_UV_CONF, self.I2C_ADDR_A], 1)[0]
        config = set_bit(config, 2)
        self.i2c.write(self.I2C_ADDR_A, [self.REG_UV_CONF, config, 0])
