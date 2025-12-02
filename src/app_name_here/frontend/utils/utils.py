"""
General utility functions.
"""

from collections import OrderedDict
import os
from typing import Any


def get_choice_from_options(options: OrderedDict) -> Any:
    """Displays and gets a chosen value from the provided options.

    :param options: Ordered dictionary of the available option names and their values.
    :type options: OrderedDict
    :return: The value of the chosen option.
    :rtype: typing.Any
    """
    while True:
        print("Choose an option:")

        # Parse and display the options in a numbered form.
        for i, name in enumerate(options.keys()):
            print(f"  {i}) {name}")

        # User input to choose an option by its number.
        choice = input("\nChoice: ")

        try:
            # Parse the chosen number
            choice_num = int(choice)
            if choice_num < 0:
                print("Choice must be a positive number! Please try again.\n")
                continue

            # Parse the option value for the chosen number
            chosen_value = list(options.values())[choice_num]
            print()
            return chosen_value

        except ValueError:
            print("Choice must be a number! Please try again.\n")
        except IndexError:
            print("Invalid choice! Please try again.\n")


def clear_screen():
    """Clears the app's screen."""
    # Citation: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
    os.system("cls" if os.name == "nt" else "clear")
