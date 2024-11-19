from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import requests

app = Flask(__name__)

# Load the dataset from GitHub
DATASET_URL = "https://raw.githubusercontent.com/MarsX-2002/fka-awesome-chatgpt-prompts/main/prompts.csv"

def load_prompts():
    try:
        df = pd.read_csv(DATASET_URL)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return []

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
        if query in str(prompt['act']).lower() or query in str(prompt['prompt']).lower()
    ]
    return jsonify(filtered_prompts)

@app.route('/random')
def random_prompt():
    return jsonify(random.choice(prompts_data) if prompts_data else {})

@app.route('/stats')
def stats():
    if not prompts_data:
        return jsonify({'total_prompts': 0, 'average_length': 0})
    
    total_prompts = len(prompts_data)
    avg_length = sum(len(str(p['prompt'])) for p in prompts_data) / total_prompts
    return jsonify({
        'total_prompts': total_prompts,
        'average_length': round(avg_length, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
