from datetime import timedelta
from flask import Flask, render_template, request, redirect, session, g
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3
import pyotp


app = Flask(__name__)
app.secret_key = "dummy_secret"

bcrypt = Bcrypt(app)

app.permanent_session_lifetime = timedelta(minutes=15)

@app.before_request
def make_session_permanent():
    session.permanent = True


DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp_code = request.form['otp']

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user:
            # Print debug info in terminal
            print("User found:", user)
            print("Entered password:", password)
            print("Stored hash:", user[2])

            if bcrypt.check_password_hash(user[2], password):
                print("✅ Password is correct")
                if pyotp.TOTP(user[3]).verify(otp_code):
                    print("✅ OTP is correct")
                    session['user'] = username
                    return redirect('/dashboard')
                else:
                    print("❌ Wrong OTP")
                    return "Invalid 2FA Code"
            else:
                print("❌ Wrong Password")
        else:
            print("❌ User not found")
        return "Invalid credentials"
    return render_template('login.html')




@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])

@app.route('/transfer', methods=['GET', 'POST'])

def transfer():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        sender = session.get('user')
        receiver = request.form['receiver']
        amount = request.form['amount']

        db = get_db()
        db.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)", (sender, receiver, amount))
        db.commit()
        return redirect('/history')
    return render_template('transfer.html')

@app.route('/history')
def history():
    db = get_db()
    cursor = db.execute("SELECT * FROM transactions WHERE sender = ?", (session.get('user'),))
    transactions = cursor.fetchall()
    return render_template('history.html', transactions=transactions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        otp_secret = pyotp.random_base32()  # For 2FA
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password, otp_secret) VALUES (?, ?, ?)",
                       (username, password, otp_secret))
            db.commit()
            return f"Account created! Save this 2FA code: {otp_secret} and scan in Google Authenticator."
        except sqlite3.IntegrityError:
            return "Username already exists!"
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
