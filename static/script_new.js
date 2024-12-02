const form = document.getElementById("queryForm");
const chatContainer = document.getElementById("chatContainer");
const errorContainer = document.getElementById("errorContainer");

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    chatContainer.style.display = "block";
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Clear error state and get input
    errorContainer.style.display = "none";
    const submitBtn = document.getElementById("submitBtn");
    submitBtn.disabled = true;
    submitBtn.textContent = "Analyzing...";
    
    const queryInput = document.getElementById("query").value;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ message: queryInput }),
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`Server Error: ${res.status} - ${errorText}`);
        }

        const data = await res.json();

        // Add messages to chat
        addMessage(queryInput, true);
        addMessage(`Category: ${data.category}\nEscalation: ${data.escalation}\nSentiment: ${data.sentiment}`, false);

    } catch (err) {
        errorContainer.textContent = err.message;
        errorContainer.style.display = "block";
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Analyze Query";
    }
});