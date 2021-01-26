import board
from busio import SPI
from digitalio import DigitalInOut
from ssd1351 import Display
from adafruit_ble.uart import UARTServer
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from random import randint, seed
from time import monotonic, sleep

# Configuration for CS, DC and Reset pins (Feather nRF52840 Express):
cs_pin = DigitalInOut(board.D11)
dc_pin = DigitalInOut(board.D10)
rst_pin = DigitalInOut(board.D9)

# Setup SPI bus using hardware SPI:
spi = SPI(clock=board.SCK, MOSI=board.MOSI)

# Create the SSD1351 display:
display = Display(spi, dc=dc_pin, cs=cs_pin, rst=rst_pin)
display.clear()
display.contrast(5)

NORTH = const(0)
EAST = const(1)
SOUTH = const(2)
WEST = const(3)
UP = ButtonPacket.UP
DOWN = ButtonPacket.DOWN
LEFT = ButtonPacket.LEFT
RIGHT = ButtonPacket.RIGHT
BORDER_WIDTH = const(2)
WALL_HORIZ_LENGTH = const(27)
WALL_VERT_LENGTH = const(44)
START_ROOM_X = const(5)
START_ROOM_Y = const(10)

RED = const(0XF800)
GREEN = const(0X07E0)
BLUE = const(0X001F)
YELLOW = const(0XFFE0)
CHARTREUSE = const(0XCFE0)
ORANGE = const(0XFC00)
INDIGO = const(0xB81F)
CYAN = const(0X07FF)
ROOM_COLORS = [RED, GREEN, BLUE, YELLOW, CHARTREUSE, ORANGE, INDIGO, CYAN]


class Mario(object):
    """Mario."""
    def __init__(self, path, w, h, screen_width, screen_height,
                 frames, display):
        """Initialize Mario.
        Args:
            path (string): Path of sprite image.
            w, h (int): Width and height of image.
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            frames(int): Sprite frames in each direction
            display (SSD1351): OLED display object.
        """
        self.buf = display.load_sprite(path, w, h)
        self.w = w
        self.h = h // frames
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.display = display
        self.x = BORDER_WIDTH
        self.y = self.screen_height // 2 - self.h // 2
        self.prev_x = self.x
        self.prev_y = self.y
        self.facing = RIGHT  # Initially facing left
        self.frame = 1  # Current sprite frame
        self.walking = False

    def advance_frame(self):
        """Advance sprite frame."""
        self.frame += 1
        if self.facing == RIGHT and self.frame > 6:
            self.frame = 4
        elif self.facing == LEFT and self.frame > 3:
            self.frame = 1

    def update_pos(self, room):
        """Update Mario's position.
        Args:
            room (obj): Mario's current room
        """
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        border = BORDER_WIDTH
        screen_width = self.screen_width
        screen_height = self.screen_height
        self.prev_x = x
        self.prev_y = y
        if self.walking:
            # Check for collision
            collision = room.check_collision(x, y, w, h, self.direction)
            # Check for walking (Mario 13x15px top left is origin)
            if self.direction == UP:
                if y < border:
                    # Move room up
                    self.y = screen_height - border - h
                    self.prev_y = self.y
                    return [room.room_x, room.room_y - 1]
                elif not collision:
                    self.y -= 1
                    self.advance_frame()
                    return [room.room_x, room.room_y]
            elif self.direction == DOWN:
                if y > screen_height - (h + border):
                    # Move room down
                    self.y = border
                    self.prev_y = self.y
                    return [room.room_x, room.room_y + 1]
                elif not collision:
                    self.y += 1
                    self.advance_frame()
                    return [room.room_x, room.room_y]
            elif self.direction == LEFT:
                if x < border:
                    # Move room left
                    self.x = screen_width - border - w
                    self.prev_x = self.x
                    return [room.room_x - 1, room.room_y]
                elif not collision:
                    self.x -= 1
                    if self.facing == LEFT:
                        self.advance_frame()
                    else:
                        self.facing = LEFT
                        self.frame = 1
                    return [room.room_x, room.room_y]
            elif self.direction == RIGHT:
                if x > screen_width - (w + border):
                    # Move room right
                    self.x = border
                    self.prev_x = self.x
                    return [room.room_x + 1, room.room_y]
                elif not collision:
                    self.x += 1
                    if self.facing == RIGHT:
                        self.advance_frame()
                    else:
                        self.facing = RIGHT
                        self.frame = 4
                    return [room.room_x, room.room_y]
        # Stop
        if self.facing == LEFT:
            self.frame = 1
        else:
            self.frame = 4
        return [room.room_x, room.room_y]

    def draw(self):
        """Draw sprite."""
        x = self.x
        y = self.y
        prev_x = self.prev_x
        prev_y = self.prev_y
        w = self.w
        h = self.h

        # Determine direction and remove previous portion of sprite
        if prev_x > x:
            # Left
            self.display.fill_vrect(x + w, prev_y, 1, h, 0)
        elif prev_x < x:
            # Right
            self.display.fill_vrect(x - 1, prev_y, 1, h, 0)
        if prev_y > y:
            # Upward
            self.display.fill_vrect(prev_x, y + h, w, 1, 0)
        elif prev_y < y:
            # Downward
            self.display.fill_vrect(prev_x, y - 1, w, 1, 0)

        size = self.w * self.h * 2
        offset = size * (self.frame - 1)
        self.display.draw_sprite(self.buf[offset: offset + size], x, y, w, h)

    def clear(self):
        """Clear sprite."""
        self.display.fill_rectangle(self.x, self.y, self.w, self.h, 0)


