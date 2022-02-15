# Copyright (C) 2021-
# Author: Kazuyuki Oonuma
# Contact: oonuma@reisys.co.jp

"""ローカルファイル処理モジュール"""


import glob
import logging

from apis.baselogic import BaseLogic

logger = logging.getLogger("process")


class Logic(BaseLogic):
    """
    #    @csrf_exempt
    #    def メソッド名(self, user, detail, *args):
    #
    #        # ここにメイン処理を記述
    #        # 次のアクションに渡す値は、ret_paramsにセットする
    #
    #        return self.get_next_exec_no(user, detail, 戻り値), 戻り値
    """

    def get_file_list(self, user, detail, *args):
        """ファイルを検索する"""

        logger.debug(__name__ + " get_file_list start.")

        # 検索結果があればファイルに保存する
        params = get_params(self, user, detail)
        search_path, save_path = params
        result = glob.glob(search_path)
        if result:
            f = open(save_path, "a")
            f.write("\n".join(result))
            f.close

        logger.debug(__name__ + " get_file_list end. [%s]" % save_path)

        return self.get_next_exec_no(user, detail, save_path), save_path


def get_params(self, user, detail):
    """個別パラメータ取得"""

    keys = self.get_individual_keys(user.user_id, detail.id)
    search_path = save_path = None
    for row in keys:
        if "SEARCH_FILE_PATH" == row.key.key:
            search_path = row.char
        elif "SAVE_FILE_PATH" == row.key.key:
            save_path = row.char

    return search_path, save_path
