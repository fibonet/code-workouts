# You are given three platforms: A, B, and C.

# Each platform contains a stack of boxes represented as a collection
# (e.g., std::vector<int> / list[int]), where:

# - Each box has a unique weight (integer).
# - The top of a platform is the last element of the collection.
# - Only the top box of a platform can be moved.
# - A robotic arm can move exactly one box at a time from the top of
#   one platform to the top of another platform.
# - There are NO placement restrictions:
#   a heavier box may be placed on a lighter box temporarily.

# Initial state:
# - Boxes may be distributed arbitrarily across A, B, and C.
# - Platforms may contain any number of boxes, including zero.

# Goal:
# - Move all boxes onto platform A.
# - Final ordering on A must be:
#     heaviest box at the bottom
#     lightest box at the top

# Additional requirement:
# - Print every robotic arm move in the format:

#     N. move box(w=X) S -> D

#   where:
#     - N is the move number
#     - X is the box weight
#     - S is the source platform name
#     - D is the destination platform name

# Example:
#     1. move box(w=5) A -> B
#     2. move box(w=2) C -> A

def move(src, dst, src_name, dst_name, move_count):
    box = src.pop()
    dst.append(box)

    move_count += 1

    print(
        f"{move_count}. "
        f"move box(w={box}) "
        f"{src_name} -> {dst_name}"
    )

    return move_count


def sort_platforms(a, b, c):
    move_count = 0

    # move everything onto B
    while a:
        move_count = move(a, b,'A', 'B',move_count)

    while c:
        move_count = move(c, b,'C', 'B',move_count)

    # B -> A using auxiliary C
    while b:
        x = b[-1] # top element

        # Move lighter boxes from A out of the way into C
        while a and a[-1] < x:
            move_count = move(a, c,'A', 'C',move_count)

        # Insert current box into A
        move_count = move(b, a,'B', 'A',move_count)

        # Restore moved boxes from C
        while c:
            move_count = move(c, a,'C', 'A',move_count)

    return move_count


def main():
    a = [9, 3, 7, 1, 5]
    b = [6, 4]
    c = [8, 2]

    total_moves = sort_platforms(a, b, c)

    print("\nFinal A (bottom -> top):")
    print(a)

    print(f"\nTotal moves: {total_moves}")


if __name__ == "__main__":
    main()
