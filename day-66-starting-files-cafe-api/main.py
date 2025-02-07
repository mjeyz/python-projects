import os
import sqlite3
from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

# CREATE DB
db_path = "instance/cafes.db"

# Initialize the database and create table if not exists
def init_db():
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cafes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                map_url TEXT NOT NULL,
                img_url TEXT NOT NULL,
                location TEXT NOT NULL,
                seats TEXT NOT NULL,
                has_toilet BOOLEAN NOT NULL,
                has_wifi BOOLEAN NOT NULL,
                has_sockets BOOLEAN NOT NULL,
                can_take_calls BOOLEAN NOT NULL,
                coffee_price TEXT
            )
        ''')
        conn.commit()
        conn.close()

# Initialize the database
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def get_random_cafe():
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cafe")
        cafes = cursor.fetchall()

        if not cafes:
            return jsonify({"error": "No cafes available."}), 404

        random_cafe = random.choice(cafes)

        cafe_data = {
            "id": random_cafe["id"],
            "name": random_cafe["name"],
            "map_url": random_cafe["map_url"],
            "img_url": random_cafe["img_url"],
            "location": random_cafe["location"],
            "has_sockets": bool(random_cafe["has_sockets"]),
            "has_toilet": bool(random_cafe["has_toilet"]),
            "has_wifi": bool(random_cafe["has_wifi"]),
            "can_take_calls": bool(random_cafe["can_take_calls"]),
            "seats": random_cafe["seats"],
            "coffee_price": random_cafe["coffee_price"],
        }

        return jsonify(cafe_data)

@app.route("/all", methods=["GET", "POST"])
def all_cafes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM cafe")
        cafes = cursor.fetchall()

    return jsonify(cafes)


@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")  # Get query parameter
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Query for cafés matching the location if `loc` is provided
        if query_location:
            cursor.execute("SELECT * FROM cafe WHERE location = ?", (query_location,))
        else:
            cursor.execute("SELECT location FROM cafe")

        cafes = cursor.fetchall()

    # Format response to JSON
    cafe_list = [dict(zip([column[0] for column in cursor.description], row)) for row in cafes]

    if cafe_list:
        return jsonify(cafes=cafe_list)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")

    # Check if new_price is provided
    if not new_price:
        return jsonify(error={"Bad Request": "new_price parameter is required."}), 400

    conn = None
    try:
        # Connect to SQLite database (adjust a database path as needed)
        conn = sqlite3.connect('instance/your_database.db')
        cursor = conn.cursor()

        # Check if café exists
        cursor.execute("SELECT id FROM cafe WHERE id = ?", (cafe_id,))
        if not cursor.fetchone():
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

        # Update the price
        cursor.execute(
            "UPDATE cafe SET coffee_price = ? WHERE id = ?",
            (new_price, cafe_id)
        )
        conn.commit()

        return jsonify(response={"success": "Successfully updated the price."}), 200

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        return jsonify(error={"Database Error": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
