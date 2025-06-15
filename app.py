from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = "dummy_secret"
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
        session['user'] = request.form['username']
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
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

if __name__ == '__main__':
    app.run(debug=True)
