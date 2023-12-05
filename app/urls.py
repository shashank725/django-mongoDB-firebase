from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    # path('accounts/profile/view/', view_profile, name='view_profile'),
    # path('accounts/profile/edit/', edit_profile, name='edit_profile'),
]