class Room(object):
    """Generate and track all walls in a room."""
    def __init__(self, room_x, room_y, max_room_x, max_room_y, screen_width,
                 screen_height, display):
        """Initialize room.
        Args:
            room_x, room_y (int): Current room grid coordinates
            max_room_x, max_room_y (int): Maximum rooms in X,Y plane
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            display (SSD1351): OLED display object.
        Notes:
            Rooms are laid out on an 16x16 grid.
        """
        self.room_x = room_x
        self.room_y = room_y
        self.max_room_x = max_room_x
        self.max_room_y = max_room_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.display = display
        self.walls = []
        self.generate_walls()

    def two_bits(self, n):
        """Breaks 16 bit binary number into bit pairs.
        Args:
            n (int): Number to split into double bits.
        """
        mask = 0b11
        for i in range(8):
            yield n & mask
            n >>= 2

    def generate_walls(self):
        """Generate room walls."""
        outer_pillars = [[0, 0, 1], [25, 0, 1], [75, 0, 1], [100, 0, 1],
                         [125, 0, 2], [125, 84, 2], [125, 126, 3],
                         [100, 126, 3], [50, 126, 3], [25, 126, 3],
                         [0, 126, 0], [0, 42, 0]]
        inner_pillars = [[25, 42], [50, 42], [75, 42], [100, 42], [25, 84],
                         [50, 84], [75, 84], [100, 84]]

        # Seed random to room coordinates so rooms are unique
        seed(self.room_x | (self.room_y << 4))
        r = randint(0, 65536)
        # Set room color
        self.color = ROOM_COLORS[r >> 2 & 0b111]
        # Locked doors
        door_north = [50, 0, 1]
        door_east = [125, 42, 2]
        door_south = [75, 126, 3]
        door_west = [0, 84, 0]
        if self.room_x == 0:
            self.walls.append(Wall(door_west, self.color, self.display))
        if self.room_y == 0:
            self.walls.append(Wall(door_north, self.color, self.display))
        if self.room_x >= self.max_room_x - 1:
            self.walls.append(Wall(door_east, self.color, self.display))
        if self.room_y >= self.max_room_y - 1:
            self.walls.append(Wall(door_south, self.color, self.display))

        # Outer walls
        for pillar in outer_pillars:
            self.walls.append(Wall(pillar, self.color, self.display))

        # Inner walls
        room_inner_dirs = list(self.two_bits(r))
        for index, coords in enumerate(inner_pillars):
            pillar = [coords[0], coords[1], room_inner_dirs[index]]
            self.walls.append(Wall(pillar, self.color, self.display))

    def check_collision(self, obj_left, obj_top, obj_width, obj_height,
                        direction):
        """Check if object is colliding with items in room.
        Args:
            obj_left, obj_top (int): object origin coordinates
            obj_width, object_height (int): object dimensions
            direction (int): direction object is travelling
        """
        obj_right = obj_left + obj_width - 1
        obj_bottom = obj_top + obj_height - 1
        # Check all walls
        for wall in self.walls:
            if wall.intersects(obj_left, obj_top, obj_right, obj_bottom,
                               direction):
                return True
        return False


