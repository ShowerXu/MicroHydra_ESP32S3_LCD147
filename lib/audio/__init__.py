"""Audio support for the ESP32-S3 board with an ES8311 codec.

Pins:
    SDA=5, SCL=4, MCLK=6, BCLK/SCLK=11, DIN/DSIN=12, LRCK=13, DOUT=10.
"""

import struct
import time

from machine import I2C, I2S, Pin

from .i2ssound import I2SSound


_MH_I2S_ID = const(1)
_MH_I2S_MCK = const(6)
_MH_I2S_SCK = const(11)
_MH_I2S_WS = const(13)
_MH_I2S_SD = const(12)
_MH_I2S_MIC = const(10)

_ES8311_SDA = const(5)
_ES8311_SCL = const(4)
_ES8311_ADDR = const(0x18)

_WAV_BUF_SIZE = const(4096)


class ES8311:
    """Small ES8311 control helper for playback."""

    def __init__(self, *, i2c_id=0, sda=_ES8311_SDA, scl=_ES8311_SCL, addr=_ES8311_ADDR):
        self.addr = addr
        self.i2c = I2C(i2c_id, sda=Pin(sda), scl=Pin(scl), freq=100000)

    def _write(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytes((val,)))
        time.sleep_ms(1)

    def exists(self):
        return self.addr in self.i2c.scan()

    def init(self):
        """Initialize DAC playback in I2S slave mode."""
        if not self.exists():
            print("Warning: ES8311 not found on I2C bus")
            return False

        # Conservative playback setup: reset, enable clocks, I2S 16-bit, power DAC,
        # route DAC to output, set a moderate analog/digital volume, and unmute.
        for reg, val in (
            (0x00, 0x1F),
            (0x00, 0x00),
            (0x01, 0x30),
            (0x02, 0x10),
            (0x03, 0x10),
            (0x08, 0x00),
            (0x09, 0x0C),
            (0x0A, 0x0C),
            (0x0B, 0x00),
            (0x0C, 0x00),
            (0x0D, 0x01),
            (0x10, 0x1F),
            (0x11, 0x7F),
            (0x12, 0x00),
            (0x13, 0x10),
            (0x31, 0x00),
            (0x32, 0xBF),
            (0x37, 0x08),
        ):
            self._write(reg, val)
        return True

    def set_volume(self, volume):
        """Set DAC volume, volume is 0..100."""
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self._write(0x32, int(volume * 255 // 100))


class Audio(I2SSound):
    """Shared audio object for UI sounds and WAV playback."""

    def __new__(cls, **kwargs):  # noqa: ARG003, D102
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, buf_size=2048, rate=11025, channels=4):
        """Create the Audio object once."""
        if getattr(self, "_audio_ready", False):
            return

        super().__init__(
            buf_size=buf_size,
            rate=rate,
            channels=channels,
            i2s_id=_MH_I2S_ID,
            sck=_MH_I2S_SCK,
            ws=_MH_I2S_WS,
            sd=_MH_I2S_SD,
            mck=_MH_I2S_MCK,
        )
        self.codec = ES8311()
        self.codec.init()
        self._audio_ready = True

    def _read_wav_header(self, wav):
        """Return (channels, sample_rate, bits, data_size) for a PCM WAV file."""
        if wav.read(4) != b"RIFF":
            raise ValueError("Not a RIFF WAV file")
        wav.seek(8)
        if wav.read(4) != b"WAVE":
            raise ValueError("Not a WAVE file")

        fmt = None
        data_size = None
        while True:
            chunk_id = wav.read(4)
            if len(chunk_id) < 4:
                break
            chunk_size = struct.unpack("<I", wav.read(4))[0]
            if chunk_id == b"fmt ":
                raw = wav.read(chunk_size)
                audio_fmt, channels, rate, _, _, bits = struct.unpack("<HHIIHH", raw[:16])
                fmt = (audio_fmt, channels, rate, bits)
            elif chunk_id == b"data":
                data_size = chunk_size
                break
            else:
                wav.seek(wav.tell() + chunk_size + (chunk_size & 1))

        if fmt is None or data_size is None:
            raise ValueError("Incomplete WAV file")
        audio_fmt, channels, rate, bits = fmt
        if audio_fmt != 1 or bits != 16:
            raise ValueError("Only 16-bit PCM WAV files are supported")
        if channels not in (1, 2):
            raise ValueError("Only mono or stereo WAV files are supported")
        return channels, rate, bits, data_size

    def play_wav(self, path, *, volume=80):
        """Play a 16-bit PCM WAV file from flash or SD.

        This is a blocking player intended for apps. UI beeps resume when playback
        finishes.
        """
        self.stop_all()
        self.deinit()

        with open(path, "rb") as wav:
            channels, rate, _, remaining = self._read_wav_header(wav)
            fmt = I2S.MONO if channels == 1 else I2S.STEREO
            output = self._make_output(rate=rate, ibuf=_WAV_BUF_SIZE * 2, fmt=fmt)
            self.codec.init()
            self.codec.set_volume(volume)
            buf = bytearray(_WAV_BUF_SIZE)
            view = memoryview(buf)
            try:
                while remaining > 0:
                    read_len = wav.readinto(view[:min(_WAV_BUF_SIZE, remaining)])
                    if not read_len:
                        break
                    output.write(view[:read_len])
                    remaining -= read_len
            finally:
                output.deinit()
                self._start_output(rate=self._rate)

    def stop_all(self):
        """Stop all mixer channels and clear pending sounds."""
        for channel in range(self.channels):
            self._queues[channel] = []
            self._registers[channel].sample = None
