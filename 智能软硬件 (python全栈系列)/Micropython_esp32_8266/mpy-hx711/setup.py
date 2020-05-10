import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip


setup(
    cmdclass={'sdist': sdist_upip.sdist},
    name='micropython-hx711',
    py_modules=['hx711'],
    version='1.0.1',
    description='Micropython driver for the HX711',
    long_description='Micropython driver for the HX711 24-Bit Analog-to-Digital Converter',
    keywords=['micropython', 'hx711'],
    url='https://github.com/SergeyPiskunov/micropython-hx711',
    author='Sergey Piskunov',
    author_email='sergey.piskunoff@gmail.com',
    maintainer='Sergey Piskunov',
    maintainer_email='sergey.piskunoff@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ],
)
