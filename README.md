# Multi-User AI Agent Chatbot Platform

A complete full-stack chatbot platform where users can create multiple AI agents with custom system prompts and chat with them using OpenRouter API.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django 4.2 + Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: PostgreSQL
- **AI API**: OpenRouter (Mistral-7B-Instruct-Free)
- **File Storage**: Django Media folder (local)

## Features

User registration and login with JWT authentication  
Create multiple AI agents/projects per user  
Custom system prompts for each agent  
Real-time chat with AI agents  
Chat history storage and retrieval  
File upload per agent  
Secure password hashing  
Clean REST API design  
Responsive UI  

## Project Structure

```
Chatbot Platform/
├── chatbot_platform/          # Main Django project
│   ├── __init__.py
│   ├── settings.py            # Django settings with PostgreSQL & JWT config
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── api/                       # Backend API app
│   ├── models.py              # Agent, ChatMessage, UploadedFile models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API views
│   ├── urls.py                # API routes
│   ├── services.py            # OpenRouter API integration
│   └── admin.py               # Django admin config
├── frontend/                  # Frontend URL routing app
│   ├── urls.py
│   └── apps.py
├── templates/                 # HTML templates
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── agents.html            # Agent management page
│   └── chat.html              # Chat interface
├── static/                    # Static files
│   ├── css/
│   │   └── style.css          # Complete styling
│   └── js/
│       ├── auth.js            # Login/Register logic
│       ├── agents.js          # Agent management logic
│       └── chat.js            # Chat interface logic
├── media/                     # User uploaded files (auto-created)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## Installation & Setup

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### 2. Clone/Navigate to Project

```bash
cd "C:\Users\Venkat\Downloads\Chatbot Platform"
```

### 3. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup PostgreSQL Database

Create a PostgreSQL database:

```sql
CREATE DATABASE chatbot_platform_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE chatbot_platform_db TO postgres;
```

Or update the `.env` file with your PostgreSQL credentials.

### 6. Configure Environment Variables

The `.env` file is already created with your OpenRouter API key. Update other variables if needed:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=chatbot_platform_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
OPENROUTER_API_KEY=
```

### 7. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/login/` - Login user (returns JWT tokens)
- `POST /api/token/refresh/` - Refresh access token

### Agents
- `GET /api/agents/` - List all user's agents
- `POST /api/agents/` - Create new agent
- `GET /api/agents/{id}/` - Get agent details
- `PUT /api/agents/{id}/` - Update agent
- `DELETE /api/agents/{id}/` - Delete agent

### Chat
- `POST /api/chat/` - Send message to agent
- `GET /api/chat/history/{agent_id}/` - Get chat history

### Files
- `POST /api/upload/` - Upload file for agent
- `GET /api/files/{agent_id}/` - Get agent's uploaded files

## Usage

### 1. Register/Login
- Navigate to http://127.0.0.1:8000/
- Click "Register" to create a new account
- Or "Login" if you already have an account

### 2. Create an Agent
- After login, you'll be on the Agents page
- Fill in the "Create New Agent" form:
  - **Name**: Give your agent a name (e.g., "Code Helper")
  - **Description**: Optional description
  - **System Prompt**: Define the agent's behavior (e.g., "You are an expert Python programmer")
- Click "Create Agent"

### 3. Chat with Agent
- Click "Chat" on any agent card
- Type messages in the chat input
- The AI will respond based on the agent's system prompt
- Upload files using the sidebar (optional)

### 4. Manage Agents
- View all your agents on the Agents page
- Delete agents you no longer need

## OpenRouter API Configuration

The project uses the **Mistral-7B-Instruct-Free** model from OpenRouter:

- **Model**: `mistralai/mistral-7b-instruct-free`
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **API Key**: Set in `.env` file

The API key is already configured in your `.env` file.

## Security Features

-  Secure password hashing (Django default PBKDF2)
-  JWT token authentication
-  Token refresh mechanism
-  Protected API routes
-  CORS configuration
-  Environment variable management

## Database Schema

### User (Django built-in)
- username, email, password

### Agent
- user (ForeignKey)
- name
- description
- system_prompt
- created_at, updated_at

### ChatMessage
- agent (ForeignKey)
- role (user/assistant)
- content
- created_at

### UploadedFile
- agent (ForeignKey)
- file
- filename
- uploaded_at

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Verify credentials in `.env` file
- Check if database exists

### API Key Error
- Verify `OPENROUTER_API_KEY` in `.env` file
- Check API key validity at https://openrouter.ai/

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
```bash
python manage.py runserver 8080
```

## Development

To add the frontend app to INSTALLED_APPS:

```python
# chatbot_platform/settings.py
INSTALLED_APPS = [
    ...
    'api',
    'frontend',  # Add this
]
```

## Production Deployment

Before deploying to production:

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` in `.env`
3. Generate a strong `DJANGO_SECRET_KEY`
4. Configure PostgreSQL for production
5. Set up HTTPS
6. Configure static file serving (WhiteNoise/Nginx)
7. Use environment-specific settings

## License

This project is open-source and available for educational purposes.

## Support

For issues or questions, please refer to:
- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
- OpenRouter docs: https://openrouter.ai/docs

---

**Built with ❤️ using Django + OpenRouter API**
