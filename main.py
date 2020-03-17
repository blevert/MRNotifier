import logging
import webbrowser

from mrnotifier.config import TrayConfig
from mrnotifier.observe import Observe
from mrnotifier.tray import Tray, TrayOption

logging.basicConfig(level=logging.INFO)


class Main:
    def __init__(self):
        open_merge_request = TrayOption(TrayConfig.menu_text, onclick=lambda tray: self.open_merge_request())
        self.tray = Tray(TrayConfig.hover_text, [open_merge_request])

        self._ready_to_merge = None

        Observe().on_ready_to_merge(self.update_tray)

    def update_tray(self, ready_to_merge):
        if ready_to_merge is None:
            self.tray.set_icon(TrayConfig.main_icon)
            self._ready_to_merge = None
        else:
            self.tray.set_icon(TrayConfig.merge_icon)
            self._ready_to_merge = ready_to_merge

    def open_merge_request(self):
        if self._ready_to_merge is None:
            logging.info('Tray double click, but not ready to merge')
        else:
            url = self._ready_to_merge.get_web_url()
            logging.info(f'Tray double click - open "{url}"')
            webbrowser.open(url)


Main()
