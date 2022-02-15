import datetime
import logging
from functools import singledispatch
from importlib import import_module

from apis.baselogic import BaseLogic
from jobflows.models import FlowDetail, Schedule

from process import const

logger = logging.getLogger("process")


@singledispatch
def execute(arg):
    pass


@execute.register(int)
def execute_imm(arg):
    """即時実行関数"""
    controller = FlowController()
    controller.run(Schedule.objects.get(id=arg))


@execute.register(Schedule)
def execute_schedule(arg):
    """スケジュール実行関数"""
    controller = FlowController()
    controller.run(arg)


class FlowController:
    """ジョブフロー制御クラス"""

    def run(self, schedule):
        """フローに従いジョブを実行"""
        now = datetime.datetime.now()
        # ステータス更新（実行中）
        self.__update_status(schedule, now, const.STATUS_RUN)

        # ジョブフローを読み込む
        details = (
            FlowDetail.objects.all().filter(flow_id=schedule.flow_id).order_by("execno")
        )

        if self.__check_invalid_service(schedule, details):
            return

        logger.debug("action start.")
        params = None
        nextno = -1
        for row in details:
            if nextno is not None and (nextno < 0 or nextno == row.execno):
                try:
                    # モジュールからクラスを生成し、メソッドを呼び出す
                    mod = import_module(row.action.service.module)
                    ret = getattr(mod.Logic(BaseLogic), row.action.method)(
                        schedule.user, row, params
                    )
                    nextno = ret[0]
                    params = ret[1]
                    logger.debug("-- next. %s -> %s, %s" % (row.execno, nextno, params))
                except ModuleNotFoundError as e:
                    self.__error(schedule, const.ERROR_MSG_MODULE_NOT_DEFINE, e)
                    return
                except Exception as e:
                    self.__error(schedule, const.ERROR_MSG_UNEXPECTED, e)
                    return

        # ステータス更新（完了 or 待ち）
        if schedule.intval > 0 or schedule.week is not None:
            self.__update_status(schedule, now, const.STATUS_WAIT)
        else:
            self.__update_status(schedule, now, const.STATUS_COMPLETE)

        logger.debug("action finish.")

    def __update_status(self, schedule, now, status):
        """ステータス更新"""
        schedule.status = status
        schedule.err_msg = None or ""

        if status == const.STATUS_RUN:
            schedule.exec_at = now.strftime("%Y%m%d%H%M%S")
            if schedule.intval > 0:
                schedule.time = (
                    now + datetime.timedelta(minutes=schedule.intval)
                ).strftime("%H%M")

        schedule.save(update_fields=["status", "time", "err_msg", "exec_at"])

    def __error(self, schedule, message, e):
        """エラーメッセージ更新"""
        schedule.status = const.STATUS_ERROR
        schedule.err_msg = message
        schedule.save(update_fields=["status", "err_msg"])
        logger.error(e)

    def __check_invalid_service(self, schedule, details):
        """サービス利用可否確認"""
        s = ""
        for row in details:
            if row.action.service.status == const.STATUS_EXEC_NO_SERVICE:
                s = const.ERROR_MSG_NO_SERVICE

            elif row.action.service.status != const.STATUS_EXEC_VALID:
                s = const.ERROR_MSG_INVALID_SERVICE.format(row.action.service.status)

            elif row.action.status == const.STATUS_EXEC_NO_SERVICE:
                s = const.ERROR_MSG_NO_ACTION

            elif row.action.status != const.STATUS_EXEC_VALID:
                s = const.ERROR_MSG_INVALID_ACTION.format(row.action.status)

        if s != "":
            self.__error(schedule, s, s)
            return True
        else:
            return False
