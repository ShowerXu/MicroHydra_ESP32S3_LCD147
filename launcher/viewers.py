"""Built-in lightweight file viewers for Files."""

import struct
import time

from lib.audio import Audio
from lib.display import Display
from lib.hydra.config import Config
from lib.userinput import UserInput


_BMP_HEADER = const(54)


def _rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


def _message(display, config, text):
    display.fill(config.palette[2])
    y = (display.height // 2) - 4
    x = max(0, (display.width - (len(text) * 8)) // 2)
    display.text(text, x, y, config.palette[8])
    display.show()


def _wait_exit(kb):
    time.sleep_ms(250)
    while True:
        keys = kb.get_new_keys()
        if "ESC" in keys or "ENT" in keys:
            return
        time.sleep_ms(20)


def open_wav(path):
    """Play a WAV file and return when done."""
    display = Display()
    config = Config()
    _message(display, config, "Playing WAV...")
    Audio().play_wav(path, volume=80)
    _message(display, config, "Done")
    _wait_exit(UserInput())


def open_unsupported(path, kind):
    """Show an unsupported-format message."""
    display = Display()
    config = Config()
    _message(display, config, kind + " decoder unavailable")
    _wait_exit(UserInput())


def open_bmp(path):
    """Open an uncompressed RGB565 or RGB888 BMP image."""
    display = Display()
    config = Config()
    kb = UserInput()

    with open(path, "rb") as bmp:
        if bmp.read(2) != b"BM":
            raise ValueError("Not a BMP file")

        bmp.seek(10)
        data_offset = struct.unpack("<I", bmp.read(4))[0]
        header_size = struct.unpack("<I", bmp.read(4))[0]
        if header_size < 40:
            raise ValueError("Unsupported BMP header")

        width = struct.unpack("<i", bmp.read(4))[0]
        height = struct.unpack("<i", bmp.read(4))[0]
        planes = struct.unpack("<H", bmp.read(2))[0]
        bits = struct.unpack("<H", bmp.read(2))[0]
        compression = struct.unpack("<I", bmp.read(4))[0]

        if planes != 1 or compression != 0 or bits not in (16, 24):
            raise ValueError("Only uncompressed 16/24-bit BMP is supported")

        top_down = height < 0
        height = abs(height)
        row_size = ((width * bits + 31) // 32) * 4
        bytes_per_pixel = bits // 8

        src_x0 = max(0, (width - display.width) // 2)
        src_y0 = max(0, (height - display.height) // 2)
        draw_w = min(width, display.width)
        draw_h = min(height, display.height)
        dst_x0 = max(0, (display.width - draw_w) // 2)
        dst_y0 = max(0, (display.height - draw_h) // 2)

        display.fill(config.palette[2])
        row = bytearray(draw_w * bytes_per_pixel)

        for dy in range(draw_h):
            src_y = src_y0 + dy
            file_y = src_y if top_down else height - 1 - src_y
            bmp.seek(data_offset + (file_y * row_size) + (src_x0 * bytes_per_pixel))
            bmp.readinto(row)

            idx = 0
            for dx in range(draw_w):
                if bits == 24:
                    b = row[idx]
                    g = row[idx + 1]
                    r = row[idx + 2]
                    color = _rgb888_to_rgb565(r, g, b)
                else:
                    color = row[idx] | (row[idx + 1] << 8)
                display.pixel(dst_x0 + dx, dst_y0 + dy, color)
                idx += bytes_per_pixel

            if dy % 12 == 0:
                display.show()

        display.show()

    _wait_exit(kb)
