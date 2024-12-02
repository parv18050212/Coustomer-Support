const form = document.getElementById("queryForm");
const responseContainer = document.getElementById("responseContainer");
const errorContainer = document.getElementById("errorContainer");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Clear previous responses
    responseContainer.style.display = "none";
    errorContainer.style.display = "none";

    const queryInput = document.getElementById("query").value;

    try {
        const res = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: queryInput }),
        });

        if (!res.ok) {
            const errorText = await res.text(); // Capture the error response
            throw new Error(`Server Error: ${res.status} - ${errorText}`);
        }

        const data = await res.json();

        // Populate the response
        document.getElementById("responseQuery").textContent = data.query;
        document.getElementById("responseEscalation").textContent = data.escalation;
        document.getElementById("responseCategory").textContent = data.category;
        document.getElementById("responseSentiment").textContent = data.sentiment;

        responseContainer.style.display = "block";
    } catch (err) {
        errorContainer.textContent = err.message;
        errorContainer.style.display = "block";
    }
});
