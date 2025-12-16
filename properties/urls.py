from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('add/', views.add_property, name='add_property'),
    path('<int:property_id>/add-room/', views.add_room, name='add_room'),
    path('room/<int:pk>/edit/', views.edit_room, name='edit_room'),
]
