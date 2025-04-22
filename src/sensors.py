from typing import Callable

callbackOnReady: Callable[[], None] = lambda: None
"""
Method reference to call if the measuring task was finished
"""

data: dict[str,str] = {}
"""
Structure consisting of sensor data values.
Filled when perform_measuring is called
"""



def initialize() -> None:
    """
        Helping
    """
    pass

def perform_measuring() -> None:
    """

    :return:
    """
    callbackOnReady()
