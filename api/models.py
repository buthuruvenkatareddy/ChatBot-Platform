from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    """Agent/Project model for each user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    system_prompt = models.TextField(default="You are a helpful AI assistant.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class ChatMessage(models.Model):
    """Chat message history for each agent"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.agent.name} - {self.role} - {self.created_at}"


class UploadedFile(models.Model):
    """Files uploaded per agent"""
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='agent_files/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.agent.name} - {self.filename}"
