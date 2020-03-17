import configparser

_config = configparser.ConfigParser()
_config.read('config.ini')


class GitlabConfig:
    url = _config.get('gitlab', 'url')
    token = _config.get('gitlab', 'token')
    verifySSL = _config.getboolean('gitlab', 'verifySSL')


class TrayConfig:
    main_icon = _config.get('tray', 'main_icon')
    merge_icon = _config.get('tray', 'merge_icon')
    hover_text = _config.get('tray', 'hover_text')
    menu_text = _config.get('tray', 'menu_text')


class ObserveConfig:
    interval = _config.getfloat('observe', 'interval')
    upvotes_to_merge = _config.getint('observe', 'upvotes_to_merge')
