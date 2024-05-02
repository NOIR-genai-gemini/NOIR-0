
    function sendMessage() {
      var userInput = document.getElementById("user-input").value;
      var chatContainer = document.getElementById("chat-container");

      //  new message 
      var messageElement = document.createElement("div");
      messageElement.classList.add("chat-message", "user-message");
      messageElement.textContent = userInput;

      //  message element to  chat container
      chatContainer.appendChild(messageElement);

      // Clear  input field
      document.getElementById("user-input").value = "";

      // bot response
      setTimeout(function() {
        var botResponse = "This is chintu, How can I help you.";
        var botMessageElement = document.createElement("div");
        botMessageElement.classList.add("chat-message", "bot-message");
        botMessageElement.textContent = botResponse;
        chatContainer.appendChild(botMessageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight; 
      }, 1000);
    }
   