from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("prompts.csv")
prompts_data = df.to_dict('records')

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
        if query in prompt['act'].lower() or query in prompt['prompt'].lower()
    ]
    return jsonify(filtered_prompts)

@app.route('/random')
def random_prompt():
    return jsonify(random.choice(prompts_data))

@app.route('/stats')
def stats():
    total_prompts = len(prompts_data)
    avg_length = sum(len(str(p['prompt'])) for p in prompts_data) / total_prompts
    return jsonify({
        'total_prompts': total_prompts,
        'average_length': round(avg_length, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
