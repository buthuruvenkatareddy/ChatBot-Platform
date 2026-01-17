// Authentication JavaScript
const API_BASE = '/api';

// Check if user is already logged in
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (token && window.location.pathname.includes('login')) {
        window.location.href = '/agents/';
    }
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

// Login Form Handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch(`${API_BASE}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                localStorage.setItem('username', data.user.username);
                showMessage('Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/agents/';
                }, 1000);
            } else {
                showMessage(data.error || 'Login failed', true);
            }
        } catch (error) {
            showMessage('Network error. Please try again.', true);
        }
    });
}

// Register Form Handler
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch(`${API_BASE}/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                localStorage.setItem('username', data.user.username);
                showMessage('Registration successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/agents/';
                }, 1000);
            } else {
                showMessage(JSON.stringify(data) || 'Registration failed', true);
            }
        } catch (error) {
            showMessage('Network error. Please try again.', true);
        }
    });
}

// Logout Function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    window.location.href = '/login/';
}

// Check auth on page load
checkAuth();
