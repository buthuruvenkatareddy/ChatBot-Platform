from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Agent endpoints
    path('agents/', views.AgentListCreateView.as_view(), name='agent-list-create'),
    path('agents/<int:pk>/', views.AgentDetailView.as_view(), name='agent-detail'),
    
    # Chat endpoints
    path('chat/', views.chat_with_agent, name='chat'),
    path('chat/history/<int:agent_id>/', views.get_chat_history, name='chat-history'),
    
    # File upload endpoints
    path('upload/', views.upload_file, name='upload-file'),
    path('files/<int:agent_id>/', views.get_agent_files, name='agent-files'),
]
