from flask import Flask, render_template_string, request, redirect, url_for
import json

app = Flask(__name__)
DATA_FILE = "data_store.json"


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


CANDIDATE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Candidate Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .card { background: #fff; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1, h2 { color: #2c3e50; }
        ul { list-style: none; padding: 0; }
        li { padding: 5px 0; }
    </style>
</head>
<body>
    <h1>Candidate Dashboard</h1>
    {% for name, info in data.items() %}
        <div class="card">
            <h2>{{ name }}</h2>
            <ul>
                <li><strong>Daily Quiz Status:</strong> {{ info.daily_quiz }}</li>
                <li><strong>Assignment Submission:</strong> {{ info.assignment }}</li>
                <li><strong>Certification Completion:</strong> {{ info.certification }}</li>
            </ul>
        </div>
    {% endfor %}
    <a href="/">Back to Home</a>
</body>
</html>
'''


ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Console</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .card { background: #fff; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #eee; }
    </style>
</head>
<body>
    <h1>Administrator Console</h1>

    <div class="card">
        <form method="get">
            <label for="skill">Skill:</label>
            <select name="skill">
                <option value="">All</option>
                <option value="Python">Python</option>
                <option value="Java">Java</option>
            </select>
            <label for="department">Department:</label>
            <select name="department">
                <option value="">All</option>
                <option value="Data Engineering">Data Engineering</option>
                <option value="Web Dev">Web Dev</option>
            </select>
            <button type="submit">Filter</button>
        </form>
    </div>

    <div class="card">
        <h2>Fresher Progress Report</h2>
        <table>
            <tr>
                <th>Name</th><th>Skill</th><th>Department</th><th>Quiz</th><th>Assignment</th><th>Certification</th>
            </tr>
            {% for name, info in data.items() %}
                <tr>
                    <td>{{ name }}</td>
                    <td>{{ info.skill }}</td>
                    <td>{{ info.department }}</td>
                    <td>{{ info.daily_quiz }}</td>
                    <td>{{ info.assignment }}</td>
                    <td>{{ info.certification }}</td>
                </tr>
            {% endfor %}
        </table>
    </div>
    <a href="/">Back to Home</a>
</body>
</html>
'''


HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Training Management Home</title>
    <style>
        body { font-family: Arial, sans-serif; background: #ecf0f1; padding: 20px; }
        h1 { color: #2c3e50; }
        a { display: inline-block; padding: 10px 20px; margin: 10px; background: #3498db; color: #fff; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Welcome to Training Management System</h1>
    <a href="/candidate">Candidate Dashboard</a>
    <a href="/admin">Administrator Console</a>
</body>
</html>
'''


@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE)


@app.route("/candidate")
def candidate():
    data = load_data()
    return render_template_string(CANDIDATE_TEMPLATE, data=data)


@app.route("/admin")
def admin():
    data = load_data()
    skill_filter = request.args.get("skill")
    dept_filter = request.args.get("department")

    if skill_filter:
        data = {k: v for k, v in data.items() if v.get("skill") == skill_filter}
    if dept_filter:
        data = {k: v for k, v in data.items() if v.get("department") == dept_filter}

    return render_template_string(ADMIN_TEMPLATE, data=data)


if __name__ == "__main__":
    app.run(debug=True)