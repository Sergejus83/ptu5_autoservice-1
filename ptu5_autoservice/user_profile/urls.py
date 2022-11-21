from django.urls import path
from . import views

# (kelias i puslapi, funkcija register is view, linko pavadinimas)
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]
