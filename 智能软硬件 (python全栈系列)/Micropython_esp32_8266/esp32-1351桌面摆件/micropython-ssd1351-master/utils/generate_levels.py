"""Arkanoid code used to generate level binary files.

Notes:
    The binary level files are comprised of 3 bytes (X, Y and color)
    for each brick.
    XY coordinates indicate the top left corner of the brick.
    Bricks are 13 pixels wide by 7 high.
    Common X values:
        6, 19, 32, 45, 58, 71, 84, 97, 110 (9 columns across)
        16, 28, 40, 52, 64, 76, 88, 100 (8 columns across)
    Common Y values:
        27, 34, 41, 48, 55, 62, 69, 76 (8 rows is the maximum)
    Color byte (0: Red, 1: Yellow, 2: Blue, 3: Pink, 4: Green)
"""


def generate_level01():
    """Generate the bricks."""
    bricks = bytearray(120)
    index = 0
    for row in range(27, 57, 6):
        brick_color = (row - 27) // 6
        for col in range(16, 112, 12):
            bricks[index] = col
            bricks[index + 1] = row
            bricks[index + 2] = brick_color
            print('index: {0} = {1},{2} -> {3}'.format(index,
                                                       bricks[index],
                                                       bricks[index + 1],
                                                       bricks[index + 2]))
            index += 3
    return bricks


def generate_level02():
    """Generate the bricks."""
    bricks = bytearray(108)
    index = 0
    col_x = 0
    column_counts = [8, 7, 6, 5, 4, 3, 2, 1]
    brick_colors = [2, 4, 1, 3, 0, 1, 4, 2]
    for col in range(16, 112, 12):
        row_y = 0
        for row in range(27, 75, 6):
            if row_y >= column_counts[col_x]:
                break
            brick_color = brick_colors[col_x]
            bricks[index] = col
            bricks[index + 1] = row
            bricks[index + 2] = brick_color
            print('index: {0} = {1},{2} -> {3}'.format(index,
                                                       bricks[index],
                                                       bricks[index + 1],
                                                       bricks[index + 2]))
            index += 3
            row_y += 1
        col_x += 1
    return bricks


def generate_level03():
    """Generate the bricks."""
    pi = [
        [44, 27, 4],
        [70, 27, 4],
        [31, 33, 4],
        [44, 33, 4],
        [57, 33, 0],
        [70, 33, 4],
        [83, 33, 4],
        [44, 39, 0],
        [57, 39, 0],
        [70, 39, 0],
        [31, 45, 0],
        [44, 45, 0],
        [70, 45, 0],
        [83, 45, 0],
        [31, 51, 0],
        [57, 51, 0],
        [83, 51, 0],
        [31, 57, 0],
        [44, 57, 0],
        [70, 57, 0],
        [83, 57, 0],
        [44, 63, 0],
        [57, 63, 0],
        [70, 63, 0],
        [57, 69, 0],
    ]
    bricks = bytearray(len(pi) * 3)
    index = 0
    for row in pi:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def generate_level04():
    """Generate the bricks."""
    pi = [
        [6, 27, 1],
        [110, 27, 1],
        [6, 33, 2],
        [19, 33, 2],
        [97, 33, 2],
        [110, 33, 2],
        [6, 39, 3],
        [19, 39, 3],
        [32, 39, 3],
        [84, 39, 3],
        [97, 39, 3],
        [110, 39, 3],
        [6, 45, 4],
        [19, 45, 4],
        [32, 45, 4],
        [45, 45, 4],
        [71, 45, 4],
        [84, 45, 4],
        [97, 45, 4],
        [110, 45, 4],
        [16, 51, 0],
        [28, 51, 0],
        [40, 51, 0],
        [52, 51, 0],
        [64, 51, 0],
        [76, 51, 0],
        [88, 51, 0],
        [100, 51, 0],
    ]
    bricks = bytearray(len(pi) * 3)
    index = 0
    for row in pi:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def generate_level05():
    """Generate the bricks."""
    rgb = [
        [6, 27, 0],
        [6, 33, 0],
        [6, 39, 0],
        [6, 45, 0],
        [6, 51, 0],
        [19, 27, 0],
        [19, 33, 0],
        [19, 39, 0],
        [19, 45, 0],
        [19, 51, 0],
        [52, 27, 4],
        [52, 33, 4],
        [52, 39, 4],
        [52, 45, 4],
        [52, 51, 4],
        [64, 27, 4],
        [64, 33, 4],
        [64, 39, 4],
        [64, 45, 4],
        [64, 51, 4],
        [97, 27, 2],
        [97, 33, 2],
        [97, 39, 2],
        [97, 45, 2],
        [97, 51, 2],
        [110, 27, 2],
        [110, 33, 2],
        [110, 39, 2],
        [110, 45, 2],
        [110, 51, 2],
    ]
    bricks = bytearray(len(rgb) * 3)
    index = 0
    for row in rgb:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def generate_level06():
    """Generate the bricks."""
    face = {
        27: (28, 40, 52, 64, 76, 88),
        33: (16, 28, 52, 64, 88, 100),
        39: (16, 28, 52, 64, 88, 100),
        45: (16, 28, 40, 52, 64, 76, 88, 100),
        51: (16, 28, 40, 52, 64, 76, 88, 100),
        57: (16, 40, 52, 64, 76, 100),
        63: (16, 28, 88, 100),
        69: (28, 40, 52, 64, 76, 88)}

    bricks = bytearray(sum([len(v) for v in face.values()]) * 3)
    index = 0
    for k, v in face.items():
        for x in v:
            bricks[index] = x
            bricks[index + 1] = k
            bricks[index + 2] = 1
            index += 3
    return bricks


