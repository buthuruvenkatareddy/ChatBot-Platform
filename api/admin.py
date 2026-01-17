from django.contrib import admin
from .models import Agent, ChatMessage, UploadedFile

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('agent', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('agent', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('filename',)
