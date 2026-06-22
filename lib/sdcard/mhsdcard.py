"""This simple module configures and mounts an SDCard."""

# mh_if shared_sdcard_spi:
# from .sdcard import _SDCard
# mh_end_if

import machine
import os



_MH_SDCARD_SLOT = const(1)
_MH_SDCARD_CLK = const(14)
_MH_SDCARD_CMD = const(15)
_MH_SDCARD_D0 = const(16)
_MH_SDCARD_D1 = const(18)
_MH_SDCARD_D2 = const(17)
_MH_SDCARD_D3 = const(21)


class SDCard:
    """SDCard control."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the SDCard."""
        if self._initialized:
            return
        self._initialized = True
        # mh_if shared_sdcard_spi:
        # self.sd = _SDCard(
        #     machine.SPI(
        #         _MH_SDCARD_SLOT,
        #         sck=machine.Pin(_MH_SDCARD_CLK),
        #         miso=machine.Pin(_MH_SDCARD_D0),
        #         mosi=machine.Pin(_MH_SDCARD_CMD),
        #     ),
        #     cs=machine.Pin(_MH_SDCARD_D3),
        # )
        # mh_else:
        self.sd = machine.SDCard(
            slot=_MH_SDCARD_SLOT,
            width=4,
            sck=machine.Pin(_MH_SDCARD_CLK),
            cmd=machine.Pin(_MH_SDCARD_CMD),
            data=(
                machine.Pin(_MH_SDCARD_D0),
                machine.Pin(_MH_SDCARD_D1),
                machine.Pin(_MH_SDCARD_D2),
                machine.Pin(_MH_SDCARD_D3),
            )
        )
        # mh_end_if


    def mount(self):
        """Mount the SDCard."""
        try:
            os.mount(self.sd, '/sd')
        except OSError as e:
            # errno 16 is EBUSY (already mounted), 17 is EEXIST
            if e.errno in (16, 17):
                pass
            else:
                print(f"Could not mount SDCard: {e}")
        except (NameError, AttributeError) as e:
            print(f"Could not mount SDCard: {e}")


    def deinit(self):
        """Unmount and deinit the SDCard."""
        try:
            os.umount('/sd')
        except Exception:
            pass
        # mh_if not shared_sdcard_spi:
        try:
            self.sd.deinit()
        except Exception:
            pass
        # mh_end_if
        self._initialized = False
        SDCard._instance = None
