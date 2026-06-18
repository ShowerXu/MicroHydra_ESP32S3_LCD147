"""Device constants for this ESP32-S3R8 16M + ST7789 board."""


class Device:
    vals = {
        "name": "ESP32S3_LCD147_ES8311",
        "mh_version": (2, 5, 0),
        "batt_adc": 9,
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
        "i2c_sda": 5,
        "i2c_scl": 4,
        "i2s_id": 1,
        "i2s_mck": 6,
        "i2s_sck": 11,
        "i2s_sd": 12,
        "i2s_ws": 13,
        "i2s_mic": 10,
        "sdcard_cs": 21,
        "sdcard_miso": 16,
        "sdcard_mosi": 15,
        "sdcard_sck": 14,
        "sdcard_slot": 2,
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
