from django.urls import path
from . import views

urlpatterns = [
    path("", views.ComingSoonView.as_view()),
    path("news/", views.MainPageView.as_view()),
    path("news/<int:link>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/create/", views.CreateNewsView.as_view()),
]
