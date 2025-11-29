import sys
from collections import Counter


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

# prepare the runes based on occurences
prepare = list()
count = Counter(magic_phrase)
lookup = dict()
for i, (let, mult) in enumerate(count.items()):
    dist = chr_dist(runes[i], let)
    if dist < 0:
        prepare.append("-" * (-dist))
    elif dist > 0:
        prepare.append("+" * dist)
    else:
        prepare.append("")

    runes[i] = let
    lookup[let] = i

actions.append(">".join(prepare))

# walk through magic phrase
prev_pos = len(count) - 1
for letter in magic_phrase:
    next_pos = lookup[letter]

    dist = next_pos - prev_pos
    if dist < 0:
        steps = -dist
        move = "<"
    elif dist > 0:
        steps = dist
        move = ">"
    else:
        move = None
        steps = 0

    if move:
        actions.append(f"{move * steps}.")
    else:
        actions.append(".")

    prev_pos = next_pos


print("".join(actions))
