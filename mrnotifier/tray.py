from infi.systray import SysTrayIcon
from mrnotifier.config import TrayConfig


class Tray:
    def __init__(self):
        self.sys_tray_icon = SysTrayIcon(TrayConfig.main, TrayConfig.hover_text)
        self.sys_tray_icon.start()

    def show_main(self):
        self.sys_tray_icon.update(icon=TrayConfig.main)

    def show_merge(self):
        self.sys_tray_icon.update(icon=TrayConfig.merge)
