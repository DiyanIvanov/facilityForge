from django.urls import path
from common.views import IndexPageView, AboutPageView, DashboardView

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]