
from django.urls import path
from .views import Player_Information_View,ReportView

urlpatterns = [
    path('playerinfo/',Player_Information_View.as_view(), name="player_information"),
    path('report/',ReportView.as_view(),name="Report"),
]