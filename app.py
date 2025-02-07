from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

data = read_data('exercises.json')

@app.route('/')
def index():
    categories = set()
    primary_muscles = set()
    for exercise in data['exercises']:
        categories.add(exercise['category'])
        primary_muscles.update(exercise.get('primary_muscles', []))

    first_exercises = data['exercises'][:10]
    return render_template(
        'index.html',
        categories=categories,
        primary_muscles=primary_muscles,
        first_exercises=first_exercises
    )

@app.route('/filter', methods=['GET'])
def filter_exercises():
    category = request.args.get('category', '')
    muscle = request.args.get('muscle', '')
    equipment = request.args.get('equipment', '')

    filtered_exercises = [
        exercise for exercise in data['exercises']
        if (category == '' or exercise['category'] == category) and
           (muscle == '' or any(m in exercise.get('primary_muscles', []) for m in muscle.split(','))) and
           (equipment == '' or equipment in exercise.get('equipment', []))
    ]

    return jsonify(filtered_exercises)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))  # Render tự cung cấp biến môi trường PORT
    app.run(debug=True, host='0.0.0.0', port=port)

