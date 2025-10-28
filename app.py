from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)
appointments = []

DOCTORS = {
    "Smith": "Dr. Smith (Cardiologist)",
    "John": "Dr. John (Dermatologist)",
    "Sara": "Dr. Sara (Pediatrician)",
    "Ali": "Dr. Ali (Neurologist)"
}

def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediBook | Doctor Appointments</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #e0f7fa, #f5f5f5);
            color: #2c3e50;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            padding: 40px 20px;
            animation: fadeInDown 0.8s ease;
        }
        h1 {
            font-size: 2.8rem;
            color: #1a237e;
            margin-bottom: 15px;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #546e7a;
            margin-bottom: 30px;
        }
        .btn {
            display: inline-block;
            background: #1e88e5;
            color: white;
            padding: 14px 32px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
        }
        .btn:hover {
            background: #1565c0;
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(30, 136, 229, 0.4);
        }
        .features {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 25px;
            margin: 30px 0;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            width: 220px;
            text-align: center;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 20px rgba(0,0,0,0.15);
        }
        .card i {
            font-size: 2.2rem;
            color: #1e88e5;
            margin-bottom: 15px;
        }
        footer {
            text-align: center;
            padding: 30px;
            color: #78909c;
            margin-top: 20px;
        }

        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .animate {
            animation: slideInUp 0.6s ease forwards;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>MediBook</h1>
            <p class="subtitle">Book appointments with trusted doctors in minutes</p>
            <a href="/book" class="btn">Book Appointment</a>
        </header>

        <div class="features">
            <div class="card animate" style="animation-delay: 0.1s">
                <div>🩺</div>
                <h3>Top Doctors</h3>
                <p>Board-certified specialists</p>
            </div>
            <div class="card animate" style="animation-delay: 0.2s">
                <div>⏱️</div>
                <h3>Quick Booking</h3>
                <p>Under 2 minutes</p>
            </div>
            <div class="card animate" style="animation-delay: 0.3s">
                <div>🔒</div>
                <h3>Secure</h3>
                <p>Private & confidential</p>
            </div>
        </div>

        <footer>
            &copy; 2025 MediBook. All rights reserved.
        </footer>
    </div>
</body>
</html>
    ''')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        doctor_key = data.get('doctor', '').strip()
        date_str = data.get('date', '').strip()

        # Validation
        if not name or not email or not is_valid_email(email) or doctor_key not in DOCTORS or not date_str:
            return jsonify({"success": False, "message": "Please fill all fields correctly."}), 400

        try:
            appt_date = datetime.strptime(date_str, "%Y-%m-%d")
            if appt_date.date() < datetime.today().date():
                return jsonify({"success": False, "message": "Date must be today or in the future."}), 400
        except:
            return jsonify({"success": False, "message": "Invalid date."}), 400

        appointments.append({
            "name": name,
            "doctor": DOCTORS[doctor_key],
            "date": date_str
        })

        return jsonify({
            "success": True,
            "message": f"✅ Appointment confirmed! Dear {name}, you're booked with {DOCTORS[doctor_key]} on {date_str}."
        })

    min_date = datetime.today().strftime('%Y-%m-%d')
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Appointment | MediBook</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }
        body {
            background: linear-gradient(to right, #e3f2fd, #bbdefb);
            color: #0d47a1;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            margin: 30px auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            animation: fadeIn 0.7s ease;
        }
        header {
            background: #1976d2;
            color: white;
            padding: 25px;
            text-align: center;
        }
        .form-box {
            padding: 30px;
        }
        h2 {
            text-align: center;
            margin-bottom: 25px;
            color: #0d47a1;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }
        input, select {
            width: 100%;
            padding: 14px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            transition: border 0.3s, box-shadow 0.3s;
        }
        input:focus, select:focus {
            border-color: #1976d2;
            outline: none;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2);
        }
        .btn {
            width: 100%;
            background: #1976d2;
            color: white;
            border: none;
            padding: 15px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s;
        }
        .btn:hover {
            background: #1565c0;
            transform: scale(1.02);
        }
        .btn:disabled {
            background: #90caf9;
            cursor: not-allowed;
            transform: none;
        }
        .alert {
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-weight: 600;
            display: none;
        }
        .alert-success {
            background: #e8f5e9;
            color: #2e7d32;
            display: none;
        }
        .alert-error {
            background: #ffebee;
            color: #c62828;
            display: none;
        }

        /* Transitions */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.6s ease forwards;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📅 Book Appointment</h1>
        </header>
        <div class="form-box">
            <form id="bookingForm">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="doctor">Doctor</label>
                    <select id="doctor" name="doctor" required>
                        <option value="">-- Select --</option>
                        <option value="Smith">Dr. Smith (Cardiologist)</option>
                        <option value="John">Dr. John (Dermatologist)</option>
                        <option value="Sara">Dr. Sara (Pediatrician)</option>
                        <option value="Ali">Dr. Ali (Neurologist)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="date">Date</label>
                    <input type="date" id="date" name="date" min="{{ min_date }}" required>
                </div>
                <button type="submit" class="btn" id="submitBtn">Confirm Booking</button>
            </form>
            <div class="alert alert-success" id="successAlert"></div>
            <div class="alert alert-error" id="errorAlert"></div>
        </div>
    </div>

    <script>
        document.getElementById('bookingForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            // Reset alerts
            document.getElementById('successAlert').style.display = 'none';
            document.getElementById('errorAlert').style.display = 'none';
            const btn = document.getElementById('submitBtn');
            btn.disabled = true;
            btn.textContent = 'Booking...';

            try {
                const res = await fetch('/book', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                if (result.success) {
                    document.getElementById('successAlert').textContent = result.message;
                    document.getElementById('successAlert').style.display = 'block';
                    e.target.reset();
                    document.getElementById('doctor').value = '';
                } else {
                    document.getElementById('errorAlert').textContent = result.message;
                    document.getElementById('errorAlert').style.display = 'block';
                }
            } catch (err) {
                document.getElementById('errorAlert').textContent = 'Booking failed. Try again.';
                document.getElementById('errorAlert').style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.textContent = 'Confirm Booking';
            }
        });

        // Set min date to today
        document.getElementById('date').min = new Date().toISOString().split('T')[0];
    </script>
</body>
</html>
    ''', min_date=min_date)

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
