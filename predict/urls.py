from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('index',views.index,name='index'),
    path('about',views.about,name='about'),
    path('prediction',views.prediction,name='prediction'),
    path('register',views.register,name='register'),
    
]
