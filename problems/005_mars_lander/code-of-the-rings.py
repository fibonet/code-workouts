import sys


def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def chr_dist(left, right):
    # hack
    if left == " " and right == " ":
        return 0
    elif left == " ":
        left = "@"
    elif right == " ":
        right = "["

    dist = ord(right) - ord(left)

    if dist > 13:
        dist -= 27

    return dist


SIZE = 30
runes = [" "] * SIZE
magic_phrase = input()

actions = list()
for i, letter in enumerate(magic_phrase):
    mi = i % SIZE
    left = runes[mi]
    count = chr_dist(left, letter)
    # log(f"{i:03} : {mi:02}  {letter!r} - {left!r} = {count}")

    runes[mi] = letter

    parts = list()
    if count < 0:
        parts.append("-" * (-count))
    elif count > 0:
        parts.append("+" * count)

    parts.append(".")
    actions.append("".join(parts))


print(">".join(actions))
