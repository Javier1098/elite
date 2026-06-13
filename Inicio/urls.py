from django.urls import path
from django.contrib.auth.views import LogoutView
from.import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from .views import dashboard

from .views import login_view




urlpatterns = [
    
#Estas son las rutas de inicio de sesion
    
path('', views.apertura, name='apertura'),  
path('logout/', views.logout_view, name='logout'),
path('accounts/login/', login_view, name='login'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)