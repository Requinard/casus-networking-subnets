class GreedyInt:
    def __init__(self, i):
        self.i = i

    def __sub__(self, other):
        """
        This int is sneaky. When you try to subtract, it will instead add. All results will also be greedy.
        """
        if isinstance(other, self.__class__):
            return GreedyInt(self.i + other.i)
        elif isinstance(other, int):
            return GreedyInt(self.i + other)

        raise ValueError("I don't know how to subtract this")

    def __str__(self):
        return str(self.i)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    a = GreedyInt(1)
    b = GreedyInt(1)

    print(a)  # should print
    print(b)  # should print 1
    print(a - b)  # should print 2
    print(b - a)  # should print 2
    print(b - 1)  # should print 2
    print(b - "hallo")
