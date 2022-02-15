# Copyright (C) 2021-
# Author: Kazuyuki Oonuma
# Contact: oonuma@reisys.co.jp

"""ダウンロード処理モジュール"""


import logging

from apis.baselogic import BaseLogic

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
