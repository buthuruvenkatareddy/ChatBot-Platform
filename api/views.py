from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Agent, ChatMessage, UploadedFile
from .serializers import (
    UserSerializer, AgentSerializer, ChatMessageSerializer,
    UploadedFileSerializer, ChatRequestSerializer
)
from .services import call_openrouter_api
import os
from PyPDF2 import PdfReader
from docx import Document


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """User registration endpoint"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """User login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AgentListCreateView(generics.ListCreateAPIView):
    """List and create agents for authenticated user"""
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Agent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an agent"""
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Agent.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_agent(request):
    """Send a message to an agent and get AI response"""
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    agent_id = serializer.validated_data['agent_id']
    user_message = serializer.validated_data['message']

    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
    except Agent.DoesNotExist:
        return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

    # Save user message
    ChatMessage.objects.create(
        agent=agent,
        role='user',
        content=user_message
    )

    # Get uploaded files and read their content
    uploaded_files = UploadedFile.objects.filter(agent=agent)
    file_contents = []
    
    for uploaded_file in uploaded_files:
        try:
            file_path = uploaded_file.file.path
            file_extension = os.path.splitext(uploaded_file.filename)[1].lower()
            content = ""
            
            # Read PDF files
            if file_extension == '.pdf':
                pdf_reader = PdfReader(file_path)
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
            
            # Read DOCX files
            elif file_extension in ['.docx', '.doc']:
                doc = Document(file_path)
                for paragraph in doc.paragraphs:
                    content += paragraph.text + "\n"
            
            # Read text files
            elif file_extension in ['.txt', '.md', '.csv', '.json', '.xml']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            # If we got content, add it
            if content.strip():
                file_contents.append(f"=== File: {uploaded_file.filename} ===\n{content}\n{'='*50}\n")
        except Exception as e:
            # Log error but continue
            print(f"Error reading file {uploaded_file.filename}: {str(e)}")
            continue
    
    # Build enhanced system prompt with file contents
    enhanced_system_prompt = agent.system_prompt
    if file_contents:
        enhanced_system_prompt += "\n\n" + "="*50
        enhanced_system_prompt += "\nYOU HAVE ACCESS TO THE FOLLOWING UPLOADED DOCUMENTS:\n"
        enhanced_system_prompt += "="*50 + "\n\n"
        enhanced_system_prompt += "\n".join(file_contents)
        enhanced_system_prompt += "\n" + "="*50
        enhanced_system_prompt += "\nIMPORTANT: Use the information from these documents to answer questions. When asked about specific details (names, dates, projects, skills, etc.), refer directly to the content above."
        enhanced_system_prompt += "\n" + "="*50

    # Get chat history
    chat_history = ChatMessage.objects.filter(agent=agent).order_by('created_at')
    messages = [{'role': msg.role, 'content': msg.content} for msg in chat_history]

    # Call OpenRouter API
    try:
        ai_response = call_openrouter_api(enhanced_system_prompt, messages)
        
        # Save assistant response
        ChatMessage.objects.create(
            agent=agent,
            role='assistant',
            content=ai_response
        )

        return Response({
            'response': ai_response,
            'agent_id': agent_id
        })
    except Exception as e:
        return Response({
            'error': f'Failed to get AI response: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request, agent_id):
    """Get chat history for a specific agent"""
    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
    except Agent.DoesNotExist:
        return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

    messages = ChatMessage.objects.filter(agent=agent)
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """Upload a file for a specific agent"""
    agent_id = request.data.get('agent_id')
    file = request.FILES.get('file')

    if not agent_id or not file:
        return Response({'error': 'agent_id and file are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
    except Agent.DoesNotExist:
        return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

    uploaded_file = UploadedFile.objects.create(
        agent=agent,
        file=file,
        filename=file.name
    )

    serializer = UploadedFileSerializer(uploaded_file)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agent_files(request, agent_id):
    """Get all uploaded files for a specific agent"""
    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
    except Agent.DoesNotExist:
        return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

    files = UploadedFile.objects.filter(agent=agent)
    serializer = UploadedFileSerializer(files, many=True)
    return Response(serializer.data)
