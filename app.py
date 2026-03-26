from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# database connection
def get_db():
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row
    return conn

# test route
@app.route('/')
def home():
    return "Server is running"

# get student
@app.route('/student/<int:id>')
def get_student(id):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM student WHERE stId=?",
        (id,)
    ).fetchone()
    return dict(student)

# mark attendance
@app.route('/mark', methods=['POST'])
def mark():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO attendence VALUES (?, ?, ?, ?)",
        (data['stId'], data['lecId'], data['time'], data['status'])
    )
    conn.commit()
    return {"message": "success"}

if __name__ == '__main__':
    app.run(debug=True)