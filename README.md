**Description**

This is a small Python3 package that enables you to read out Vishay VEML6075 sensor using a FTDI chip. 

**Hardware Setup**

The FTDI is accessed using the pyFTDI library.

I tested this implementation utilizing the ADBUS interface of a FTDI FT2232H.

[Please have a look at the pyFTDI documentation how to wire up I2C. Scroll down to the bottom.](https://eblot.github.io/pyftdi/api/i2c.html)