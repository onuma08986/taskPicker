"""URL Configuration"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import SignUp
from accounts import views

urlpatterns = [
    # システム認証機能
    path("admin/", admin.site.urls),
    # トップ画面
    path("", views.top, name="top"),
    # 汎用画面
    path("", include("django.contrib.auth.urls")),
    # ユーザ登録画面
    path("signup/", SignUp.as_view(), name="signup"),
    # メイン機能
    # path('main', include('main.urls')),
    # RESTAPI機能
    path("rest/", include("apis.urls")),
]
