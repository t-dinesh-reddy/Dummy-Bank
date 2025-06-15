# 💳 Dummy Bank Website

A lightweight dummy online banking web application built with **Flask**, **Bootstrap**, and **SQLite**. Ideal for learning web development, cybersecurity testing, or practicing frameworks like ISO/IEC 27001.

---

## 🚀 Features

- 🔐 Login (dummy session-based)
- 🧾 View balance (mocked)
- 💸 Transfer funds (dummy entries)
- 📜 Transaction history (stored in SQLite)
- 🎨 Bootstrap UI (responsive)
- 🧪 Perfect for cybersecurity labs or demo projects

---

## 🧱 Tech Stack

| Layer      | Technology           |
|------------|----------------------|
| Frontend   | HTML, CSS, Bootstrap |
| Backend    | Python Flask         |
| Database   | SQLite               |
| Hosting    | Flask dev server     |

---

## 📁 Project Structure

DUMMY_BANK/
├── app.py
├── database.db
├── create_db.py
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── dashboard.html
│ ├── transfer.html
│ └── history.html
├── static/
│ └── style.css
└── requirements.txt



---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/dummy-bank-website.git
cd dummy-bank-website

# Install Flask
pip install flask

# Create database
python create_db.py

# Run the app
python app.py
