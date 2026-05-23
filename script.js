document.getElementById('summarizeBtn').addEventListener('click', async () => {
    const textInput = document.getElementById('textInput').value.trim();
    const summarizeBtn = document.getElementById('summarizeBtn');
    const resultBox = document.getElementById('resultBox');
    const summaryDisplay = document.getElementById('summaryDisplay');

    if (!textInput) {
        alert("Please enter some text first!");
        return;
    }


    summarizeBtn.disabled = true;
    summarizeBtn.innerText = "Analyzing text...";
    resultBox.style.display = "none";

    try {
        
        const response = await fetch('https://content-summarizer-ybyy.onrender.com/api/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();

        if (response.ok) {
            
            summaryDisplay.innerText = data.summary;
            resultBox.style.display = "block";
        } else {
            alert("Error: " + (data.error || "Something went wrong"));
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        alert("Could not connect to the backend server.");
    } finally {
        
        summarizeBtn.disabled = false;
        summarizeBtn.innerText = "Generate Summary";
    }
});