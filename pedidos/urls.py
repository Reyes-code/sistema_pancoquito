from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('', LogoutView.as_view(next_page='login'), name='logout'), 

]