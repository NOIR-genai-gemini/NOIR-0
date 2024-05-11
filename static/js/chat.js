
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

window.onload = function() {
  fetch('/get_previous_messages')
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(messages => {

const chatContainer = document.getElementById('chat-container');

messages.forEach((message, index) => {
  console.log(message);
  if (index % 2 === 0) {
      // Create a div for user message (even index)
      var messageElement = document.createElement("div");
      messageElement.classList.add("chat-message", "user-message");
      messageElement.textContent = message; // Assuming message is the user's message
      chatContainer.appendChild(messageElement);
  } else {
      // Create a div for bot message (odd index)
      var botMessageElement = document.createElement("div");
      botMessageElement.classList.add("chat-message", "bot-message");
      botMessageElement.innerHTML = markdownToHtml(message); // Assuming message is the bot's message
      chatContainer.appendChild(botMessageElement);
  }
});
      })
      .catch(error => {
          console.error('Error:', error);
      });};

  