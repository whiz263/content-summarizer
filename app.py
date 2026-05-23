import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

# Force load_dotenv to look in the current file's directory (just like last time)
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

# Enable CORS so our local HTML file can send requests to this API
CORS(app)

# Initialize the Gemini Client. 
# It will automatically find the GEMINI_API_KEY in your environment variables.
client = genai.Client()

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    
    # Validation: Make sure they actually sent some text
    if not data or not data.get('text'):
        return jsonify({"error": "No text provided. Please submit text to summarize."}), 400
        
    text_to_summarize = data['text']
    
    # This is the prompt instruction we are sending to the AI
    prompt = f"Please provide a concise, well-structured summary of the following text using bullet points for key takeaways:\n\n{text_to_summarize}"
    
    try:
        # Call the Gemini 2.5 Flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Send the generated text back to the frontend
        return jsonify({"summary": response.text}), 200
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return jsonify({"error": "Failed to generate summary from AI."}), 500

if __name__ == '__main__':
    # Running on port 5002 just in case your finance tracker is still sleeping on 5001!
    app.run(debug=True, port=5002)