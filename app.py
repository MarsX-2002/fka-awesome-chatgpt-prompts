from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import requests

app = Flask(__name__)

# Create sample data if unable to load from GitHub
SAMPLE_PROMPTS = [
    {
        "act": "Linux Terminal",
        "prompt": "I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English, I will do so by putting text inside curly brackets {like this}."
    },
    {
        "act": "English Translator",
        "prompt": "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations."
    },
    {
        "act": "Position Interviewer",
        "prompt": "I want you to act as an interviewer. I will be the candidate and you will ask me the interview questions for the position position. I want you to only reply as the interviewer. Do not write all the conservation at once. I want you to only do the interview with me. Ask me the questions and wait for my answers. Do not write explanations. Ask me the questions one by one like an interviewer does and wait for my answers."
    }
]

def load_prompts():
    try:
        # First try to load from the repository
        response = requests.get("https://raw.githubusercontent.com/MarsX-2002/fka-awesome-chatgpt-prompts/main/prompts.csv")
        if response.status_code == 200:
            # Save the content to a temporary file
            with open("temp_prompts.csv", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            # Read the CSV file
            df = pd.read_csv("temp_prompts.csv")
            return df.to_dict('records')
        else:
            print("Failed to load data from GitHub, using sample data")
            return SAMPLE_PROMPTS
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return SAMPLE_PROMPTS

prompts_data = load_prompts()

@app.route('/')
def index():
    return render_template('index.html', prompts=prompts_data[:12])

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify(prompts_data[:12])
    
    filtered_prompts = [
        prompt for prompt in prompts_data
        if query in str(prompt.get('act', '')).lower() or query in str(prompt.get('prompt', '')).lower()
    ]
    return jsonify(filtered_prompts)

@app.route('/random')
def random_prompt():
    if prompts_data:
        return jsonify(random.choice(prompts_data))
    return jsonify({"act": "Sample Prompt", "prompt": "No prompts available at the moment."})

@app.route('/stats')
def stats():
    if not prompts_data:
        return jsonify({'total_prompts': 0, 'average_length': 0})
    
    total_prompts = len(prompts_data)
    avg_length = sum(len(str(p.get('prompt', ''))) for p in prompts_data) / total_prompts
    return jsonify({
        'total_prompts': total_prompts,
        'average_length': round(avg_length, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
