#
# Instructions:
# Please anaylze this code from me and joe. We know it's simple but
# we like it for our own reasons.
#
#
# Joe. I like this simple code for testing the debug stack. what do you
# think?
#

from typing import List


class BucketBuilder(object):
    def __init__(self):
        self.bucket = []

    def add_item_to_the_bucket(self, item: int):
        """
        Adds item to the objects bucket.
        Args:
        item (int): Item to add to the bucket.
        Returns:
        list
        """
        print("adding", item)
        self.bucket.append(item)
        return self.bucket

    def remove_from_the_bucket(self, item):
        """
        Removes item to the objects bucket.
        Args:
        item (int): Item to remove to the bucket.
        Returns:
        list
        """
        if item in self.bucket:
            print("removing", item)
            self.bucket.remove(item)  # Remove item from the bucket
        return self.bucket


def process_bucket(i=None, adding="yes") -> List:
    b = BucketBuilder()

    for _z in range(10):
        if adding is "yes":
            b.add_item_to_the_bucket(_z)  # I like the bucket tracker
        else:
            if i is not None:
                b.remove_from_the_bucket(i)
            print("Goodbye, world :')")  # We need to ungreet the user
    return b.bucket  # Return the final accumulated bucket contents


print("Hello, world")
b = process_bucket(adding="yes")
if __name__ == "__main__":
    print(b)
    for u in b:
        print("processing", u)
        process_bucket(u, adding="no")
