from flask import Flask, render_template, request, redirect
import sqlite3
import string, random

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS urls (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 long_url TEXT NOT NULL,
                 short_code TEXT UNIQUE NOT NULL)""")
    conn.commit()
    conn.close()

# --- Helper: Generate Short Code ---
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# --- Home Page ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form["long_url"]

        # Generate a unique short code
        short_code = generate_short_code()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
        conn.commit()
        conn.close()

        short_url = request.host_url + short_code
        return render_template("index.html", short_url=short_url)

    return render_template("index.html")

# --- Redirect Short URL ---
@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_code=?", (short_code,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "Invalid short URL", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
