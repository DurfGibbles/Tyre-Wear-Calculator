from flask import Flask, request, render_template, redirect
from mangum import Mangum
import pymysql
import os
from asgiref.wsgi import WsgiToAsgi

# Initialize Flask application
app = Flask(__name__, template_folder='templates')

# Database configuration
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
    return redirect('http://tyre-wear-calculator.s3-website-ap-southeast-2.amazonaws.com/index.html')

@app.route('/results')
def serve_results():
    result = request.args.get('result', 'No results available.')
    return render_template('results.html', result=result)

@app.route('/submit', methods=['POST'])
def handle_form():
    try:
        # Validate form data
        required_fields = ['track_name', 'lap_distance', 'abrasiveness', 'evolution', 'car_name', 'traction', 'downforce', 'braking_force', 'tyre_name']
        for field in required_fields:
            if field not in request.form:
                return {"error": f"Missing required field: {field}"}, 400

        # Convert form data
        try:
            lap_distance = float(request.form['lap_distance'])
            abrasiveness = int(request.form['abrasiveness'])
            evolution = int(request.form['evolution'])
            traction = int(request.form['traction'])
            downforce = int(request.form['downforce'])
            braking_force = int(request.form['braking_force'])
        except ValueError as e:
            return {"error": f"Invalid numeric input: {str(e)}"}, 400

        track_name = request.form['track_name']
        car_name = request.form['car_name']
        tyre_name = request.form['tyre_name']

        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve base tyre wear
        cursor.execute('SELECT base_wear FROM tyre WHERE tyre_name = %s', (tyre_name,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return {"error": f"Tyre {tyre_name} not found"}, 400
        base_wear = result['base_wear']

        # Calculate tyre wear
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

        return {
            "message": "Form submitted",
            "data": dict(request.form),
            "result": f"Calculated tyre wear for {tyre_name}: {final_wear}"
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500

# Wrap Flask app with WSGI-to-ASGI adapter
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)