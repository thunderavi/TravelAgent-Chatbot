async function sendMessage(event) {
    event.preventDefault();

    const input = document.getElementById('user-input');
    const message = input.value;

    // Display user message
    displayMessage(message, 'user');

    // Clear input field
    input.value = '';

    try {
        const response = await fetch('/get-itinerary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        displayMessage(data.reply, 'bot');
    } catch (error) {
        console.error('Error:', error);
        displayMessage("Sorry, there was an error. Please try again later.", 'bot');
    }
}

function displayMessage(message, sender) {
    const chatWindow = document.getElementById('chat-window');
    const messageElement = document.createElement('p');
    messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
}
