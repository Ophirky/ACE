"""
    Holds a generic logger class to handle logs.
"""
# Imports #
import logging
import os

from src.server.utils.consts.logging_consts import LoggerConsts


class Logger:
    """
    Handles all logs
    """

    def __init__(self, logger_name: str) -> None:
        """
        Initialize logger
        :param logger_name: (str) the name of the logger
        :return: None
        """
        self.format = LoggerConsts.FORMAT
        self.level = LoggerConsts.LOG_LEVEL
        self.file_name = logger_name + LoggerConsts.LOG_FILE_EXTENSION
        self.file_path = LoggerConsts.LOG_DIR + self.file_name

        if not os.path.isdir(LoggerConsts.LOG_DIR):
            os.makedirs(LoggerConsts.LOG_DIR)
            print("created dir")

        self.logger = logging.getLogger(logger_name)

        self.logger.setLevel(self.level)
        file_handler = logging.FileHandler(self.file_path)
        file_handler.setFormatter(logging.Formatter(self.format))
        self.logger.addHandler(file_handler)


