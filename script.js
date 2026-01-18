document.addEventListener('DOMContentLoaded', () => {
    const chatWidget = document.getElementById('chat-widget');
    const chatBubble = document.getElementById('chat-bubble');
    const closeChatBtn = document.getElementById('close-chat');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearChatBtn = document.getElementById('clear-chat');

    const API_URL = '/api/chat';

    // Toggle Chat Panel
    chatBubble.addEventListener('click', () => {
        chatWidget.classList.add('active');
        userInput.focus();
    });

    closeChatBtn.addEventListener('click', () => {
        chatWidget.classList.remove('active');
    });

    const addMessage = (text, isBot = true) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('msg');
        messageDiv.classList.add(isBot ? 'bot' : 'user');

        // Basic formatting for newlines and potential links
        const formattedText = text.replace(/\n/g, '<br>');
        messageDiv.innerHTML = formattedText;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const showTyping = (show) => {
        typingIndicator.style.display = show ? 'flex' : 'none';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();

        if (!message) return;

        // User Message
        addMessage(message, false);
        userInput.value = '';

        // Bot Response
        showTyping(true);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            showTyping(false);

            if (data.response) {
                addMessage(data.response, true);
            } else if (data.error) {
                addMessage('Error: ' + data.error, true);
            }
        } catch (error) {
            showTyping(false);
            addMessage('Error: Connection failed. Please check the terminal.', true);
        }
    });

    clearChatBtn.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        addMessage('Terminal cleared. Welcome back. I am Atlas, your intelligence layer. How can I assist your trading today?', true);
    });
});
