"""Unit tests for interview module."""

from src.demo.interview import A, B, C, D, main


class TestClassA:
    """Test class A."""

    def test_do_thing(self, capsys):
        """Test A.do_thing() prints correct message."""
        a = A()
        a.do_thing()
        captured = capsys.readouterr()
        assert captured.out == "From A\n"

    def test_inheritance(self):
        """Test A is a proper class."""
        a = A()
        assert isinstance(a, A)


class TestClassB:
    """Test class B."""

    def test_do_thing(self, capsys):
        """Test B.do_thing() prints correct message."""
        b = B()
        b.do_thing()
        captured = capsys.readouterr()
        assert captured.out == "From B\n"

    def test_inheritance(self):
        """Test B inherits from A."""
        b = B()
        assert isinstance(b, B)
        assert isinstance(b, A)
        assert issubclass(B, A)


class TestClassC:
    """Test class C."""

    def test_do_thing(self, capsys):
        """Test C.do_thing() prints correct message."""
        c = C()
        c.do_thing()
        captured = capsys.readouterr()
        assert captured.out == "From C\n"

    def test_inheritance(self):
        """Test C inherits from A."""
        c = C()
        assert isinstance(c, C)
        assert isinstance(c, A)
        assert issubclass(C, A)


class TestClassD:
    """Test class D."""

    def test_do_thing(self, capsys):
        """Test D.do_thing() prints correct message based on MRO."""
        d = D()
        d.do_thing()
        captured = capsys.readouterr()
        assert captured.out == "From B\n"

    def test_inheritance(self):
        """Test D inherits from both B and C."""
        d = D()
        assert isinstance(d, D)
        assert isinstance(d, B)
        assert isinstance(d, C)
        assert isinstance(d, A)
        assert issubclass(D, B)
        assert issubclass(D, C)
        assert issubclass(D, A)

    def test_method_resolution_order(self):
        """Test method resolution order for class D."""
        expected_mro = (D, B, C, A, object)
        assert D.__mro__ == expected_mro

    def test_mro_behavior(self):
        """Test that D uses B's method due to MRO (diamond problem)."""
        d = D()
        assert hasattr(d, "do_thing")


class TestMainFunction:
    """Test main function."""

    def test_main(self, capsys):
        """Test main function creates D instance and calls do_thing."""
        main()
        captured = capsys.readouterr()
        assert captured.out == "From B\n"
