from django.urls import path

from applications.views import ApplicationView

urlpatterns = [
    path('', ApplicationView.as_view(), name='applications'),
]