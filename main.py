import logging

from mrnotifier.observe import Observe
from mrnotifier.tray import Tray

logging.basicConfig(level=logging.INFO)

tray = Tray()


def update_tray(is_ready_to_merge):
    logging.info("Ready to merge: " + str(is_ready_to_merge))
    if is_ready_to_merge:
        tray.show_merge()
    else:
        tray.show_main()


Observe().on_ready_to_merge(update_tray)
