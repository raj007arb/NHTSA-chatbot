function loadChart(chartType) {
    let chartDisplay = document.getElementById("chartDisplay");

    // Hide the image initially before loading a new one
    chartDisplay.style.display = "none";

    fetch('http://127.0.0.1:5000/get_chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chart_type: chartType })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to load chart");
        }
        return response.blob();
    })
    .then(blob => {
        if (blob.size === 0) {  // If response is empty, don't show image
            console.warn("⚠️ No chart received.");
            return;
        }

        const imgUrl = URL.createObjectURL(blob);
        chartDisplay.src = imgUrl;
        chartDisplay.style.display = "block"; // Show image when loaded
    })
    .catch(error => {
        console.error("❌ Error loading chart:", error);
        chartDisplay.style.display = "none"; // Hide image on error
    });
}


async function sendMessage() {
    let inputField = document.getElementById("userMessage");
    let chatBox = document.getElementById("chatBox");

    if (!inputField || !chatBox) {
        console.error("❌ Missing required elements.");
        return;
    }

    let userInput = inputField.value.trim();
    if (userInput === "") {
        console.warn("⚠️ Warning: Empty message.");
        return;
    }

    // Create user message container
    let userMessageContainer = document.createElement("div");
    userMessageContainer.classList.add("message-container", "user-message-container");

    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerText = userInput;

    userMessageContainer.appendChild(userMessage);
    chatBox.appendChild(userMessageContainer);

    // Clear input field
    inputField.value = "";

    // Scroll to latest message
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        let response = await fetch("http://127.0.0.1:5000/chatbot", { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        });

        let data = await response.json();
        console.log("📥 Chatbot Response:", data);

        // Create bot message container
        let botMessageContainer = document.createElement("div");
        botMessageContainer.classList.add("message-container", "bot-message-container");

        let botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot-message");
        botMessage.innerText = data.response || "Error in response";

        botMessageContainer.appendChild(botMessage);
        chatBox.appendChild(botMessageContainer);

        // Scroll to latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error("❌ Fetch Error:", error);
    }
}


document.getElementById("recallForm").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent default form submission

    // Get user input values
    let make = document.getElementById("make").value.trim();
    let model = document.getElementById("model").value.trim();
    let modelYear = document.getElementById("modelYear").value.trim();

    // Create JSON payload
    let requestData = {
        make: make,
        model: model,
        model_year: modelYear
    };

    // Send request to Flask backend
    let response = await fetch("http://127.0.0.1:5000/get_vehicle_data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    });
});



