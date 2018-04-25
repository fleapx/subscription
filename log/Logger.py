import logging


class Logger:
    def __init__(self, path, cmd_level=logging.DEBUG, file_level=logging.INFO):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            # 设置CMD日志
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            sh.setLevel(cmd_level)
            # 设置文件日志
            fh = logging.FileHandler(path)
            fh.setFormatter(fmt)
            fh.setLevel(file_level)
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
