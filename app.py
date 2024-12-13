from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from your frontend on GitHub Pages

load_dotenv()
# Database connection
DB_URI = os.getenv("DATABASE_URL")  # Use environment variable for security

def init_db():
    # Connect to PostgreSQL and create the table
    with psycopg2.connect(DB_URI) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id SERIAL PRIMARY KEY,
                answer TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route("/submit-answer", methods=["POST"])
def submit_answer():
    # Get data from the request
    data = request.get_json()
    answer = data.get("answer")

    if not answer:
        return jsonify({"error": "No answer provided"}), 400

    # Insert data into PostgreSQL
    with psycopg2.connect(DB_URI) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO answers (answer) VALUES (%s)", (answer,))
        conn.commit()

    return jsonify({"message": "Answer recorded successfully!"}), 201

@app.route("/")
def health_check():
    return "Flask backend is running!"

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
