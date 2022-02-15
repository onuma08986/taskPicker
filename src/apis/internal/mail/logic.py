# Copyright (C) 2021-
# Author: Kazuyuki Oonuma
# Contact: oonuma@reisys.co.jp

"""メール送信処理モジュール"""


import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apis.baselogic import BaseLogic
from process import const

logger = logging.getLogger("process")

# 画像拡張子
EXT_IMG = ["bmp", "gif", "png", "jpg", "jpeg", "tif", "tiff"]


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

    def send_gmail(self, user, detail, file_path):
        """gmailを送信する"""

        logger.debug("gmail send start. path=%s" % file_path)

        params = get_params(self, user, detail)
        if file_path is not None:
            # 添付ありメール
            send_multipart(detail, params, file_path)
            remove_file(file_path)
        else:
            # 添付なしメール
            send(params)

        logger.debug("gmail send end.")

        return self.get_next_exec_no(user, detail, None), None


def get_params(self, user, detail):
    """個別パラメータ取得"""

    keys = self.get_individual_keys(user.user_id, detail.id)
    host = port = account = passwd = None
    f_addr = t_addr = title = body = None
    for row in keys:
        if "SMTP_HOST" == row.key.key:
            host = row.char
        elif "SMTP_PORT" == row.key.key:
            port = row.num
        elif "SMTP_ACCOUNT" == row.key.key:
            account = row.char
        elif "SMTP_PASSWORD" == row.key.key:
            passwd = row.char
        elif "MAIL_FROM_ADDRESS" == row.key.key:
            f_addr = row.char
        elif "MAIL_TO_ADDRESS" == row.key.key:
            t_addr = row.char
        elif "MAIL_TITLE" == row.key.key:
            title = row.char
        elif "MAIL_BODY" == row.key.key:
            body = row.text

    return host, port, account, passwd, f_addr, t_addr, title, body


def send_multipart(detail, params, file_path):
    """添付ありメール送信"""

    host, port, account, passwd, f_addr, t_addr, title, body = params
    msg = MIMEMultipart()
    msg["Subject"] = title
    msg["From"] = f_addr
    msg["To"] = t_addr
    if "<html>" in body.lower():
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    # ファイルを添付
    with open(file_path, "rb") as f:
        if detail.action.o_type == const.TYPE_IO_IMG:
            part = MIMEImage(f.read())
        else:
            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
        part["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(
            file_path
        )
    msg.attach(part)

    # 認証
    sv = smtplib.SMTP(host, port)
    sv.starttls()
    sv.login(account, passwd)
    sv.send_message(msg)
    sv.quit()


def send(params):
    """添付なしメール送信"""

    host, port, account, passwd, f_addr, t_addr, title, body = params
    if "<html>" in body.lower():
        msg = MIMEText(body, "html")
    else:
        msg = MIMEText(body, "plain")

    msg["Subject"] = title
    msg["From"] = f_addr
    msg["To"] = t_addr

    # 認証
    sv = smtplib.SMTP(host, port)
    sv.starttls()
    sv.login(account, passwd)
    sv.send_message(msg)
    sv.quit()


def remove_file(file_path):
    """一時ファイル内のファイルの場合は削除"""
    if file_path.startswith("/code/media/tmp/"):
        os.remove(file_path)
        logger.debug("file removed. %s" % file_path)
