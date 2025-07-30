# Import required libraries: Flask for web app, pymysql for MySQL database
from flask import Flask, request
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

# Connect to MySQL database to store form data
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# Route for the main page, handling both GET (display form) and POST (process form)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data from submitted fields
        track_name = request.form['track_name']
        lap_distance = request.form['lap_distance']
        abrasiveness = request.form['abrasiveness']
        evolution = request.form['evolution']
        car_name = request.form['car_name']
        traction = request.form['traction']
        downforce = request.form['downforce']
        braking_force = request.form['braking_force']
        tyre_name = request.form['tyre_name']

        cursor.execute('SELECT base_wear FROM tyre WHERE tyre_name = %s', (tyre_name))
        result = cursor.fetchone()
        tyre_wear = result['base_wear'] if result else "Unknown"

        # Still to be done
        if tyre_wear == 'C1':
            print("The selected tyre is the C1 compound")
            final_wear = tyre_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_wear == 'C2':
            print("The selected tyre is the C2 compound")
            final_wear = tyre_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_wear == 'C3':
            print("The selected tyre is the C3 compound")
            final_wear = tyre_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_wear == 'C4':
            print("The selected tyre is the C4 compound")
            final_wear = tyre_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_wear == 'C5':
            print("The selected tyre is the C5 compound")
            final_wear = tyre_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)

        # Insert car data into car table and get the auto-generated ID
        cursor.execute('INSERT INTO car (car_name, traction_rating, downforce_rating, braking_rating) VALUES (%s, %s, %s, %s)', (car_name, traction, downforce, braking_force))
        
        # Insert track data into track table and get the auto-generated ID
        cursor.execute('INSERT INTO track (track_name, lap_distance, abrasiveness_rating, evolution_rating) VALUES (%s, %s, %s, %s)', (track_name, lap_distance, abrasiveness, evolution))
        
        # Insert tyre wear result into tyre wear table
        cursor.execute('INSERT INTO tyre_wear (final_wear) VALUES (%s)', (final_wear))
        
        # Save changes to database
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()
