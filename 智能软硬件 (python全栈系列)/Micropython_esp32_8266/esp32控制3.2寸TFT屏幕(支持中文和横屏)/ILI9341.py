import time
import ustruct,struct
import framebuf

_COLUMN_SET = const(0x2a)
_PAGE_SET = const(0x2b)
_RAM_WRITE = const(0x2c)
_RAM_READ = const(0x2e)
_DISPLAY_ON = const(0x29)
_WAKE = const(0x11)
_LINE_SET = const(0x37)

#字库文件
ch_path='HZK16'

def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

def color(color1):
    return (color1[0] & 0xf8) << 8 | (color1[1]  & 0xfc) << 3 | color1[2]  >> 3


class ILI9341:
    """
    A simple driver for the ILI9341/ILI9340-based displays.

    #lcd = ili9341.ILI9341(spi, cs=Pin(33), dc=Pin(5), rst=Pin(4),scroll=True)  #True<=>Landscape,False<=>Portrait
    #size is lcd.width * lcd.height


    >>> import ili9341
    >>> from machine import Pin, SPI
    >>> spi = SPI(miso=Pin(12), mosi=Pin(13, Pin.OUT), sck=Pin(14, Pin.OUT))  #240*320 
    #or add : scroll = True ->scroll 320*240
    >>> display = ili9341.ILI9341(spi, cs=Pin(0), dc=Pin(5), rst=Pin(4))
    >>> display.fill(ili9341.color565(0xff, 0x11, 0x22))
    >>> display.pixel(120, 160, 0)
    """

    width = 240
    height = 320

    def __init__(self, spi, cs, dc, rst,scroll=False):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.reset()
        self._scroll = scroll
        self.init()

    def init(self):
        if self._scroll:  #横屏
            scroll_cmd = b'\x28'
            self.width = 320
            self.height = 240
        else:
            scroll_cmd = b'\x48'
        for command, data in (
            (0xef, b'\x03\x80\x02'),
            (0xcf, b'\x00\xc1\x30'),
            (0xed, b'\x64\x03\x12\x81'),
            (0xe8, b'\x85\x00\x78'),
            (0xcb, b'\x39\x2c\x00\x34\x02'),
            (0xf7, b'\x20'),
            (0xea, b'\x00\x00'),
            (0xc0, b'\x23'),  # Power Control 1, VRH[5:0]
            (0xc1, b'\x10'),  # Power Control 2, SAP[2:0], BT[3:0]
            (0xc5, b'\x3e\x28'),  # VCM Control 1
            (0xc7, b'\x86'),  # VCM Control 2
            (0x36, scroll_cmd),  # Memory Access Control  0x48 竖屏  0x28 横屏
            (0x3a, b'\x55'),  # Pixel Format
            (0xb1, b'\x00\x18'),  # FRMCTR1
            (0xb6, b'\x08\x82\x27'),  # Display Function Control
            (0xf2, b'\x00'),  # 3Gamma Function Disable
            (0x26, b'\x01'),  # Gamma Curve Selected
            (0xe0,  # Set Gamma
             b'\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00'),
            (0xe1,  # Set Gamma
             b'\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f'),
        ):
            self._write(command, data)
        self._write(_WAKE)
        time.sleep_ms(120)
        self._write(_DISPLAY_ON)
        
        #
        


    def reset(self):
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

    def _write(self, command, data=None):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([command]))
        self.cs.value(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def _block(self, x0, y0, x1, y1, data=None):
        self._write(_COLUMN_SET, ustruct.pack(">HH", x0, x1))
        self._write(_PAGE_SET, ustruct.pack(">HH", y0, y1))
        if data is None:
            return self._read(_RAM_READ, (x1 - x0 + 1) * (y1 - y0 + 1) * 3)
        self._write(_RAM_WRITE, data)

    def _read(self, command, count):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([command]))
        data = self.spi.read(count)
        self.cs.value(1)
        return data

    def pixel(self, x, y, color=None):
        if color is None:
            r, b, g = self._block(x, y, x, y)
            return color565(r, g, b)
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return
        self._block(x, y, x, y, ustruct.pack(">H", color))
   
    def pixel2(self, x, y,scale=0, color=None):
        if scale <= x <self.width-scale and scale <= y < self.height-scale:
            for i in range(-scale,scale):
                for j in range(-scale,scale):
                    self.pixel(x+i,y+j,color)

    def fill_rectangle(self, x, y, w, h, color):
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, w))
        h = min(self.height - y, max(1, h))
        self._block(x, y, x + w - 1, y + h - 1, b'')
        chunks, rest = divmod(w * h, 512)
        if chunks:
            data = ustruct.pack(">H", color) * 512
            for count in range(chunks):
                self._data(data)
        data = ustruct.pack(">H", color) * rest
        self._data(data)

    def fill(self, color):
        self.fill_rectangle(0, 0, self.width, self.height, color)
    
    def draw(self, x, y, x1, y1, color=0x0000):
        if x == x1:
            if y1<y:
                y,y1=y1,y
            for m in range(y,y1+1):
                self.pixel(x,m,color)
        elif y==y1:
            if x1<x:
                x,x1=x1,x
            for n in range(x,x1+1):
                self.pixel(n,y,color)
        else :
            if x1 < x :
                x, x1 = x1, x
                y, y1 = y1, y
            r = (y1 - y) / (x1 - x)
            while x <= x1:
                self.pixel(round(x),round(y),color)
                x=x+1
                y=y+r

    ##中文char
    def chchar(self,x,y,code,origin=1,color = 0x0000,background=0xffff):
        if ((x+16)>= self.width) or ((y+16)>= self.height):
            return
        f = open(ch_path,'rb')
        if origin:
            a = code.encode('gb2312')
        area = a[0]-160
        index = a[1]-160
        offset = (94*(area-1)+(index-1))*32
        f.seek(offset)
        btxt=f.read(32)
        f.close()
        for i in range(16):
            t1 = btxt[i<<1]
            t1 = int(bin(t1)[2:])
            t1 = "%08d" % t1

            t2 = btxt[(i<<1)+1]
            t2 = int(bin(t2)[2:])
            t2 = "%08d" % t2
            t = t1+t2
            for j in range(16):
                if t[j]=='1':
                    self.pixel((x+j),(y+i),color)
        #end

    def chstrH(self,x,y,code,num=1,origin=1,color = 0x0000,background=0xffff):
        for mm in range(num):
            if (x+16*mm+16<self.width):
                self.chchar(x+16*mm,y,code[mm],origin,color,background)
            else:
                break

    def chstrV(self,x,y,code,num=1,origin=1,color = 0x0000,background=0xffff):
        for mm in range(num):
            if (y+16*mm+16 < self.height):
                self.chchar(x,y+16*mm,code[mm],origin,color,background)
            else:
                break


    def char(self, char, x, y, color=0x0000, background=0xffff):
        buffer = bytearray(8)
        framebuffer = framebuf.FrameBuffer1(buffer, 8, 8)
        framebuffer.text(char, 0, 0)
        color = ustruct.pack(">H", color)
        background = ustruct.pack(">H", background)
        data = bytearray(2 * 8 * 8)
        for c, byte in enumerate(buffer):
            for r in range(8):
                if byte & (1 << r):
                    data[r * 8 * 2 + c * 2] = color[0]
                    data[r * 8 * 2 + c * 2 + 1] = color[1]
                else:
                    data[r * 8 * 2 + c * 2] = background[0]
                    data[r * 8 * 2 + c * 2 + 1] = background[1]
        self._block(x, y, x + 7, y + 7, data)

    def text(self, text, x, y,color=0x0000, background=0xffff, wrap=None,
             vwrap=None, clear_eol=False):
        if wrap is None:
            wrap = self.width - 8
        if vwrap is None:
            vwrap = self.height - 8
        tx = x
        ty = y

        def new_line():
            nonlocal tx, ty

            tx = x
            ty += 8
            if ty >= vwrap:
                ty = y

        for char in text:
            if char == '\n':
                if clear_eol and tx < wrap:
                    self.fill_rectangle(tx, ty, wrap - tx + 7, 8, background)
                new_line()
            else:
                if tx >= wrap:
                    new_line()
                self.char(char, tx, ty, color, background)
                tx += 8
        if clear_eol and tx < wrap:
            self.fill_rectangle(tx, ty, wrap - tx + 7, 8, background)

    

