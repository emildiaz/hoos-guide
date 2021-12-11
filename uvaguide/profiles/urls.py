from django.urls import path
from . import views
from .views import FriendView

#add namespace
app_name = 'profiles'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('friends/', FriendView.as_view(), name='friends'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('add_friend/<int:friend_id>', views.send_request, name='send_request'),
    path('view_friend/<int:friend_id>', views.view_friend, name='view_friend'),
    path('accept/<int:friend_id>', views.accept, name='accept'),
    path('deny/<int:friend_id>', views.deny, name='deny'),
]