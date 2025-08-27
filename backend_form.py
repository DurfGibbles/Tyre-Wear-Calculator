from flask import Flask, send_file, request, render_template
from mangum import Mangum
import pymysql
import os

# Initialize Flask application
app = Flask(__name__, template_folder='templates')

# Database configuration (use environment variables for RDS)
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('RDS_HOST', 'tyre-wear-db.c3uyg622u8ob.ap-southeast-2.rds.amazonaws.com'),
        user=os.environ.get('RDS_USER', 'admin'),
        password=os.environ.get('RDS_PASSWORD', 'Snapegaming193'),
        db=os.environ.get('RDS_DB', 'tyre_wear_calculator'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def serve_index():
    return send_file('templates/index.html')

@app.route('/results')
def serve_results():
    return send_file('templates/results.html')

@app.route('/submit', methods=['POST'])
def handle_form():
    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve form data
        track_name = request.form['track_name']
        lap_distance = float(request.form['lap_distance'])
        abrasiveness = int(request.form['abrasiveness'])
        evolution = int(request.form['evolution'])
        car_name = request.form['car_name']
        traction = int(request.form['traction'])
        downforce = int(request.form['downforce'])
        braking_force = int(request.form['braking_force'])
        tyre_name = request.form['tyre_name']

        # Retrieve base tyre wear from database
        cursor.execute('SELECT base_wear FROM tyre WHERE tyre_name = %s', (tyre_name,))
        result = cursor.fetchone()
        base_wear = result['base_wear'] if result else None

        if base_wear is None:
            return {"error": f"Tyre {tyre_name} not found"}, 400

        # Calculate tyre wear (simplified to avoid redundant conditions)
        final_wear = base_wear * lap_distance * abrasiveness * evolution * traction * downforce * braking_force

        # Insert data into database
        cursor.execute(
            'INSERT INTO car (car_name, traction, downforce, braking) VALUES (%s, %s, %s, %s)',
            (car_name, traction, downforce, braking_force)
        )
        cursor.execute(
            'INSERT INTO track (track_name, distance, abrasiveness, evolution) VALUES (%s, %s, %s, %s)',
            (track_name, lap_distance, abrasiveness, evolution)
        )
        cursor.execute('INSERT INTO tyre_wear (final_wear) VALUES (%s)', (final_wear))

        # Commit changes
        conn.commit()

        # Close database connection
        cursor.close()
        conn.close()

        # Return JSON response for Lambda and render results
        return {
            "message": "Form submitted",
            "data": dict(request.form),
            "result": f"Calculated tyre wear for {tyre_name}: {final_wear}"
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500

# Mangum handler for AWS Lambda
handler = Mangum(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)