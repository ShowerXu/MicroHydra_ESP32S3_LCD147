import time
from machine import Pin


class Keys:
    """Read the four GPIO buttons with debounce and edge tracking."""

    main_action = "ENT"
    secondary_action = "ESC"
    aux_action = "FN"

    ext_dir_dict = {";": "UP", ",": "LEFT", ".": "DOWN", "/": "RIGHT", "`": "ESC"}

    _BUTTONS = (
        ("ESC", 0),
        ("UP", 1),
        ("ENT", 2),
        ("DOWN", 3),
    )

    def __init__(self, *, debounce_ms=35, **kwargs):  # noqa: ARG002
        self.key_state = []
        self.new_key_state = []
        self.released_key_state = []
        self.debounce_ms = debounce_ms
        now = time.ticks_ms()
        self._pins = [(name, Pin(pin, Pin.IN, Pin.PULL_UP)) for name, pin in self._BUTTONS]
        self._raw_state = {name: False for name, _ in self._BUTTONS}
        self._stable_state = {name: False for name, _ in self._BUTTONS}
        self._last_change = {name: now for name, _ in self._BUTTONS}

    def get_pressed_keys(self, *, force_fn=False, force_shift=False) -> list:  # noqa: ARG002
        """Return currently held keys after debounce filtering."""
        now = time.ticks_ms()
        pressed = []
        released = []

        for name, pin in self._pins:
            raw_pressed = pin.value() == 0

            if raw_pressed != self._raw_state[name]:
                self._raw_state[name] = raw_pressed
                self._last_change[name] = now

            if raw_pressed != self._stable_state[name] \
            and time.ticks_diff(now, self._last_change[name]) >= self.debounce_ms:
                self._stable_state[name] = raw_pressed
                if raw_pressed:
                    pressed.append(name)
                else:
                    released.append(name)

        self.key_state = [name for name, _ in self._BUTTONS if self._stable_state[name]]
        self.new_key_state = pressed
        self.released_key_state = released
        return self.key_state

    def get_key_events(self):
        """Return (pressed, released) edges from the most recent scan."""
        return self.new_key_state, self.released_key_state


MOD_KEYS = ("SHIFT", "FN", "OPT")
ALWAYS_NEW_KEYS = ()
NO_REPEAT_KEYS = ("ENT", "ESC")
