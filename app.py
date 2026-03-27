from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# database connection
def get_db():
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row
    return conn

# test route
from flask import render_template

@app.route('/')
def home():
    return render_template("index.html")

# get student
@app.route('/student/<int:id>')
def get_student(id):
    conn = get_db()

    student = conn.execute(
        "SELECT * FROM student WHERE stId=?",
        (id,)
    ).fetchone()

    attendance = conn.execute(
        "SELECT * FROM attendence WHERE stId=? ORDER BY attendedTime DESC LIMIT 1",
        (id,)
    ).fetchone()

    if student is None:
        return {"error": "not found"}, 404

    result = dict(student)

    if attendance:
        result["status"] = attendance["status"]
        result["time"] = attendance["attendedTime"]
    else:
        result["status"] = "absent"
        result["time"] = ""

    return result

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

# print attendance report
@app.route('/report/<int:id>')
def report(id):
    conn = get_db()

    student = conn.execute(
        "SELECT * FROM student WHERE stId=?",
        (id,)
    ).fetchone()

    records = conn.execute(
        "SELECT * FROM attendence WHERE stId=?",
        (id,)
    ).fetchall()

    return render_template("report.html", student=student, records=records)


if __name__ == '__main__':
    app.run(debug=True)