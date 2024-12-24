import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to initialize the database and create the students table
def initialize_database():
    conn = sqlite3.connect('database/student_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            prn TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            contact TEXT,
            course TEXT,
            dob DATE,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

# Example route for the home page
@app.route('/')
def index():
    conn = sqlite3.connect('database/student_management.db')
    conn.row_factory = sqlite3.Row
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)


def get_db_connection():
    try:
        conn = sqlite3.connect('database/student_management.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print("An error occurred while connecting to the database:", e)
        return None



@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['student_name']
        prn = request.form['prn']
        email = request.form['email']
        contact = request.form['contact']
        course = request.form['course']
        dob = request.form['dob']

        # Calculate age
        age = datetime.now().year - datetime.strptime(dob, '%Y-%m-%d').year

        try:
            conn = get_db_connection()
            if conn:
                conn.execute('INSERT INTO students (student_name, prn, email, contact, course, dob, age) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (name, prn, email, contact, course, dob, age))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        except sqlite3.Error as e:
            print("An error occurred during student insertion:", e)
    return render_template('add_student.html')



@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    try:
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
        # Perform update logic here if POST
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred while updating student:", e)
    return render_template('edit_student.html', student=student)


@app.route('/update_student/<int:id>', methods=['POST'])
def update_student(id):
    student_name = request.form['student_name']
    prn = request.form['prn']
    email = request.form['email']
    contact = request.form['contact']
    course = request.form['course']
    dob = request.form['dob']

    # Calculate age from DOB if needed
    from datetime import datetime
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    age = datetime.now().year - dob_date.year

    conn = sqlite3.connect('database/student_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE students
        SET student_name = ?, prn = ?, email = ?, contact = ?, course = ?, dob = ?, age = ?
        WHERE id = ?
    ''', (student_name, prn, email, contact, course, dob, age, id))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))




@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred while deleting student:", e)
    return redirect(url_for('index'))



@app.route('/view_students/<course>')
def view_students(course):
    try:
        conn = get_db_connection()
        students = conn.execute('SELECT * FROM students WHERE course = ?', (course,)).fetchall()
        conn.close()
        return render_template('view_students.html', students=students, course=course)
    except sqlite3.Error as e:
        print("An error occurred while fetching students by course:", e)
        return redirect(url_for('index'))



@app.route('/filter')
def filter_students():
    course = request.args.get('course')
    conn = get_db_connection()
    if course == 'all':
        students = conn.execute('SELECT * FROM students').fetchall()
    else:
        students = conn.execute('SELECT * FROM students WHERE course = ?', (course,)).fetchall()
    conn.close()
    return render_template('index.html', students=students)



if __name__ == "__main__":
    app.run(debug=True)






