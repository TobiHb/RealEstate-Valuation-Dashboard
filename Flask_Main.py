from flask import Flask, request, Response, render_template
import sqlite3
import csv
import pickle
import numpy as np
from Model import predict_with_model
from Model import feature_names


app = Flask(__name__)

# Database connection
def getconn():
    return sqlite3.connect("property.db")



# Function for initialising Database
def init_database():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS property (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        link TEXT,
        property_type TEXT NOT NULL,
        ZIP TEXT,
        square_meters INTEGER NOT NULL,
        beds INTEGER NOT NULL,
        baths INTEGER NOT NULL,
        price REAL,
        model_price REAL
    )
    """)
    conn.commit()
    conn.close()



# Reset Database (Delete all entries)
@app.route('/reset', methods=['POST'])
def reset_database():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("DELETE FROM property")
    conn.commit()
    conn.close()
    return render_template('reset.html')



# Property Overview
@app.route('/properties')
def properties():
    conn = getconn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM property").fetchall()
    conn.close()
    return render_template('properties.html', rows=rows)



# CSV-Export
@app.route('/export')
def export():
    conn = getconn()
    cur = conn.cursor()
    rows = list(cur.execute("SELECT * FROM property"))
    conn.close()

    def generate_csv():
        yield "ID,Name,Link,Type,ZIP,m²,Beds,Baths,Price,Modelprice\n"
        for row in rows:
            yield ",".join(str(item) if item is not None else "" for item in row) + "\n"

    return Response(generate_csv(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=properties.csv"})



# Add New Property
@app.route('/newproperty', methods=['GET', 'POST'])
def newproperty():
    if request.method == 'POST':
        name = request.form.get('name', type=str)
        link = request.form.get('link', type=str)
        property_type = request.form.get('property_type', type=str)
        ZIP = request.form.get('ZIP', type=str)
        square_meters = request.form.get('square_meters', type=int)
        beds = request.form.get('beds', type=int)
        baths = request.form.get('baths', type=int)
        price = request.form.get('price', type=float)


        # Prepare input data for model
        input_data = {
            'PROPERTYSQFT': square_meters,
            'BEDS': beds,
            'BATH': baths
        }

        # Add ZIP-Code and property_type as optional features
        if f'STATE_{ZIP}' in feature_names:
            input_data[f'STATE_{ZIP}'] = 1  # Set ZIP-Code as binary feature
        if f'TYPE_{property_type}' in feature_names:
            input_data[f'TYPE_{property_type}'] = 1  # Set property_type as binary feature



        # Model Price Prediction-Logic
        try:
            model_price = predict_with_model(input_data)
            print("Input data:", input_data)
                
        except Exception as e:
            print(f"Error during prediction: {e}")
            # "X" for model_price when prediction fails
            model_price = None
            print("Set model_price to N/A")
            print(e)





        # Save object in database
        conn = getconn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO property (name, link, property_type, ZIP, square_meters, beds, baths, price, model_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, link, property_type, ZIP, square_meters, beds, baths, price if price is not None else None, model_price)
        )
        print(f"Inserted dataset with model_price={model_price}")
        conn.commit()
        conn.close()


        # Success page after adding property
        return render_template('success.html')
    
    return render_template('newproperty.html')


# Start Page
@app.route("/")
def home():
    return render_template('root.html')


if __name__ == '__main__':
    # Automatically initialize database
    init_database()
    app.run(debug=True)