def generate_level07():
    """Generate the bricks."""
    bricks = bytearray(9 * 6 * 3)
    color = 0
    index = 0
    for x in range(6, 111, 13):
        for y in range(27, 63, 7):
            bricks[index] = x
            bricks[index + 1] = y
            bricks[index + 2] = color
            index += 3
            color += 1
            if color >= 5:
                color = 0
    return bricks


def generate_level08():
    """Generate the bricks."""
    bricks = bytearray(8 * 5 * 3)
    colors = [2, 0, 1, 3, 4]
    index = 0
    col_x = 0
    for x in range(6, 111, 26):
        for y in range(27, 77, 7):
            bricks[index] = x
            bricks[index + 1] = y
            bricks[index + 2] = colors[col_x]
            index += 3
        col_x += 1
    return bricks


def generate_level09():
    """Generate the bricks."""
    pi = [
        [19, 27, 1],
        [32, 27, 1],
        [84, 27, 1],
        [97, 27, 1],
        [45, 34, 1],
        [71, 34, 1],
        [32, 41, 4],
        [45, 41, 4],
        [58, 41, 4],
        [71, 41, 4],
        [84, 41, 4],
        [32, 48, 4],
        [45, 48, 0],
        [58, 48, 4],
        [71, 48, 0],
        [84, 48, 4],
        [19, 55, 4],
        [32, 55, 4],
        [45, 55, 4],
        [58, 55, 4],
        [71, 55, 4],
        [84, 55, 4],
        [97, 55, 4],
        [6, 62, 4],
        [19, 62, 4],
        [32, 62, 4],
        [45, 62, 4],
        [58, 62, 4],
        [71, 62, 4],
        [84, 62, 4],
        [97, 62, 4],
        [110, 62, 4],
        [6, 69, 4],
        [32, 69, 4],
        [84, 69, 4],
        [110, 69, 4],
        [6, 76, 4],
        [45, 76, 4],
        [71, 76, 4],
        [110, 76, 4],
    ]
    bricks = bytearray(len(pi) * 3)
    index = 0
    for row in pi:
        bricks[index] = row[0]
        bricks[index + 1] = row[1]
        bricks[index + 2] = row[2]
        index += 3
    return bricks


def test():
    """Test."""
    ba = generate_level09()
    path = 'Level009.bin'
    with open(path, "w") as f:
        f.write(ba)


test()
