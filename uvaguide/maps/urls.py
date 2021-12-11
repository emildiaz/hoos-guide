from django.urls import path
from . import views
from .views import PlaceView

#add namespace
app_name = 'maps'

urlpatterns = [
    path('', PlaceView.as_view(), name='place'),
    path('<int:place_id>/', views.detail, name='detail'),
    path('<int:place_id>/like/', views.like, name='like'),
]