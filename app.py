from reportlab.pdfgen import canvas
from flask import send_file
from flask import Flask, render_template, request,redirect, flash, session
import sqlite3
app = Flask(__name__)
app.secret_key = "caresphere123"




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name, age, gender, phone, email, password) VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, gender, phone, email, password)
        )

        conn.commit()
        conn.close()
        flash("✅ Registration successful. Please login.")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session['email'] = email
            session['user'] = user[1]
            print("LOGIN:", session['email'])
            return redirect('/dashboard')
        else:
            flash("❌ Invalid Email or Password")
            return redirect('/login')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
    
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM medicines WHERE user_email=?", (session['email'],))
    medicine_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM health_records WHERE user_email=?", (session['email'],))
    health_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM emergency_contacts WHERE user_email=?", (session['email'],))
    emergency_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedbacks WHERE user_email=?", (session['email'],))
    feedback_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        user=session['user'],
        medicine_count=medicine_count,
        health_count=health_count,
        emergency_count=emergency_count,
        feedback_count=feedback_count
    )

@app.route('/medicine', methods=['GET', 'POST'])
def medicine():
    print("MEDICINE PAGE:", session.get('email'))  # Debugging line
    if 'email' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        medicine_name = request.form['medicine_name']
        medicine_time = request.form['medicine_time']
        print("Current session email:", session['email'])  # Debugging line
        cursor.execute(
            "INSERT INTO medicines(medicine_name, medicine_time, user_email) VALUES (?, ?, ?)",
            (medicine_name, medicine_time, session['email'])
            
        )

        conn.commit()

    cursor.execute("SELECT * FROM medicines WHERE user_email=?", (session['email'],))
    medicines = cursor.fetchall()
    print("Records Found:", medicines)  # Debugging line

    conn.close()

    return render_template(
        'medicine.html',
        medicines=medicines
    )

    

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/health-records', methods=['GET', 'POST'])
def health_records():

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        patient_name = request.form['patient_name']
        weight = request.form['weight']
        height = request.form['height']
        blood_pressure = request.form['blood_pressure']
        sugar_level = request.form['sugar_level']

        cursor.execute(
            """
            INSERT INTO health_records
            (patient_name, weight, height, blood_pressure, sugar_level, user_email)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient_name, weight, height, blood_pressure, sugar_level, session['email'])
        )

        conn.commit()

    cursor.execute("SELECT * FROM health_records WHERE user_email=?", (session['email'],))
    records = cursor.fetchall()

    conn.close()

    return render_template(
        'health-records.html',
        records=records
    )

@app.route('/emergency', methods=['GET', 'POST'])
def emergency():

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        relation = request.form['relation']
        phone = request.form['phone']

        cursor.execute(
            """
            INSERT INTO emergency_contacts
            (name, relation, phone, user_email)
            VALUES (?, ?, ?, ?)
            """,
            (name, relation, phone, session['email'])
        )

        conn.commit()

    cursor.execute("SELECT * FROM emergency_contacts WHERE user_email=?", (session['email'],))
    contacts = cursor.fetchall()

    conn.close()

    return render_template(
        'emergency.html',
        contacts=contacts
    )

@app.route('/emotional')
def emotional():
    return render_template('emotional.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/family')
def family():
    return render_template('family.html')

@app.route('/carescore')
def carescore():
    return render_template('carescore.html')

@app.route('/healthpassport', methods=['GET', 'POST'])
def healthpassport():

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        blood_pressure = request.form['blood_pressure']
        sugar_level = request.form['sugar_level']
        emergency_contact = request.form['emergency_contact']

        cursor.execute(
            """
            INSERT INTO health_passport
            (name, age, blood_group, blood_pressure,
             sugar_level, emergency_contact, user_email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                age,
                blood_group,
                blood_pressure,
                sugar_level,
                emergency_contact,
                session['email']
            )
        )

        conn.commit()

    cursor.execute("SELECT * FROM health_passport WHERE user_email=?", (session['email'],))
    passports = cursor.fetchall()

    conn.close()

    return render_template(
        'healthpassport.html',
        passports=passports
    )

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        feedback_text = request.form['feedback']
        rating = request.form['rating']

        cursor.execute(
            """
            INSERT INTO feedbacks
            (name, feedback, rating, user_email)
            VALUES (?, ?, ?, ?)
            """,
            (name, feedback_text, rating, session['email'])
        )

        conn.commit()

    cursor.execute("SELECT * FROM feedbacks WHERE user_email=?", (session['email'],))
    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        'feedback.html',
        feedbacks=feedbacks
    )
@app.route('/download-passport/<int:id>')
def download_passport(id):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM health_passport WHERE id=?",
        (id,)
    )

    passport = cursor.fetchone()
    conn.close()

    pdf_file = f"passport_{id}.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 800, "Digital Health Passport")

    c.setFont("Helvetica", 12)

    c.drawString(100, 740, f"Name : {passport[1]}")
    c.drawString(100, 710, f"Age : {passport[2]}")
    c.drawString(100, 680, f"Blood Group : {passport[3]}")
    c.drawString(100, 650, f"Blood Pressure : {passport[4]}")
    c.drawString(100, 620, f"Sugar Level : {passport[5]}")
    c.drawString(100, 590, f"Emergency Contact : {passport[6]}")

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )
    
@app.route('/logout')
def logout():
    
    session.clear()

    flash("👋 Logged Out Successfully")

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)