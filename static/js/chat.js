// Chat Page JavaScript
const API_BASE = '/api';
let currentAgentId = null;

// Get URL parameter
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login/';
    }
}

// Get auth headers
function getAuthHeaders() {
    return {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json',
    };
}

// Show message
function showMessage(message, isError = false) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = isError ? 'message error' : 'message success';
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);
}

// Load agent info
async function loadAgentInfo(agentId) {
    try {
        const response = await fetch(`${API_BASE}/agents/${agentId}/`, {
            headers: getAuthHeaders(),
        });
        
        if (response.ok) {
            const agent = await response.json();
            document.getElementById('agentTitle').textContent = `🤖 Chat with ${agent.name}`;
            document.getElementById('agentInfo').innerHTML = `
                <p><strong>Name:</strong> ${agent.name}</p>
                <p><strong>Description:</strong> ${agent.description || 'N/A'}</p>
                <p><strong>System Prompt:</strong> ${agent.system_prompt}</p>
            `;
        } else if (response.status === 401) {
            window.location.href = '/login/';
        }
    } catch (error) {
        showMessage('Failed to load agent info', true);
    }
}

// Load chat history
async function loadChatHistory(agentId) {
    try {
        const response = await fetch(`${API_BASE}/chat/history/${agentId}/`, {
            headers: getAuthHeaders(),
        });
        
        if (response.ok) {
            const messages = await response.json();
            displayMessages(messages);
        } else if (response.status === 401) {
            window.location.href = '/login/';
        }
    } catch (error) {
        showMessage('Failed to load chat history', true);
    }
}

// Format message content with markdown-like styling
function formatMessage(content) {
    // Convert code blocks (```language\ncode\n```)
    content = content.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code class="language-${lang || 'plaintext'}">${escapeHtml(code.trim())}</code></pre>`;
    });
    
    // Convert inline code (`code`)
    content = content.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    // Convert bold (**text**)
    content = content.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Convert line breaks
    content = content.replace(/\n/g, '<br>');
    
    return content;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Display messages
function displayMessages(messages) {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = messages.map(msg => `
        <div class="chat-message ${msg.role}">
            ${formatMessage(msg.content)}
        </div>
    `).join('');
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message
document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to UI
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML += `
        <div class="chat-message user">${escapeHtml(message)}</div>
    `;
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    messageInput.value = '';
    messageInput.disabled = true;
    
    // Add typing indicator
    const typingId = 'typing-' + Date.now();
    chatMessages.innerHTML += `
        <div class="chat-message assistant typing-indicator" id="${typingId}">
            <span></span><span></span><span></span>
        </div>
    `;
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await fetch(`${API_BASE}/chat/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                agent_id: currentAgentId,
                message: message,
            }),
        });
        
        // Remove typing indicator
        document.getElementById(typingId)?.remove();
        
        if (response.ok) {
            const data = await response.json();
            
            // Add assistant response to UI with formatting
            chatMessages.innerHTML += `
                <div class="chat-message assistant">${formatMessage(data.response)}</div>
            `;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } else if (response.status === 401) {
            window.location.href = '/login/';
        } else {
            const error = await response.json();
            showMessage(error.error || 'Failed to send message', true);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', true);
    } finally {
        messageInput.disabled = false;
        messageInput.focus();
    }
});

// Upload file
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('agent_id', currentAgentId);
    
    try {
        const response = await fetch(`${API_BASE}/upload/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: formData,
        });
        
        if (response.ok) {
            showMessage('File uploaded successfully!');
            fileInput.value = '';
            loadFiles(currentAgentId);
        } else if (response.status === 401) {
            window.location.href = '/login/';
        } else {
            showMessage('Failed to upload file', true);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', true);
    }
});

// Load files
async function loadFiles(agentId) {
    try {
        const response = await fetch(`${API_BASE}/files/${agentId}/`, {
            headers: getAuthHeaders(),
        });
        
        if (response.ok) {
            const files = await response.json();
            displayFiles(files);
        } else if (response.status === 401) {
            window.location.href = '/login/';
        }
    } catch (error) {
        showMessage('Failed to load files', true);
    }
}

// Display files
function displayFiles(files) {
    const filesList = document.getElementById('filesList');
    
    if (files.length === 0) {
        filesList.innerHTML = '<p style="color: #666; font-size: 14px;">No files uploaded</p>';
        return;
    }
    
    filesList.innerHTML = files.map(file => `
        <div class="file-item">
            📄 ${file.filename}
        </div>
    `).join('');
}

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.clear();
    window.location.href = '/login/';
});

// Initialize
checkAuth();
currentAgentId = parseInt(getUrlParameter('agent_id'));

if (!currentAgentId) {
    window.location.href = '/agents/';
} else {
    loadAgentInfo(currentAgentId);
    loadChatHistory(currentAgentId);
    loadFiles(currentAgentId);
}
