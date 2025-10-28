from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <html>
            <head>
                <title>Doctor Appointment Booking</title>
                <style>
                    body {font-family: Arial; background: #f2f2f2; text-align: center; margin-top: 50px;}
                    h1 {color: #333;}
                    a {text-decoration: none; color: white; background: #007BFF; padding: 10px 20px; border-radius: 5px;}
                    a:hover {background: #0056b3;}
                </style>
            </head>
            <body>
                <h1>Welcome to Doctor Appointment Booking</h1>
                <p>Book your appointment with a doctor easily.</p>
                <a href="/book">Book Appointment</a>
            </body>
        </html>
    ''')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        doctor = request.form['doctor']
        date = request.form['date']
        return render_template_string('''
            <html>
                <head><title>Booking Confirmed</title></head>
                <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                    <h2>Appointment Confirmed!</h2>
                    <p>Thank you, {{name}}. Your appointment with Dr. {{doctor}} on {{date}} has been booked.</p>
                    <a href="/">Go Back Home</a>
                </body>
            </html>
        ''', name=name, doctor=doctor, date=date)

    return render_template_string('''
        <html>
            <head>
                <title>Book Appointment</title>
                <style>
                    body {font-family: Arial; background: #f9f9f9; text-align: center; margin-top: 50px;}
                    form {display: inline-block; text-align: left; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px #ccc;}
                    input, select {width: 100%; margin: 8px 0; padding: 8px;}
                    button {background: #28a745; color: white; padding: 10px; border: none; border-radius: 5px;}
                    button:hover {background: #218838;}
                </style>
            </head>
            <body>
                <h2>Book Your Appointment</h2>
                <form method="POST">
                    <label>Name:</label><br>
                    <input type="text" name="name" required><br>
                    <label>Email:</label><br>
                    <input type="email" name="email" required><br>
                    <label>Doctor:</label><br>
                    <select name="doctor" required>
                        <option value="">Select Doctor</option>
                        <option value="Smith">Dr. Smith (Cardiologist)</option>
                        <option value="John">Dr. John (Dermatologist)</option>
                        <option value="Sara">Dr. Sara (Pediatrician)</option>
                    </select><br>
                    <label>Date:</label><br>
                    <input type="date" name="date" required><br>
                    <button type="submit">Book Appointment</button>
                </form>
            </body>
        </html>
    ''')

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
