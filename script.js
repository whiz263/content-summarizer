document.getElementById('summarizeBtn').addEventListener('click', async () => {
    const textInput = document.getElementById('textInput').value.trim();
    const summarizeBtn = document.getElementById('summarizeBtn');
    const resultBox = document.getElementById('resultBox');
    const summaryDisplay = document.getElementById('summaryDisplay');

    if (!textInput) {
        alert("Please enter some text first!");
        return;
    }

    // UI Feedback: Disable button and show loading state
    summarizeBtn.disabled = true;
    summarizeBtn.innerText = "Analyzing text...";
    resultBox.style.display = "none";

    try {
        // Hit our Python Flask server running on port 5002
        const response = await fetch("https://content-summarizer-ybyy.onrender.com", { 
 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();

        if (response.ok) {
            // Display the clean summary text returned by the AI
            summaryDisplay.innerText = data.summary;
            resultBox.style.display = "block";
        } else {
            alert("Error: " + (data.error || "Something went wrong"));
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        alert("Could not connect to the backend server. Make sure app.py is running!");
    } finally {
        // Restore button state
        summarizeBtn.disabled = false;
        summarizeBtn.innerText = "Generate Summary";
    }
});