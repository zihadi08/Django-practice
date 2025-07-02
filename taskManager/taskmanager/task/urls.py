from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('toggle/<int:task_id>/', views.toggle_complete, name='toggle'),
    path('delete/<int:task_id>/', views.delete_task, name='delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]