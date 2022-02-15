from django.apps import AppConfig

from process import scheduler


class ProcessConfig(AppConfig):
    name = "process"

    def ready(self):
        """スケジュールを起動する"""
        scheduler.start()