class Wall(object):
    """A solid wall."""
    def __init__(self, pillar, color, display):
        """Initialize wall.
        Args:
            pillar ([int]): [X coord, Y coord, direction]
            display (SSD1351): OLED display object.
            color (int): RGB565 color
        """
        x, y, direction = pillar
        self.color = color
        if direction == NORTH:
            self.w = BORDER_WIDTH
            self.h = WALL_VERT_LENGTH
            self.left = x
            self.top = y - WALL_VERT_LENGTH + 2
        elif direction == EAST:
            self.w = WALL_HORIZ_LENGTH
            self.h = BORDER_WIDTH
            self.left = x
            self.top = y
        elif direction == SOUTH:
            self.w = BORDER_WIDTH
            self.h = WALL_VERT_LENGTH
            self.left = x
            self.top = y
        elif direction == WEST:
            self.w = WALL_HORIZ_LENGTH
            self.h = BORDER_WIDTH
            self.left = x - WALL_HORIZ_LENGTH + 2
            self.top = y
        else:
            print('Invalid direction: {0:b}'.format(direction))

        self.right = self.left + self.w - 1
        self.bottom = self.top + self.h - 1
        self.draw_wall(display)

    def draw_wall(self, display):
        """Draw wall.
        Args:
            display (SSD1351): OLED display object.
        """
        display.fill_rectangle(self.left, self.top, self.w, self.h, self.color)

    def intersects(self, obj_left, obj_top, obj_right, obj_bottom, direction):
        """Determine if object intersects wall.
        Args:
            obj_left, obj_top, obj_right, obj_bottom(int): object boundaries
            direction (int): direction object is travelling
        """
        if direction == UP:
            # Object travelling UP
            if (obj_left <= self.right and obj_right >= self.left and
               obj_top - 1 == self.bottom):
                return True
            else:
                return False
        elif direction == DOWN:
            # Object travelling DOWN
            if (obj_left <= self.right and obj_right >= self.left and
               obj_bottom + 1 == self.top):
                return True
            else:
                return False
        elif direction == LEFT:
            # Object travelling LEFT
            if (obj_top <= self.bottom and obj_bottom >= self.top and
               obj_left - 1 == self.right):
                return True
            else:
                return False
        elif direction == RIGHT:
            # Object travelling RIGHT
            if (obj_top <= self.bottom and obj_bottom >= self.top and
               obj_right + 1 == self.left):
                return True
            else:
                return False
        else:
            # Unknown
            return False

# Initialize Mario
mario = Mario('images/Mario13x96.raw', 13, 96, 127, 128, 6, display)
# Create first room
room = Room(START_ROOM_X, START_ROOM_Y, 16, 16, 127, 128, display)
mario.update_pos(room)
mario.draw()
uart_server = UARTServer()

while True:
    uart_server.start_advertising()
    # Wait for BLE connection
    while not uart_server.connected:
        pass

    while uart_server.connected:
        timer = monotonic()
        if uart_server.in_waiting:  # Check for BLE packets
            packet = Packet.from_stream(uart_server)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:  # Gamepad pressed
                    # Walking
                    mario.walking = True
                    mario.direction = packet.button
                else:
                    # Stopped
                    mario.walking = False
                    # Draw standing still
                    mario.update_pos(room)
                    mario.draw()
        # Draw Mario waling
        if mario.walking:
            room_x, room_y = mario.update_pos(room)
            if [room_x, room_y] != [room.room_x, room.room_y]:
                # room.changed
                display.clear()
                room = Room(room_x, room_y, 16, 16, 127, 128, display)
            mario.draw()

        # Adjust speed to 30 FPS
        timer_dif = .033333333 - (monotonic() - timer)
        if timer_dif > 0:
            sleep(timer_dif)
