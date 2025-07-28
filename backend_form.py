# Import required libraries: Flask for web app, pymysql for MySQL database
from flask import Flask
import pymysql

# Initialize Flask application
app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  
    'password': '',  
    'database': 'tyre_wear_calculator',  
}

# Route for the main page, handling both GET (display form) and POST (process form)
@app.route('/', methods=['GET', 'POST'])
def index():
    # Placeholder for tyre wear calculation (to be replaced with actual logic)
    tyre_wear = "Moderate"

    # Connect to MySQL database to store form data
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Insert car data into car table and get the auto-generated ID
    cursor.execute('INSERT INTO car (car_name, traction_rating, downforce_rating, braking_rating) VALUES (%s, %s, %s, %s)')
        
    # Insert track data into track table and get the auto-generated ID
    cursor.execute('INSERT INTO track (track_name, lap_distance, abrasiveness_rating, evolution_rating) VALUES (%s, %s, %s, %s)')
        
    # Insert tyre wear result into results table, linking to car and track IDs
    cursor.execute('INSERT INTO results (tyre_wear, car_id, track_id) VALUES (%s, %s, %s)')
        
    # Save changes to database
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()