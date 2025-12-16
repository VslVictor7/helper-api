from django.urls import path
from .views import (
    ImagesView,
    ImagePNGView,
    ImageByNameView,
    MobsView,
    DeathsView,
)

urlpatterns = [
    path("images/", ImagesView.as_view()),
    path("images/png/<str:filename>/", ImagePNGView.as_view()),
    path("images/<str:name>/", ImageByNameView.as_view()),
    path("mobs/", MobsView.as_view()),
    path("deaths/", DeathsView.as_view()),
]