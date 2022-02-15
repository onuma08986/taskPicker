import logging
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Q

from process import const

logger = logging.getLogger("process")


def start():
    """スケジュール起動（毎分0秒）"""
    sc = BackgroundScheduler()
    sc.add_job(__get_schedules, "cron", second=0)
    sc.start()


def __get_schedules():
    """実行対象のスケジュールを取得し、別スレッドでジョブフローを実行"""
    from jobflows.models import Schedule

    from process import controller

    logger.info("scheduler start.")

    now = datetime.now()

    schedules = Schedule.objects.all().filter(
        Q(date=None)
        | Q(date=now.strftime("%m%d"))
        | Q(week__contains=now.strftime("%w")),
        time=now.strftime("%H%M"),
        s_from__lte=now.strftime("%Y%m%d"),
        s_to__gte=now.strftime("%Y%m%d"),
        status=const.STATUS_WAIT,
    )

    # スレッド実行（並列数：10）
    with ThreadPoolExecutor(max_workers=10, thread_name_prefix="th") as executor:
        for row in schedules:
            executor.submit(controller.execute, row)

    logger.info("scheduler end.")
