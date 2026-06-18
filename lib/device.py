"""Device constants for this ESP32-S3R8 16M + ST7789 board."""


class Device:
    vals = {
        "name": "ESP32S3_LCD147_ES8311",
        "mh_version": (2, 5, 0),
        "batt_adc": 5,
        "display_backlight": 48,
        "display_baudrate": 40000000,
        "display_cs": 42,
        "display_dc": 41,
        "display_height": 172,
        "display_miso": None,
        "display_mosi": 45,
        "display_reset": 39,
        "display_rotation": 1,
        "display_sck": 40,
        "display_spi_id": 1,
        "display_width": 320,
        "i2c_sda": 12,
        "i2c_scl": 13,
        "i2s_id": 1,
        "i2s_mck": 7,
        "i2s_sck": 8,
        "i2s_ws": 9,
        "i2s_sd": 11,
        "i2s_mic": 10,
        "sdcard_slot": 1,
        "sdcard_clk": 14,
        "sdcard_cmd": 15,
        "sdcard_d0": 16,
        "sdcard_d1": 18,
        "sdcard_d2": 17,
        "sdcard_d3": 21,
        "rgb_led": 38,
    }
    feats = (
        "buttons",
        "display",
        "i2s_speaker",
        "i2s_microphone",
        "sdcard",
        "rgb_led",
        "wifi",
        "bluetooth",
        "spi_ram",
        "ESP32S3_LCD147_ES8311",
    )

    @staticmethod
    def __getattr__(name: str):
        return Device.vals[name]

    @staticmethod
    def __contains__(val: str):
        return val in Device.feats


Device = Device()
