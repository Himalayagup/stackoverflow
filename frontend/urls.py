from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('register/', views.Register.as_view(),name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view,   name='logout'),
    path('search/', views.SearchPageView.as_view(), name="search"),
    path('ask/', views.AddQuestionView.as_view(), name='add_new_question')
]
