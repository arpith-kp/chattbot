from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('rest/public/chatbot/1.0/send', views.egnyte_post, name='bridgedetails'),
]
