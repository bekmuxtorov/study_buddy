from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('add_room/', views.add_room_page, name='add_room'),
    path('room/<str:pk>', views.room_detail_view, name='room_detail'),
    path('room/delete/<str:pk>', views.room_delete, name='room_delete'),
    path('room/update/<str:pk>', views.room_update, name='room_update'),
    path('message/delete/<str:pk>', views.message_delete, name='message_delete'),
    path('message/update/<str:pk>', views.message_update, name='message_update'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
