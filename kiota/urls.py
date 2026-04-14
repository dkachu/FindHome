from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('house/<int:house_id>/', views.detail, name='detail'),
    path('about/', views.about, name='about'),      # Link for About Us
    path('contact/', views.contact, name='contact'), # Link for Contact
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'), #management
    path('logout/', views.custom_logout, name='logout'),

]
