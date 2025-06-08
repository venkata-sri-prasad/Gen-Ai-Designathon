from flask import Flask, render_template_string, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data_store.json"


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

CANDIDATE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Candidate Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background: #f0f4f8;
            margin: 0;
            padding: 20px 40px;
            color: #34495e;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 40px;
        }
        .dashboard {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            padding: 25px;
            flex: 1 1 280px;
            max-width: 320px;
            transition: transform 0.2s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        }
        h2 {
            margin-top: 0;
            color: #1abc9c;
            border-bottom: 2px solid #1abc9c;
            padding-bottom: 8px;
        }
        ul {
            list-style: none;
            padding-left: 0;
        }
        li {
            margin-bottom: 10px;
            font-size: 16px;
        }
        .status {
            font-weight: 600;
            color: #2980b9;
        }
        a {
            display: block;
            width: 150px;
            margin: 40px auto 0;
            text-align: center;
            text-decoration: none;
            padding: 12px 0;
            background: #1abc9c;
            color: white;
            border-radius: 25px;
            font-weight: 700;
            box-shadow: 0 6px 15px rgba(26,188,156,0.5);
            transition: background 0.3s ease;
        }
        a:hover {
            background: #16a085;
        }
    </style>
</head>
<body>
    <h1>Candidate Dashboard</h1>
    <div class="dashboard">
        {% for name, info in data.items() %}
        <div class="card">
            <h2>{{ name }}</h2>
            <ul>
                <li>Daily Quiz Status: <span class="status">{{ info.daily_quiz }}</span></li>
                <li>Assignment Submission: <span class="status">{{ info.assignment }}</span></li>
                <li>Certification Completion: <span class="status">{{ info.certification }}</span></li>
                <li><small>Last Updated: {{ info.last_updated if info.last_updated else 'N/A' }}</small></li>
            </ul>
        </div>
        {% endfor %}
    </div>
    <a href="/">Back to Home</a>
</body>
</html>
'''

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Admin Console</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background: #f0f4f8;
            margin: 0;
            padding: 30px 50px;
            color: #34495e;
        }
        h1 {
            text-align: center;
            margin-bottom: 40px;
            color: #2c3e50;
        }
        form {
            max-width: 600px;
            margin: 0 auto 30px;
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        select, button {
            padding: 10px 15px;
            font-size: 16px;
            border-radius: 6px;
            border: 1px solid #bdc3c7;
            outline: none;
            transition: border-color 0.3s ease;
        }
        select:focus, button:hover {
            border-color: #1abc9c;
            cursor: pointer;
        }
        button {
            background: #1abc9c;
            color: white;
            border: none;
            font-weight: 700;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        th, td {
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
            font-size: 15px;
        }
        th {
            background-color: #1abc9c;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
        }
        tr:hover {
            background-color: #ecf8f7;
        }
        a {
            display: block;
            width: 150px;
            margin: 40px auto 0;
            text-align: center;
            text-decoration: none;
            padding: 12px 0;
            background: #1abc9c;
            color: white;
            border-radius: 25px;
            font-weight: 700;
            box-shadow: 0 6px 15px rgba(26,188,156,0.5);
            transition: background 0.3s ease;
        }
        a:hover {
            background: #16a085;
        }
    </style>
</head>
<body>
    <h1>Administrator Console</h1>
    <form method="get">
        <select name="skill" aria-label="Filter by skill">
            <option value="">All Skills</option>
            <option value="Python">Python</option>
            <option value="Java">Java</option>
        </select>
        <select name="department" aria-label="Filter by department">
            <option value="">All Departments</option>
            <option value="Data Engineering">Data Engineering</option>
            <option value="Web Dev">Web Dev</option>
        </select>
        <button type="submit">Filter</button>
    </form>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Skill</th>
                <th>Department</th>
                <th>Daily Quiz</th>
                <th>Assignment</th>
                <th>Certification</th>
                <th>Last Updated</th>
            </tr>
        </thead>
        <tbody>
            {% for name, info in data.items() %}
            <tr>
                <td>{{ name }}</td>
                <td>{{ info.skill }}</td>
                <td>{{ info.department }}</td>
                <td>{{ info.daily_quiz }}</td>
                <td>{{ info.assignment }}</td>
                <td>{{ info.certification }}</td>
                <td>{{ info.last_updated if info.last_updated else 'N/A' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
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
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #e0f7fa, #f9fbe7);
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 40px 60px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
            border: 1px solid #d0d0d0;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
        }
        a {
            display: inline-block;
            margin: 15px 20px;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            background: #3498db;
            border: none;
            border-radius: 10px;
            text-decoration: none;
            transition: background 0.3s ease, transform 0.2s ease;
        }
        a:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        .footer {
            margin-top: 30px;
            font-size: 13px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Training Management System</h1>
        <a href="/candidate">Candidate Dashboard</a>
        <a href="/admin">Administrator Console</a>
        <div class="footer">Designed with ❤️ for onboarding excellence</div>
    </div>
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


@app.route("/update/<name>", methods=["POST"])
def update_status(name):
    data = load_data()
    if name in data:
        data[name]["daily_quiz"] = request.form["daily_quiz"]
        data[name]["assignment"] = request.form["assignment"]
        data[name]["certification"] = request.form["certification"]
        data[name]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_data(data)
    return redirect(url_for('candidate'))


if __name__ == "__main__":
    app.run(debug=True)