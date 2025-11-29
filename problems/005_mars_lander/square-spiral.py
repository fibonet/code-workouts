import sys


def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


OUTSIDE = "*"
MOVES = dict(up=(-1, 0), down=(1, 0), right=(0, 1), left=(0, -1))
TURNS = {
    "clockwise": dict(up="right", right="down", down="left", left="up"),
    "counter-clockwise": dict(up="left", left="down", down="right", right="up"),
}


def letter_streamer(pattern1, pattern2):
    pa1, rep1 = pattern1[0], int(pattern1[1:])
    pa2, rep2 = pattern2[0], int(pattern2[1:])
    step = ord(pa2) - ord(pa1)
    i = ord(pa1) - ord("A")

    while True:
        for _ in range(rep1):
            yield chr(ord("A") + i)
        i = (i + step) % 26


def spiral_walker(d_corner, direction, canvas, size):
    row, col, towards = d_corner
    rs, cs = MOVES[towards]
    center = (size + 1) // 2, (size + 1) // 2

    value = None
    while value is None:
        yield row, col

        if (row, col) == center:
            break
        elif canvas[row + rs][col + cs] == OUTSIDE:
            towards = TURNS[direction][towards]
            rs, cs = MOVES[towards]
            row, col = row + rs, col + cs
        elif (
            ahead := canvas[row + 2 * rs][col + 2 * cs]
        ) is not None and ahead.isalpha():
            # look ahead
            towards = TURNS[direction][towards]
            rs, cs = MOVES[towards]
            row, col = row + rs, col + cs
        else:
            row, col = row + rs, col + cs

        value = canvas[row][col]


# read the inputs
size, start, direction, pattern1, pattern2 = input().split()
size = int(size)

genie = letter_streamer(pattern1, pattern2)

canvas = [[None for _ in range(size + 2)] for _ in range(size + 2)]
for i in range(size + 2):
    canvas[0][i] = OUTSIDE
    canvas[size + 1][i] = OUTSIDE
    canvas[i][0] = OUTSIDE
    canvas[i][size + 1] = OUTSIDE

DIRECTED_CORNERS = {
    "clockwise": dict(
        topLeft=(1, 1, "right"),
        topRight=(1, size, "down"),
        bottomLeft=(size, 1, "up"),
        bottomRight=(size, size, "left"),
    ),
    "counter-clockwise": dict(
        topLeft=(1, 1, "bottom"),
        topRight=(1, size, "left"),
        bottomLeft=(size, 1, "right"),
        bottomRight=(size, size, "up"),
    ),
}

d_corner = DIRECTED_CORNERS[direction][start]
walker = spiral_walker(d_corner, direction, canvas, size)
for move in walker:
    row, col = move
    value = next(genie)
    canvas[row][col] = value
    # log(move, "->", value)

for ri in range(1, size + 1):
    line = "".join(canvas[ri][ci] or " " for ci in range(1, size + 1))
    print(line)
