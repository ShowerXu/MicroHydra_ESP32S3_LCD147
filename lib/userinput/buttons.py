"""Compatibility helper for reading the four board buttons."""

from ._keys import Keys


_keys = Keys()


def get_keys():
    """Return debounced currently pressed keys."""
    return _keys.get_pressed_keys()
