"""SSD1351 demo (Scrolling Marquee)."""
from ssd1351 import Display, color565
from time import sleep
from sys import implementation


def test():
    """Scrolling Marquee"""

    try:
        # Implementation dependant pin and SPI configuration
        if implementation.name == 'circuitpython':
            import board
            from busio import SPI
            from digitalio import DigitalInOut
            cs_pin = DigitalInOut(board.P0_15)
            dc_pin = DigitalInOut(board.P0_17)
            rst_pin = DigitalInOut(board.P0_20)
            spi = SPI(clock=board.P0_24, MOSI=board.P0_22)
        else:
            from machine import Pin, SPI
            cs_pin = Pin(5)
            dc_pin = Pin(17)
            rst_pin = Pin(16)
            spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))

        # Create the SSD1351 display:
        display = Display(spi, dc=dc_pin, cs=cs_pin, rst=rst_pin)
        display.clear()

        # Draw non-moving circles
        display.fill_circle(63, 63, 63, color565(27, 72, 156))
        display.fill_circle(63, 63, 53, color565(0, 0, 0))
        display.fill_circle(63, 63, 43, color565(189, 0, 36))
        display.fill_circle(63, 63, 33, color565(0, 0, 0))

        # Load Marquee image
        display.draw_image('images\Rototron128x26.raw', 0, 50, 128, 26)

        # Set up scrolling
        display.set_scroll(horiz_offset=1, vert_start_row=50,
                           vert_row_count=26, vert_offset=0, speed=1)
        display.scroll(True)

        while True:
            # Do nothing, scrolling handled by hardware
            sleep(1)

    except KeyboardInterrupt:
        display.cleanup()


test()
