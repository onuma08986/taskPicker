from django.urls import path, include

urlpatterns = [
    # RESTAPI機能（随時追記）
    path("twitter/", include("apis.external.twitter.urls")),
    path("youtube/", include("apis.external.youtube.urls")),
]
