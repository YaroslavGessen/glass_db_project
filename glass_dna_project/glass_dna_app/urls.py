from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='app-home-page'),
    path('about/', views.about_page, name='app-about-page'),
]
