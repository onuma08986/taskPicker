# メッセージ
ERROR_MSG_MODULE_NOT_DEFINE = "サービスモジュールが存在しません。"
ERROR_MSG_UNEXPECTED = "予期せぬエラーが発生しました。"
ERROR_MSG_NO_SERVICE = "提供が終了しているサービスを使用しています。"
ERROR_MSG_NO_ACTION = "提供が終了している機能を使用しています。"
ERROR_MSG_INVALID_SERVICE = "現在ご利用できないサービスを使用しています。：{}"
ERROR_MSG_INVALID_ACTION = "現在ご利用できない機能を使用しています。：{}"


# ステータス
STATUS_WAIT = 0  # 実行待ち
STATUS_RUN = 1  # 実行中
STATUS_COMPLETE = 2  # 完了
STATUS_ERROR = 3  # エラー


STATUS_EXEC_PRE = 0  # 利用準備中
STATUS_EXEC_VALID = 1  # 利用可
STATUS_EXEC_MENTE = 2  # メンテナンス中
STATUS_EXEC_SUSPEND = 3  # サービス一時停止
STATUS_EXEC_NO_SERVICE = 9  # サービス終了

TYPE_IO_NONE = 0
TYPE_IO_KEYVALUE = 1
TYPE_IO_JSON = 2
TYPE_IO_XML = 3
TYPE_IO_TEXT = 4
TYPE_IO_CSV = 5
TYPE_IO_PDF = 6
TYPE_IO_IMG = 7
TYPE_IO_OTHER = 99
