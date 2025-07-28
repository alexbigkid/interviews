"""
    Just a little something to bring iRobot people to smile :)
    Generates some random yes and no answers.
"""

# Standard library imports

# Third party imports
import random

# Local application imports


class YesNoGenerator():


    def __init__(self):
        self.__random_number = random.randint(0, 9)

    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def generate_random_yes(self):
        yes_list = [
            "Yes",
            "Yes, yes, and yes!",
            "This recipe gets my vote.",
            "On a scale of 1-10, this recipe is 100!",
            "Yammy 😋",
            "Healthy, so I'm going to say yes to that.",
            "Let's do it!",
            "Okey-dokey!",
            "That would be a Y-E-S!",
            "There's a 100% chance that I'm going say yes to that one.",
            "The smile on my face says it all"
        ]
        return yes_list[self.__random_number]


    def generate_random_no(self):
        no_list = [
            "No",
            "Absolutelly not",
            "I dont' like that recipe",
            "No way!",
            "It's N to the O!",
            "That sounds like effort, so no.",
            "Not today",
            "Negative",
            "TL;DR;",
            "On a scale of maybe to absolutely, I would say: absolutely not!",
            "Too expensive, so No."
        ]
        return no_list[self.__random_number]
