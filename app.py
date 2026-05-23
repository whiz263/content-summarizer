import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv


script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": " https://whiz263.github.io/content-summarizer/"}})


client = genai.Client()

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "message": "Content Summarizer API is running!"}), 200

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    
    
    if not data or not data.get('text'):
        return jsonify({"error": "No text provided. Please submit text to summarize."}), 400
        
    text_to_summarize = data['text']
    
    
    prompt = f"Please provide a concise, well-structured summary of the following text using bullet points for key takeaways:\n\n{text_to_summarize}"
    
    try:
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
       
        return jsonify({"summary": response.text}), 200
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return jsonify({"error": "Failed to generate summary from AI."}), 500

if __name__ == '__main__':
    
    app.run(debug=True, port=5002)