import unittest

from parameterized import parameterized

# local  modules imports
from context import handler

class TestHandler(unittest.TestCase):
    """This tests the functionality of the handler.py"""
    maxDiff = None


    # @classmethod
    # def setUpClass(cls) -> None:
    #     """A class method called before tests in an individual class are run."""
    #     pass


    # @classmethod
    # def tearDownClass(cls) -> None:
    #     """A class method called after tests in an individual class have run."""
    #     pass


    # def setUp(self) -> None:
    #     """Called immediately before each and every test to prepare the test method to run"""
    #     return super().setUp()


    # def tearDown(self) -> None:
    #     """Called immediately after each and every test to cleanup after each test method has ran."""
    #     return super().tearDown()


    @parameterized.expand([
        ['key1',   "value1"],
        ['key2',   "value2"],
    ])
    def test_function_name_to_test(self, key:str, value:str) -> None:
        # print(f'-> {self.__class__.__name__}.{function_name()}')cd ..
        self.assertEqual(key[-1], value[-1])


if __name__ == '__main__':
    unittest.main()
