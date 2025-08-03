# Import required libraries: Flask for web app, pymysql for MySQL database
from flask import Flask, request, render_template
import pymysql

# Initialize Flask application
app = Flask(__name__)

# Database configuration
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="tyre_wear_calculator"
)
cursor = conn.cursor()

# Connect to MySQL database to store form data
# Cursor is a Python object that acts as an intermediary between code and database

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

        lap_distance = float(lap_distance)
        abrasiveness = int(abrasiveness)
        evolution = int(evolution)
        traction = int(traction)
        downforce = int(downforce)
        braking_force = int(braking_force)

        # Retrieve the base tyre wear from the database
        cursor.execute('SELECT base_wear FROM tyre WHERE tyre_name = %s', (tyre_name,))
        result = cursor.fetchone()
        base_wear = result[0] if result else "Unknown"

        # Still to be done - calculations for tyre wear
        if tyre_name == 'C1':
            print("The selected tyre is the C1 compound")
            final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_name == 'C2':
            print("The selected tyre is the C2 compound")
            final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_name == 'C3':
            print("The selected tyre is the C3 compound")
            final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_name == 'C4':
            print("The selected tyre is the C4 compound")
            final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)
        elif tyre_name == 'C5':
            print("The selected tyre is the C5 compound")
            final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force
            print(final_wear)

        # Insert car data into car table and get the auto-generated ID
        cursor.execute('INSERT INTO car (car_name, traction, downforce, braking) VALUES (%s, %s, %s, %s)', (car_name, traction, downforce, braking_force))
        
        # Insert track data into track table and get the auto-generated ID
        cursor.execute('INSERT INTO track (track_name, distance, abrasiveness, evolution) VALUES (%s, %s, %s, %s)', (track_name, lap_distance, abrasiveness, evolution))
        
        # Insert tyre wear result into tyre wear table
        cursor.execute('INSERT INTO tyre_wear (final_wear) VALUES (%s)', (final_wear))
        
        # Save changes to database
        conn.commit()

        return render_template('index.html', result=f"Calculated tyre wear for {tyre_name}: {final_wear}")

        # Close cursor and connection
        cursor.close()
        conn.close()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)