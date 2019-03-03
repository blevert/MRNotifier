import logging
import webbrowser

from mrnotifier.config import TrayConfig, GitlabConfig
from mrnotifier.observe import Observe
from mrnotifier.tray import Tray, TrayOption

logging.basicConfig(level=logging.INFO)


class Main:
    def __init__(self):
        open_merge_request = TrayOption(TrayConfig.menu_text, onclick=lambda tray: self.open_merge_request())
        self.tray = Tray(TrayConfig.hover_text, [open_merge_request])

        self._url = None

        Observe().on_ready_to_merge(self.update_tray)

    def update_tray(self, is_ready_to_merge):
        logging.info('Ready to merge: ' + str(is_ready_to_merge))
        if is_ready_to_merge:
            self.tray.set_icon(TrayConfig.merge_icon)
            self._url = GitlabConfig.url
        else:
            self.tray.set_icon(TrayConfig.main_icon)
            self._url = None

    def open_merge_request(self):
        logging.info(f'Tray double click - open "{self._url}"')
        if self._url:
            webbrowser.open(self._url)


Main()
