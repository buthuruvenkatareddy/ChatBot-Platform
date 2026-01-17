from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('agents/', TemplateView.as_view(template_name='agents.html'), name='agents'),
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat'),
]
