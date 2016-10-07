from django.conf.urls import url
from django.contrib import admin
from .views import login_user, logout_user
from .views import delete_user, list_user, edit_user
from .views import change_password, NewUserView

urlpatterns = [
    url(r'newuser/', NewUserView.as_view(), name='newuser'),
    url(r'login/', login_user, name='login'),
    url(r'logout/', logout_user, name='logout'),
    url(r'delete/$', delete_user, name='deleteuser'),
    url(r'^edituser/$', edit_user, name='edituser'),
    url(r'^change/$', change_password, name='changepassword'),
]
