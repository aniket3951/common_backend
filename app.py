import os
import psycopg2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get("postgresql://auto:AWg52ySEBNMWHf1RkQayhw3Mt43DqR1N@dpg-d64df9cr85hc73bqahvg-a/royaldb_5t09")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    data = request.form
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (name, phone, email, service, event_date, message)
        VALUES (%s, %s, %s, %s, %s, %s)
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
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    bookings = cur.fetchall()
    conn.close()
    return render_template("dashboard.html", bookings=bookings)

