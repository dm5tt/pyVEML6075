from setuptools import setup

setup(
    name='pyVEML6075',
    version='0.0.1',
    packages=['pyVEML6075'],
    install_requires=['pyFTDI==0.54.0'],
    url='https://github.com/dm5tt/pyVEML6075',
    license='GNU GPLv3',
    author='Holger Adams',
    author_email='mail@dm5tt.de',
    description='\'Package to read out UVA/UVB measurements of a Vishay VEML6075 sensor using I2C via pyFTDI\''
)
