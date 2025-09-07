from django.urls import path
from . import views



urlpatterns = [


path('', views.home, name='home'),
path('api_info/', views.api_info, name='api_info'),
path('send-message/<str:text>',views.send_message,name = 'send_message'),
path('post-alert/' , views.post_alert, name='post_alert'),


]