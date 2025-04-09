const chatbox = document.getElementById('chatbox');

function appendMessage(message, sender) {
  const p = document.createElement('p');
  p.innerHTML = `<strong>${sender}:</strong> ${message}`;
  p.className = sender === 'Bot' ? 'bot-msg' : 'user-msg';
  chatbox.appendChild(p);
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
  const inputBox = document.getElementById('userInput');
  const userInput = inputBox.value.trim();
  if (!userInput) return;

  appendMessage(userInput, 'You');
  inputBox.value = '';

  const typingMsg = document.createElement('p');
  typingMsg.className = 'bot-msg typing-indicator';
  typingMsg.textContent = 'Bot is typing...';
  chatbox.appendChild(typingMsg);
  chatbox.scrollTop = chatbox.scrollHeight;

  try {
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    typingMsg.remove();
    appendMessage(data.reply, 'Bot');
  } catch (err) {
    typingMsg.remove();
    appendMessage("❌ Server error!", 'Bot');
  }
}
