import os
import psycopg2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# ✅ Correct way: read DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable not set")
    return psycopg2.connect(DATABASE_URL, sslmode="require")


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            service TEXT,
            event_date TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# ✅ Initialize DB safely on startup
try:
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print("❌ Database init failed:", e)


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
        data.get("name"),
        data.get("phone"),
        data.get("email"),
        data.get("service"),
        data.get("date"),
        data.get("message")
    ))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, phone, email, service, event_date, message, created_at
        FROM bookings
        ORDER BY created_at DESC
    """)
    bookings = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("dashboard.html", bookings=bookings)


if __name__ == "__main__":
    app.run(debug=True)
