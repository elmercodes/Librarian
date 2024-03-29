import psycopg2
import psycopg2.extras
import os
from flask import request, jsonify
import traceback
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DB_NAME = os.getenv('DB_NAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')
USERNAME = os.getenv('USERNAME')
DB_HOST = os.getenv('DB_HOST')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=5432,
        dbname=DB_NAME,
        user=USERNAME,
        password=USER_PASSWORD,
        sslmode='require'
    )
    return conn

def get_db_connection():
    conn = psycopg2.connect(
        host="host",
        port=5432,
        dbname="database_name",
        user="db_username",
        password="db_password"
    )
    return conn


def book_inventory():
    book_id = request.args.get('id', type=int)
    if not book_id:
        return jsonify({'error': 'No book ID provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT inventory FROM books WHERE books_id = %s', (book_id,))
    book_inventory = cursor.fetchone()
    cursor.close()
    conn.close()

    if book_inventory:
        return jsonify({'books_id': book_id, 'inventory': book_inventory[0]})
    else:
        return jsonify({'error': 'Book not found'}), 404


def book_by_title():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'No book title provided'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Check if pg_trgm extension is available
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'pg_trgm'")
        if cursor.fetchone() is None:
            return jsonify({'error': 'The pg_trgm extension is not enabled in the database'}), 500

        cursor.execute("""
            SELECT title
            FROM books
            WHERE title %% %s
            ORDER BY similarity(title, %s) DESC;
        """, (title, title))

        books = cursor.fetchall()
        if books:
            return jsonify([dict(book) for book in books])
        else:
            return jsonify({'error': 'Book not found'}), 404

    except Exception as e:
        print(f"Database error: {e}")
        traceback.print_exc()  # Print full traceback
        return jsonify({'error': 'Internal server error'}), 500

    finally:
        cursor.close()
        conn.close()

