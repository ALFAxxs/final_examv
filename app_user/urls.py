from django.urls import path

from .views import login_page, registration_page, home_page, create_account, logout_user, delete_account, update_account, filtered_account, update_user

urlpatterns = [
    path('', login_page, name='login'),
    path('registration/', registration_page, name='registration'),
    path('home/<int:id>', home_page, name='home'),
    path('home/update-user/<int:id>', update_user, name='update_user'),
    path('home/<int:id>/filter', filtered_account, name='filtered_home'),
    path('new/<int:id>', create_account, name='new'),
    path('logout/', logout_user, name='logout'),
    path('delete/<int:id>', delete_account, name='delete'),
    path('update/<int:id>', update_account, name='update')
]