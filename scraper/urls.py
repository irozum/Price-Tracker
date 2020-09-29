from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('<int:pk>/delete/', views.LinkDelete.as_view())
]