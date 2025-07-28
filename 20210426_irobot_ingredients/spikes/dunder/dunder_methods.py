"""Main to test dunder methods"""

# Standard library imports
import sys


class dunderMethods():
    DUNDER_INIT_IS_CALLED = '__init__ is called'
    DUNDER_ENTER_IS_CALLED = '__enter__ is called'
    DUNDER_EXIT_IS_CALLED = '__exit__ is called'
    DUNDER_DEL_IS_CALLED = '__del__ is called'
    DUNDER_DELETE_IS_CALLED = '__delete__ is called'


    def __init__(self):
        print(self.DUNDER_INIT_IS_CALLED)


    def __enter__(self):
        print(self.DUNDER_ENTER_IS_CALLED)
        return self


    def __exit__(self, type, value, traceback):
        print(self.DUNDER_EXIT_IS_CALLED)


    def __del__(self):
        print(self.DUNDER_DEL_IS_CALLED)


    def __delete__(self, instance):
        print(self.DUNDER_DELETE_IS_CALLED)


    def __init__(self):
        print(self.DUNDER_INIT_IS_CALLED)



def dunder_tesing():
    with dunderMethods() as dm:
        print('dunder_tesing')


def main():
    exit_code = 0
    try:
        dunder_tesing()
    except Exception as exception:
        print(Fore.RED + f"ERROR: executing getting recipes with your favorite ingredients")
        print(f"{exception}{Style.RESET_ALL}")
        exit_code = 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
