from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database path on Render
DB_PATH = "/app/data/booking.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        service TEXT,
        event_date TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Main website homepage
@app.route("/")
def home():
    return render_template("index.html")

# Booking submission
@app.route("/book", methods=["POST"])
def book():
    data = request.form
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (name, phone, email, service, event_date, message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["phone"],
        data["email"],
        data["service"],
        data["date"],
        data["message"]
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("success"))

@app.route("/success")
def success():
    return render_template("success.html")

# Admin dashboard view
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM bookings ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("dashboard.html", bookings=rows)

# Start server
if __name__ == "__main__":
    app.run()
