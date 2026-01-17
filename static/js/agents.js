// Agents Page JavaScript
const API_BASE = '/api';

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
    }, 5000);
}

// Load agents
async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE}/agents/`, {
            headers: getAuthHeaders(),
        });
        
        if (response.ok) {
            const agents = await response.json();
            displayAgents(agents);
        } else if (response.status === 401) {
            window.location.href = '/login/';
        } else {
            showMessage('Failed to load agents', true);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', true);
    }
}

// Display agents
function displayAgents(agents) {
    const agentsList = document.getElementById('agentsList');
    
    if (agents.length === 0) {
        agentsList.innerHTML = '<p style="color: #666;">No agents yet. Create your first agent!</p>';
        return;
    }
    
    agentsList.innerHTML = agents.map(agent => `
        <div class="agent-card">
            <h3>${agent.name}</h3>
            <p>${agent.description || 'No description'}</p>
            <p><strong>System Prompt:</strong> ${agent.system_prompt.substring(0, 100)}...</p>
            <div class="agent-actions">
                <button class="btn btn-primary" onclick="openChat(${agent.id})">Chat</button>
                <button class="btn btn-danger" onclick="deleteAgent(${agent.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Create agent
document.getElementById('createAgentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('agentName').value,
        description: document.getElementById('agentDescription').value,
        system_prompt: document.getElementById('systemPrompt').value,
    };
    
    try {
        const response = await fetch(`${API_BASE}/agents/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(formData),
        });
        
        if (response.ok) {
            showMessage('Agent created successfully!');
            e.target.reset();
            document.getElementById('systemPrompt').value = 'You are a helpful AI assistant.';
            loadAgents();
        } else {
            showMessage('Failed to create agent', true);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', true);
    }
});

// Delete agent
async function deleteAgent(agentId) {
    if (!confirm('Are you sure you want to delete this agent?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/agents/${agentId}/`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        
        if (response.ok) {
            showMessage('Agent deleted successfully!');
            loadAgents();
        } else {
            showMessage('Failed to delete agent', true);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', true);
    }
}

// Open chat
function openChat(agentId) {
    window.location.href = `/chat/?agent_id=${agentId}`;
}

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.clear();
    window.location.href = '/login/';
});

// Initialize
checkAuth();
loadAgents();
