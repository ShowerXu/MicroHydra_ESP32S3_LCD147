"""MicroHydra app template."""

import machine
import time

from lib import display, userinput
from lib.hydra import config


_MH_DISPLAY_HEIGHT = const(172)
_MH_DISPLAY_WIDTH = const(320)
_DISPLAY_WIDTH_HALF = const(_MH_DISPLAY_WIDTH // 2)

_CHAR_WIDTH = const(16)
_CHAR_WIDTH_HALF = const(_CHAR_WIDTH // 2)


DISPLAY = display.Display()
CONFIG = config.Config()
INPUT = userinput.UserInput()


def main_loop():
    """Run the main loop of the app."""
    current_text = "Hello World!"

    while True:
        keys = INPUT.get_new_keys()

        if keys:
            current_text = str(keys)

        if "ESC" in keys:
            machine.reset()

        DISPLAY.fill(CONFIG.palette[2])
        DISPLAY.text(
            text=current_text,
            x=_DISPLAY_WIDTH_HALF - (len(current_text) * _CHAR_WIDTH_HALF),
            y=50,
            color=CONFIG.palette[8],
        )
        DISPLAY.show()
        time.sleep_ms(10)


main_loop()
