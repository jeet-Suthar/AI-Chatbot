// DOM selection
const typingForm = document.querySelector(".typing-form");
const chatContainer = document.querySelector(".chat-list");
const suggestions = document.querySelectorAll(".suggestion");
const toggleThemeButton = document.querySelector("#theme-toggle-button");
const deleteChatButton = document.querySelector("#delete-chat-button");

// State variables
let userMessage = null;
let isResponseGenerating = false; // for stopping any response between generating previous one

// flask API url here we do backend thing
const API_URL = `https://ai-chatbot-rraj.onrender.com/chat`;


// Here i am using localStorage - built-in variable to store some values
// Load theme and chat data from local storage on page load
const loadDataFromLocalstorage = () => {
  const savedChats = localStorage.getItem("saved-chats"); // This feature can be properly implemented in future where have previous saved chats
                                                          // for now it serves basically to load home page with content
  const isLightMode = localStorage.getItem("themeColor") === "light_mode";
  // Apply the stored theme
  document.body.classList.toggle("light_mode", isLightMode);
  toggleThemeButton.innerText = isLightMode ? "dark_mode" : "light_mode";
  // Restore saved chats or clear the chat container
  chatContainer.innerHTML = "";
  document.body.classList.toggle("hide-header", savedChats);
  chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to the bottom
};

// Create a new message element and return it....just create new msg blocks
const createMessageElement = (content, ...classes) => {
  const div = document.createElement("div");
  div.classList.add("message", ...classes);
  div.innerHTML = content;
  return div;
};

// printing output
const printingOutput = (data, textElement, incomingMessageDiv) => {
  incomingMessageDiv.querySelector(".icon").classList.add("hide"); // Hide send icon when generating response

  if (data.response.type === "table") {
    // ✅ Table response with row-by-row animation
    let table = document.createElement("table");
    textElement.innerHTML = ""; // Clear previous content

    let tabledata = data.response.data;
    if (!Array.isArray(tabledata) || tabledata.length === 0) {
      textElement.innerText = "No data available.";
      return;
    }

    let columns = Object.keys(tabledata[0]);

    // Generate table headers
    let headerRow = document.createElement("tr");
    columns.forEach(column => {
      let th = document.createElement("th");
      th.innerText = column;
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);
    textElement.appendChild(table); // Add table to DOM immediately

    // Row-by-row animation
    let index = 0;
    const addRow = () => {
      if (index < tabledata.length) {
        let row = document.createElement("tr");
        columns.forEach(column => {
          let td = document.createElement("td");
          td.innerText = tabledata[index][column];
          row.appendChild(td);
        });
        table.appendChild(row);
        index++;
        setTimeout(addRow, 100); // Delay for effect
      }
    };
    addRow(); // Start animation
  } 
  else if (data.response.type === "text") {
    // ✅ Typing effect for text response
    let fullText = data.response.data;
    textElement.innerText = ""; // Clear previous content

    let index = 0;
    const typeNext = () => {
      if (index < fullText.length) {
        textElement.innerText += fullText[index];
        index++;
        setTimeout(typeNext, 25); // Adjust typing speed
      }
    };
    typeNext(); // Start typing effect
  } 
  else {
    // ✅ Handle unexpected response types
    textElement.innerText = "Invalid response type.";
  }

  setTimeout(() => {
    isResponseGenerating = false; // Allow next input
    incomingMessageDiv.querySelector(".icon").classList.remove("hide"); // Show send icon again
  }, 300); // Small delay to avoid flickering
};


// Fetch response from the API based on user message
const generateAPIResponse = async (incomingMessageDiv) => {
  const textElement = incomingMessageDiv.querySelector(".text"); // Getting text element
  console.log("User input: " + textElement);

  try {
    // Send a POST request to the API with the user's message
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userMessage,
      }),
    });

    const data = await response.json();
    console.log("Data got from AI JS:\n" + JSON.stringify(data, null, 2));

    if (!response.ok) throw new Error(data.error.message);
    // Get the API response text and remove asterisks from it
    const apiResponse = data;

    printingOutput(apiResponse, textElement, incomingMessageDiv); // Show typing effect
  } catch (error) {
    // Handle error
    isResponseGenerating = false;
    textElement.innerText = error.message;
    textElement.parentElement.closest(".message").classList.add("error");
  } finally {
    incomingMessageDiv.classList.remove("loading");
  }
};

// Show a loading animation while waiting for the API response
const showLoadingAnimation = () => {
  const html = `<div class="message-content">
                  <img class="avatar" src="https://ai-chatbot-rraj.onrender.com/static/images/abstract-061-svgrepo-com(1).svg" alt="Gemini avatar">
                  <p class="text"></p>
                  <div class="loading-indicator">
                    <div class="loading-bar"></div>
                    <div class="loading-bar"></div> 
                    <div class="loading-bar"></div>
                  </div>
                </div>
                <span onClick="copyMessage(this)" class="icon material-symbols-rounded">content_copy</span>`;
  const incomingMessageDiv = createMessageElement(html, "incoming", "loading");
  chatContainer.appendChild(incomingMessageDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to the bottom
  generateAPIResponse(incomingMessageDiv);
};



// Handle sending outgoing chat messages
const handleOutgoingChat = () => {
  // trims outgoing msg
  userMessage =
    typingForm.querySelector(".typing-input").value.trim() || userMessage;
  if (!userMessage || isResponseGenerating) return; // Exit if there is no message or response is generating
  isResponseGenerating = true;

  const html = `<div class="message-content">
                  <img class="avatar" src="https://ai-chatbot-rraj.onrender.com/static/images/Jeet-Suthar-pfp.jpg" alt="User avatar">
                  <p class="text"></p>
                </div>`;

  const outgoingMessageDiv = createMessageElement(html, "outgoing");
  outgoingMessageDiv.querySelector(".text").innerText = userMessage;
  chatContainer.appendChild(outgoingMessageDiv);

  typingForm.reset(); // Clear input field
  document.body.classList.add("hide-header");
  chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to the bottom
  setTimeout(showLoadingAnimation, 500); // Show loading animation after a delay
};

// Toggle between light and dark themes
toggleThemeButton.addEventListener("click", () => {
  const isLightMode = document.body.classList.toggle("light_mode");
  localStorage.setItem("themeColor", isLightMode ? "light_mode" : "dark_mode");
  toggleThemeButton.innerText = isLightMode ? "dark_mode" : "light_mode";
});

// Delete all chats from local storage when button is clicked
deleteChatButton.addEventListener("click", () => {
  if (confirm("Are you sure you want to delete all the chats?")) {
    // localStorage.removeItem("saved-chats");
    loadDataFromLocalstorage();
  }
});

// Set userMessage and handle outgoing chat when a suggestion is clicked
suggestions.forEach((suggestion) => {
  suggestion.addEventListener("click", () => {
    userMessage = suggestion.querySelector(".text").innerText;
    handleOutgoingChat();
  });
});

// Copy message text to the clipboard
const copyMessage = (copyButton) => {
  const messageText = copyButton.parentElement.querySelector(".text").innerText;
  navigator.clipboard.writeText(messageText);
  copyButton.innerText = "done"; // Show confirmation icons
  setTimeout(() => (copyButton.innerText = "content_copy"), 1000); // Revert icon after 1 second
};
// Prevent default form submission and handle outgoing chat
typingForm.addEventListener("submit", (e) => {
  e.preventDefault();
  handleOutgoingChat();
});
loadDataFromLocalstorage();
