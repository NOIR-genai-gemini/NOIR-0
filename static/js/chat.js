
function markdownToHtml(markdownText) {
  // Replace headers (###)
  markdownText = markdownText.replace(/###\s(.+?)\n/g, '<h3>$1</h3>');

  // Replace headers (##)
  markdownText = markdownText.replace(/##\s(.+?)\n/g, '<h2>$1</h2>');

  // Replace headers (#)
  markdownText = markdownText.replace(/#\s(.+?)\n/g, '<h1>$1</h1>');

  // Replace bold (**text**)
  markdownText = markdownText.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Replace italic (*text*)
  markdownText = markdownText.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Replace inline code (`code`)
  markdownText = markdownText.replace(/`(.+?)`/g, '<code>$1</code>');

  // Replace unordered lists (* item)
  markdownText = markdownText.replace(/\n\*\s(.+?)(?=\n)/g, '<li>$1</li>');

  // Replace paragraphs
  markdownText = markdownText.replace(/(.+?)(?=\n\n)/g, '<p>$1</p>');

  // Replace line breaks
  markdownText = markdownText.replace(/\n/g, '<br>');

  return markdownText;
}

function sendMessage() {
var userInput = document.getElementById("user-input").value;
var chatContainer = document.getElementById("chat-container");

// Create a new message element for the user's message
var messageElement = document.createElement("div");
messageElement.classList.add("chat-message", "user-message");
messageElement.textContent = userInput;
chatContainer.appendChild(messageElement);

// Clear input field
document.getElementById("user-input").value = "";

// Scroll to the bottom of the chat container
chatContainer.scrollTop = chatContainer.scrollHeight;

// Send user input to Flask route
fetch("/process", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ message: userInput }),
})
  .then((response) => response.json())
  .then((data) => {
    // Create a new message element for the bot's response
    var botMessageElement = document.createElement("div");
    botMessageElement.classList.add("chat-message", "bot-message");
    botMessageElement.innerHTML = markdownToHtml(data.message);
    chatContainer.appendChild(botMessageElement);

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
  })
  .catch((error) => {
    console.error("Error:", error);
  });
}

  