#######################
#ctrl k c, ctrl k u
    # def _set_window(self, x0, y0, x1, y1):
    #     # Column Address Set
    #     self._write(0x2A)
    #     self._data(struct.pack('B',( (x0>>8) & 0xFF)  ))
    #     self._data(struct.pack('B', (x0 & 0xFF) )    )
    #     self._data(struct.pack('B', ( (y0>>8) & 0xFF)) )
    #     self._data(struct.pack('B', (y0 & 0xFF)) )
    #     #self._write_words(((x0>>8) & 0xFF, x0 & 0xFF, (y0>>8) & 0xFF, y0 & 0xFF))
    #     # Page Address Set
    #     self._write(0x2B)
    #     self._data(struct.pack('B',((x1>>8) & 0xFF  )))
    #     self._data(struct.pack('B',( x1 & 0xFF )))
    #     self._data(struct.pack('B',( (y1>>8) & 0xFF )))
    #     self._data(struct.pack('B',( y1 & 0xFF )))
        
    #     #self._write_words(((x1>>8) & 0xFF, x1 & 0xFF, (y1>>8) & 0xFF, y1 & 0xFF))
    #     # Memory Write
    #     self._write(0x2C)

    # def _set_image_headers(self, f):
    #     headers = list()
    #     if f.read(2) != b'BM':
    #         raise OSError('Not a valid BMP image')
    #     for pos in (10, 18, 22):                                 # startbit, width, height
    #         f.seek(pos)
    #         headers.append(struct.unpack('<H', f.read(2))[0])    # read double byte
    #     return headers

    # def _get_image_points(self, pos, width, height):
    #     if isinstance(pos, (list, tuple)):
    #         x, y = pos
    #     else:
    #         x = 0 if width == self.width else (self.width-width)//2
    #         y = 0 if height == self.height else (self.height-height)//2
    #     return x, y

    # # Using in renderBmp method
    # def _render_bmp_image(self, filename, pos):
    #     path = 'images/'
    #     memread = 480
    #     with open(path + filename, 'rb') as f:
    #         startbit, width, height = self._set_image_headers(f)
    #         if width < self.width:
    #             width -= 1
    #         x, y = self._get_image_points(pos, width, height)
    #         self._set_window(x, (width)+x, y, (height)+y)
    #         f.seek(startbit)
    #         while True:
    #             try:
    #                 data = bytearray(f.read(memread))
    #                 #self._reverse(data, len(data))
    #                 data = sorted(data,reverse=True)
    #                 data = bytearray(data)
    #                 self._data(data)
    #             except OSError: break

