from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Agent, ChatMessage, UploadedFile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class AgentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Agent
        fields = ('id', 'user', 'name', 'description', 'system_prompt', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'agent', 'role', 'content', 'created_at')
        read_only_fields = ('created_at',)


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id', 'agent', 'file', 'filename', 'uploaded_at')
        read_only_fields = ('uploaded_at',)


class ChatRequestSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    message = serializers.CharField()
