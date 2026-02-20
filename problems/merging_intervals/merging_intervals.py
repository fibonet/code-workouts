import pytest


def merge_interval(intervals, to_add):
    result = list()
    left, right = to_add
    was_added = False
    for il, ir in intervals:
        if ir < left:
            # copy all intervals bellow target
            result.append([il, ir])

        elif right < il:
            if not was_added:
                result.append([left, right])
                was_added = True

            # copy all intervals above target
            result.append([il, ir])

        else:
            # overlapping intervals, expand merge window
            left = min(left, il)
            right = max(right, ir)

    if not was_added:
        result.append([left, right])

    return result


@pytest.mark.parametrize(
    "intervals,to_add,expected",
    [
        # 1. Insert without overlap (middle)
        ([[1, 3], [6, 9]], [4, 5], [[1, 3], [4, 5], [6, 9]]),
        # 2. Insert overlapping one interval
        ([[1, 3], [6, 9]], [2, 5], [[1, 5], [6, 9]]),
        # 3. Overlap multiple intervals
        (
            [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
            [4, 9],
            [[1, 2], [3, 10], [12, 16]],
        ),
        # 4. Insert at beginning (no overlap)
        ([[5, 7], [8, 10]], [1, 3], [[1, 3], [5, 7], [8, 10]]),
        # 5. Insert at end (no overlap)
        ([[1, 2], [3, 5]], [6, 8], [[1, 2], [3, 5], [6, 8]]),
        # 6. Exact match with existing interval
        ([[1, 5]], [1, 5], [[1, 5]]),
        # 7. Fully contained inside existing
        ([[1, 10]], [3, 6], [[1, 10]]),
        # 8. New interval contains all existing
        ([[2, 3], [5, 7]], [1, 10], [[1, 10]]),
        # 9. Touching boundary
        ([[1, 3], [6, 9]], [3, 6], [[1, 9]]),
        # 10. Single element intervals
        ([[1, 1], [3, 3], [5, 5]], [2, 4], [[1, 1], [2, 4], [5, 5]]),
        # 11. Empty initial list
        ([], [4, 8], [[4, 8]]),
        # 12. Negative numbers
        ([[-10, -5], [0, 3]], [-6, 1], [[-10, 3]]),
        # 13. Adjacent but not overlapping
        ([[1, 2], [4, 5]], [2, 4], [[1, 5]]),
    ],
    ids=[
        "insert_no_overlap_middle",
        "overlap_single",
        "overlap_multiple",
        "insert_at_start",
        "insert_at_end",
        "exact_match",
        "contained_inside",
        "contains_all",
        "touching_boundary",
        "single_points",
        "empty_input",
        "negative_numbers",
        "adjacent_no_merge_if_open",
    ],
)
def test_merge_intervals(intervals, to_add, expected):
    actual = merge_interval(intervals, to_add)
    assert actual == expected


if __name__ == "__main__":
    print("do not run, test only.")
