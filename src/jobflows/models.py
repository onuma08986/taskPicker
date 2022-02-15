from django.db import models
from django.utils.timezone import now
from accounts.models import User


class Service(models.Model):
    """サービスクラス"""

    sname = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="表記名（略）"
    )
    fname = models.CharField(max_length=255, verbose_name="表記名")
    module = models.CharField(max_length=255, verbose_name="モジュール")
    image = models.ImageField(null=True, blank=True, verbose_name="サムネイル")
    status = models.SmallIntegerField(default=1, verbose_name="状態")
    is_active = models.BooleanField(default=False, verbose_name="利用可")
    update_at = models.DateTimeField(default=now, verbose_name="最終更新日時")

    def __str__(self):
        return self.fname

    class Meta:
        verbose_name_plural = "サービス"


class Authenticate(models.Model):
    """認証テーブル"""

    title = models.CharField(max_length=255, verbose_name="タイトル")
    oa = models.CharField(max_length=255, null=True, blank=True)
    nk = models.CharField(max_length=255, null=True, blank=True)
    np = models.CharField(max_length=255, null=True, blank=True)
    tk = models.CharField(max_length=255, null=True, blank=True)
    update_at = models.DateTimeField(default=now, verbose_name="最終更新日時")

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, verbose_name="サービス"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="ユーザー"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "認証"


class Action(models.Model):
    """アクションテーブル"""

    method = models.CharField(max_length=50, verbose_name="メソッド")
    image = models.ImageField(null=True, blank=True, verbose_name="サムネイル")
    title = models.CharField(max_length=255, verbose_name="タイトル")
    exp1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明１")
    exp2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明２")
    i_type = models.SmallIntegerField(default=1, verbose_name="入力形式")
    o_type = models.SmallIntegerField(default=1, verbose_name="出力形式")
    status = models.SmallIntegerField(default=1, verbose_name="状態")
    update_at = models.DateTimeField(default=now, verbose_name="最終更新日時")

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, verbose_name="サービス"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "アクション"


class Condition(models.Model):
    """条件テーブル"""

    method = models.CharField(max_length=50, verbose_name="メソッド")
    image = models.ImageField(null=True, blank=True, verbose_name="サムネイル")
    title = models.CharField(max_length=255, verbose_name="タイトル")
    exp1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明１")
    exp2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明２")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "条件"


class Key(models.Model):
    """キーテーブル"""

    name = models.CharField(max_length=255, verbose_name="キー名")
    key = models.CharField(unique=True, max_length=255, verbose_name="キー")
    exp1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明１")
    exp2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明２")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "キー"


class ActionKey(models.Model):
    """アクションキーテーブル"""

    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, null=True, verbose_name="アクション"
    )
    key = models.ForeignKey(Key, on_delete=models.CASCADE, null=True, verbose_name="キー")

    def __str__(self):
        return "%s (%s)" % (self.action.title, self.key.name)

    class Meta:
        verbose_name_plural = "アクションキー"


class ActionCondition(models.Model):
    """アクション条件テーブル"""

    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, null=True, verbose_name="アクション"
    )
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, null=True, verbose_name="条件"
    )

    def __str__(self):
        return "%s (%s)" % (self.action.title, self.condition.title)

    class Meta:
        verbose_name_plural = "アクション条件"


class Flow(models.Model):
    """フローテーブル"""

    title = models.CharField(max_length=255, verbose_name="タイトル")
    exp1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明１")
    exp2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="説明２")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "フロー"


class FlowDetail(models.Model):
    """フロー明細テーブル"""

    execno = models.SmallIntegerField(verbose_name="実行NO")
    next_execno = models.SmallIntegerField(null=True, blank=True, verbose_name="後続実行NO")

    flow = models.ForeignKey(
        Flow, on_delete=models.CASCADE, null=True, verbose_name="フロー"
    )
    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, null=True, verbose_name="アクション"
    )

    def __str__(self):
        return "%s / %s / %s" % (self.flow.title, self.execno, self.action.title)

    class Meta:
        verbose_name_plural = "フロー明細"


class IndividualKeys(models.Model):
    """個別キー設定テーブル"""

    char = models.CharField(max_length=255, null=True, blank=True, verbose_name="文字列")
    file = models.FileField(upload_to="files/", null=True, blank=True)
    text = models.TextField(null=True, blank=True, verbose_name="フリー")
    bool = models.BooleanField(verbose_name="ON/OFF")
    num = models.IntegerField(null=True, blank=True, verbose_name="数値")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="ユーザー"
    )
    flowdetail = models.ForeignKey(
        FlowDetail, on_delete=models.CASCADE, null=True, verbose_name="フロー明細"
    )
    key = models.ForeignKey(
        Key, on_delete=models.CASCADE, null=True, verbose_name="アクションキー"
    )

    def __str__(self):
        return "%s / %s / %s / %s" % (
            self.user.user_id,
            self.flowdetail.flow.title,
            self.flowdetail.execno,
            self.key.name,
        )

    class Meta:
        verbose_name_plural = "個別キー設定"


class IndividualConditions(models.Model):
    """個別条件設定テーブル"""

    next_execno = models.SmallIntegerField(null=True, blank=True, verbose_name="後続実行NO")
    priority = models.SmallIntegerField(null=True, blank=True, verbose_name="実行順")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="ユーザー"
    )
    flowdetail = models.ForeignKey(
        FlowDetail, on_delete=models.CASCADE, null=True, verbose_name="フロー明細"
    )
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, null=True, verbose_name="条件"
    )

    def __str__(self):
        return "%s / %s / %s" % (
            self.user.user_id,
            self.flowdetail.flow.title,
            self.condition.title,
        )

    class Meta:
        verbose_name_plural = "個別条件設定"


class Schedule(models.Model):
    """スケジュールテーブル"""

    intval = models.SmallIntegerField(default=0, blank=True, verbose_name="実行間隔（分）")
    date = models.CharField(max_length=8, null=True, blank=True, verbose_name="実行日")
    time = models.CharField(max_length=4, null=True, blank=True, verbose_name="実行時間")
    week = models.CharField(max_length=7, null=True, blank=True, verbose_name="実行曜日")
    s_from = models.CharField(max_length=8, null=True, blank=True, verbose_name="開始日")
    s_to = models.CharField(max_length=8, null=True, blank=True, verbose_name="終了日")
    status = models.SmallIntegerField(default=0, blank=True, verbose_name="状態")
    exec_at = models.CharField(
        max_length=17, null=True, blank=True, verbose_name="最終実行日時"
    )
    err_msg = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="エラーメッセージ"
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="ユーザー"
    )
    flow = models.ForeignKey(
        Flow, on_delete=models.CASCADE, null=True, verbose_name="フロー"
    )

    class Meta:
        verbose_name_plural = "スケジュール"
