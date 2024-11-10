import json

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_html(data):
    categories = set()
    primary_muscles = set()
    
    for exercise in data['exercises']:
        categories.add(exercise['category'])
        primary_muscles.update(exercise.get('primary_muscles', []))
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exercise Data</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }
            .exercise-container {
                display: flex;
                flex-wrap: wrap;
                gap: 2rem;
            }
            .exercise {
                flex: 1 1 calc(20% - 2rem);
                box-sizing: border-box;
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .exercise:hover {
                transform: scale(1.05);
            }
            .exercise h2 {
                margin-top: 0;
            }
            .exercise p {
                margin: 5px 0;
            }
            .exercise video {
                display: block;
                margin: 10px 0;
            }
            .exercise-details {
                display: none;
            }
            .filter {
                margin-bottom: 20px;
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgb(0,0,0);
                background-color: rgba(0,0,0,0.4);
                padding-top: 60px;
            }
            .modal-content {
                background-color: #fefefe;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
                border-radius: 10px;
            }
            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }
            .close:hover,
            .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
        <script>
            function toggleDetails(id) {
                var modal = document.getElementById('modal-' + id);
                modal.style.display = "block";
            }

            function closeModal(id) {
                var modal = document.getElementById('modal-' + id);
                modal.style.display = "none";
            }

            function filterExercises() {
                var categoryFilter = document.getElementById('categoryFilter').value;
                var muscleFilter = document.getElementById('muscleFilter').value;

                var exercises = document.getElementsByClassName('exercise');
                for (var i = 0; i < exercises.length; i++) {
                    var exercise = exercises[i];
                    var category = exercise.getAttribute('data-category');
                    var primaryMuscles = exercise.getAttribute('data-primary-muscles').split(',');

                    if ((categoryFilter === "" || category === categoryFilter) &&
                        (muscleFilter === "" || primaryMuscles.includes(muscleFilter))) {
                        exercise.style.display = "block";
                    } else {
                        exercise.style.display = "none";
                    }
                }
            }

            function adjustCardSize() {
                var width = window.innerWidth;

                var exercises = document.getElementsByClassName('exercise');
                
                if (width > 1200) {
                    for (var i = 0; i < exercises.length; i++) {
                        exercises[i].style.flex = "1 1 calc(20% - 2rem)";
                    }
                } else if (width > 900) {
                    for (var i = 0; i < exercises.length; i++) {
                        exercises[i].style.flex = "1 1 calc(25% - 2rem)";
                    }
                } else if (width > 600) {
                    for (var i = 0; i < exercises.length; i++) {
                        exercises[i].style.flex = "1 1 calc(33.333% - 2rem)";
                    }
                } else if (width > 400) {
                    for (var i = 0; i < exercises.length; i++) {
                        exercises[i].style.flex = "1 1 calc(50% - 2rem)";
                    }
                } else {
                    for (var i = 0; i < exercises.length; i++) {
                        exercises[i].style.flex = "1 1 calc(100% - 2rem)";
                    }
                }
            }

            window.onresize = adjustCardSize;

            window.onload = function() {
              adjustCardSize();
              filterExercises();
            };
        </script>
    </head>
    <body>
        <h1>Exercise Data</h1>
        <div class="filter">
            <label for="categoryFilter">Category:</label>
            <select id="categoryFilter" onchange="filterExercises()">
                <option value="">All</option>
    """

    for category in categories:
        html_content += f'<option value="{category}">{category}</option>'

    html_content += """
            </select>

            <label for="muscleFilter">Primary Muscle:</label>
            <select id="muscleFilter" onchange="filterExercises()">
                <option value="">All</option>
    """

    for muscle in primary_muscles:
        html_content += f'<option value="{muscle}">{muscle}</option>'

    html_content += """
            </select>
        </div>
        <div class="exercise-container">
    """

    for i, exercise in enumerate(data['exercises']):
        primary_muscles_str = ','.join(exercise.get('primary_muscles', []))
        html_content += f"""
        <div class="exercise" data-category="{exercise['category']}" data-primary-muscles="{primary_muscles_str}" onclick="toggleDetails('{i}')">
            <h2>{exercise['name']}</h2>
            <p><strong>Category:</strong> {exercise['category']}</p>
            <p><strong>Primary Muscles:</strong> {', '.join(exercise.get('primary_muscles', []))}</p>
        </div>

        <div id="modal-{i}" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('{i}')">×</span>
                <h2>{exercise['name']}</h2>
                <p><strong>Category:</strong> {exercise['category']}</p>
                <p><strong>Primary Muscles:</strong> {', '.join(exercise.get('primary_muscles', []))}</p>
                <p><strong>Description:</strong> {exercise.get('description', 'N/A')}</p>
                <p><strong>Equipment:</strong> {', '.join(exercise.get('equipment', []))}</p>
                <p><strong>Instructions:</strong> {' '.join(exercise.get('instructions', []))}</p>
                <p><strong>Secondary Muscles:</strong> {', '.join(exercise.get('secondary_muscles', []))}</p>
                {f'<video controls><source src="{exercise["video"]}" type="video/mp4">Your browser does not support the video tag.</video>' if 'video' in exercise else ''}
            </div>
        </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """
    
    return html_content

def write_html(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == '__main__':
    data = read_data('minified-exercises.json')
    html_content = generate_html(data)
    write_html('exercises.html', html_content)
