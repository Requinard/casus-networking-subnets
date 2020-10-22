class InvertedInt:
    def __init__(self, i):
        self.i = i

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return InvertedInt(self.i + other.i)
        elif isinstance(other, int):
            return InvertedInt(self.i + other)

        raise ValueError("I don't know how to subtract this")

    def __str__(self):
        return str(self.i)


if __name__ == '__main__':
    a = InvertedInt(1)
    b = InvertedInt(1)

    print(a)  # should print
    print(b)  # should print 1
    print(a - b)  # should print 2
    print(b - a)  # should print 2
    print(b - 1)  # should print 2
    print(b - "hallo")
