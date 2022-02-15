import logging
import os

logger = logging.getLogger("process")


class Condition:
    def __init__(self, name):
        self.name = name

    def file_found(self, detail, save_file_path):
        """ファイルが見つかった"""
        return True if os.path.exists(save_file_path) else False

    def file_not_found(self, detail, save_file_path):
        """ファイルが見つからない"""
        return False if os.path.exists(save_file_path) else True
