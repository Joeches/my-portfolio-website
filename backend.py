from flask import Flask, render_template, request, jsonify, abort
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DATABASE = 'portfolio.db'

# Sample initial data for demonstration purposes
projects_data = [
    {
        "id": 1,
        "title": "Project 1",
        "description": "Description of Project 1",
        "github_link": "https://github.com/yourusername/project1",
    },
    {
        "id": 2,
        "title": "Project 2",
        "description": "Description of Project 2",
        "github_link": "https://github.com/yourusername/project2",
    }
]

# Initialize the database and create the 'projects' table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            github_link TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert initial data into the 'projects' table
def insert_initial_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO projects (title, description, github_link)
        VALUES (?, ?, ?)
    ''', [(project['title'], project['description'], project['github_link']) for project in projects_data])
    conn.commit()
    conn.close()

# Get all projects from the database
def get_projects():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    conn.close()
    return projects

# Get a specific project by ID from the database
def get_project(project_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    conn.close()
    return project

# Create a new project in the database
def create_project(title, description, github_link):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (title, description, github_link) VALUES (?, ?, ?)', (title, description, github_link))
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return project_id

# Update an existing project in the database
def update_project(project_id, title, description, github_link):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE projects SET title = ?, description = ?, github_link = ? WHERE id = ?', (title, description, github_link, project_id))
    conn.commit()
    conn.close()

# Delete a project from the database
def delete_project(project_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()

# Initialize the database and insert initial data
init_db()
insert_initial_data()

# Route to serve the frontend HTML page
@app.route('/')
def index():
    return render_template('index.html')

# RESTful API endpoints for projects
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'GET':
        projects = get_projects()
        return jsonify(projects)
    elif request.method == 'POST':
        data = request.json
        title = data.get('title', '')
        description = data.get('description', '')
        github_link = data.get('github_link', '')
        project_id = create_project(title, description, github_link)
        return jsonify({"id": project_id}), 201

@app.route('/api/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_project(project_id):
    if request.method == 'GET':
        project = get_project(project_id)
        if project is None:
            abort(404)
        return jsonify(project)
    elif request.method == 'PUT':
        data = request.json
        title = data.get('title', '')
        description = data.get('description', '')
        github_link = data.get('github_link', '')
        update_project(project_id, title, description, github_link)
        return jsonify({"message": "Project updated successfully"})
    elif request.method == 'DELETE':
        delete_project(project_id)
        return jsonify({"message": "Project deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
