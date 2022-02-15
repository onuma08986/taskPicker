# Copyright (C) 2021-
# Author: Kazuyuki Oonuma
# Contact: oonuma@reisys.co.jp

"""[Youtube API]処理モジュール"""


import logging
import sys

from apis.baselogic import BaseLogic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("process")


class Logic(BaseLogic):
    """
    #    @csrf_exempt
    #    def メソッド名(self, user, detail, file_path):
    #
    #        # ここにメイン処理を記述
    #        # 次のアクションに渡す値は、ret_paramsにセットする
    #
    #        return self.get_next_exec_no(user, detail, 戻り値), 戻り値
    """

    @csrf_exempt
    def action1(self, detail, params):
        ret_params = None
        logger.debug(sys._getframe().f_code.co_name)
        return self.get_next_exec_no(detail, ret_params), ret_params

    @csrf_exempt
    def action2(self, detail, params):
        ret_params = None
        logger.debug(sys._getframe().f_code.co_name)
        return self.get_next_exec_no(detail, ret_params), ret_params

    @csrf_exempt
    def list(request):
        """リソースを取得(GET)"""
        return HttpResponse('{"list": "success"}')

    @csrf_exempt
    def insert(request):
        """リソースを作成(POST)"""
        return HttpResponse('{"insert": "success"}')

    @csrf_exempt
    def insert_video(request):
        """リソースを作成(POST)"""
        return HttpResponse('{"insert_video": "success"}')

    @csrf_exempt
    def insert_title(request):
        """リソースを作成(POST)"""
        return HttpResponse('{"insert_title": "success"}')

    @csrf_exempt
    def update(request):
        """リソースを変更(PUT)"""
        return HttpResponse('{"update": "success"}')

    @csrf_exempt
    def delete(request):
        """リソースを削除(DELETE)"""
        return HttpResponse('{"delete": "success"}')
