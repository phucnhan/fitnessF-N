from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

data = read_data('minified-exercises.json')

@app.route('/')
def index():
    categories = set()
    primary_muscles = set()
    
    for exercise in data['exercises']:
        categories.add(exercise['category'])
        primary_muscles.update(exercise.get('primary_muscles', []))
    
    return render_template('index.html', exercises=data['exercises'], categories=categories, primary_muscles=primary_muscles)

@app.route('/exercise/<int:exercise_id>')
def exercise(exercise_id):
    exercise = data['exercises'][exercise_id]
    return render_template('exercise.html', exercise=exercise)

if __name__ == '__main__':
    app.run(debug=True)
