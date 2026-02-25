"""Interview code."""


class A:
    """Class A."""

    def do_thing(self):
        print("From A")


class B(A):
    """Class B."""

    def do_thing(self):
        print("From B")


class C(A):
    """Class C."""

    def do_thing(self):
        print("From C")


class D(B, C):
    """Class D."""

    pass


def main():
    d = D()
    d.do_thing()


if __name__ == "__main__":
    main()
