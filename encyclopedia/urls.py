from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path('create', views.create, name='create'),
    path("random", views.random, name="random"),
    path('edit/<str:title>', views.edit, name='edit'),
    path("<str:title>", views.page, name="page")
]
