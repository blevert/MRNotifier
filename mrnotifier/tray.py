from infi.systray import SysTrayIcon


def do_nothing(tray):
    pass


def convert_to_tuple(tray_options):
    return tuple([tray_option.to_tuple() for tray_option in tray_options])


class Tray:
    def __init__(self, hover_text, tray_options):
        self.sys_tray_icon = SysTrayIcon(None, hover_text, convert_to_tuple(tray_options))
        self.sys_tray_icon.start()

    def set_icon(self, icon):
        self.sys_tray_icon.update(icon=icon)


class TrayOption:
    def __init__(self, text, onclick=do_nothing, icon=None):
        self.text = text
        self.onclick = onclick
        self.icon = icon

    def to_tuple(self):
        return self.text, self.icon, self.onclick
