from django.urls import path
from . import views

urlpatterns = [
    # C'est ce "name='login'" que Django cherche
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]