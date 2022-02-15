from .logic import Logic
from django.urls import path, include


urlpatterns = [
    path('list', Logic.list, name="list"),
    path('insert/video', Logic.insert_video, name="video"),
    path('insert/title', Logic.insert_title, name="title"),
    path('update', Logic.update, name="update"),
    path('delete', Logic.delete, name="delete"),
]