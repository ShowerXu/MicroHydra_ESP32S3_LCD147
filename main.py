"""Base 'apploader' for MicroHydra."""
import machine
from lib.hydra import loader, runtime
from lib import sdcard
import sys


# mh_if frozen:
# _LAUNCHER = const(".frozen/launcher/launcher")
# mh_else:
_LAUNCHER = const("/launcher/launcher")
# mh_end_if
sys.path = ['', '/lib', '.frozen', '.frozen/lib']


#default app path is the path to the launcher
app = _LAUNCHER

# mh_if TDECK:
# # T-Deck must manually power on its peripherals
# machine.Pin(10, machine.Pin.OUT, value=True)
# mh_end_if


# if this was not a power reset, we are probably launching an app:
if machine.reset_cause() != machine.PWRON_RESET:
    args = loader.get_args()
    if args:
        # pop the import path to prevent infinite boot loop
        app = args.pop(0)
        loader.set_args(*args)

# only mount the sd card if the app is on the sd card.
if app.startswith("/sd"):
    sdcard.SDCard().mount()

# import the requested app!
try:
    module = __import__(app)
    if not (app.startswith("/apps") or app.startswith("/sd/apps")):
        try:
            module = runtime.import_fresh(app)
        except Exception:
            pass
        if hasattr(module, "run"):
            module.run(*args)
except Exception as e:  # noqa: BLE001
    with open('log.txt', 'a') as log:
        log.write(f"[{app}]\n")
        sys.print_exception(e, log)
    # reboot into launcher
    loader.launch_app(_LAUNCHER)
