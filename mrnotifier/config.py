import configparser

_config = configparser.ConfigParser()
_config.read('config.ini')


class GitlabConfig:
    url = _config.get('gitlab', 'url')
    token = _config.get('gitlab', 'token')
    verifySSL = _config.getboolean('gitlab', 'verifySSL')


class TrayConfig:
    main = _config.get('tray', 'main')
    merge = _config.get('tray', 'merge')
    hover_text = _config.get('tray', 'hover_text')


class ObserveConfig:
    interval = _config.getint('observe', 'interval')
    upvotes_to_merge = _config.getint('observe', 'upvotes_to_merge')
