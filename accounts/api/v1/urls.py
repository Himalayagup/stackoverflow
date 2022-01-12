from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("logout/", views.Logout.as_view(), name="rest_logout"),
    path("login/", views.CustomLoginView.as_view(), name="rest_login"),
]
