from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views 
from django.contrib.auth.views import LogoutView
from profiles.views import FriendView

urlpatterns = [
    path('places/', include('maps.urls')),
    path('logout', LogoutView.as_view()),
    path('', views.home, name='home'),
    path('profile/', include('profiles.urls'), name='profile'),
    path('map/<str:location>/', views.map, name='map'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('map/<str:start>/<str:end>/', views.mapDirections, name='mapDirections'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

